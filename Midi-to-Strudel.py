from collections import defaultdict
import argparse
import logging
import glob
import math
import sys
import os
import mido

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("log.log", encoding="utf-8", mode="a")
    file_handler.setFormatter(logging.Formatter(
        "[{asctime}][{levelname}]: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{"
    ))

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(
        "[{levelname}]: {message}",
        style="{"
    ))

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

logger = setup_logging()

def main():
    args = parse_args()
    mid = load_midi_file(args.midi)
    tempo, bpm, cycle_len = get_timing_values(mid)
    events = collect_note_events(mid, tempo)
    tracks = build_tracks(events, cycle_len, args)
    output = build_output(tracks, bpm, args.tab_size)

    print(output)
    with open('result.txt', 'w') as f:
        f.write(output + '\n')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--midi', type=str, help='Path to the Midi file. (default: Uses first .mid in folder)')
    parser.add_argument('-b', '--bar-limit', type=int, default=0, help='The amount of bars to convert. 0 means no limit. (default: %(default)s)')
    parser.add_argument('-f', '--flat-sequences', action='store_true', help='No complex timing or chords. (default: off)')
    parser.add_argument('-t', '--tab-size', type=int, default=2, help='How many spaces to use for indentation in the output. (default: %(default)s)')
    parser.add_argument('-n', '--notes-per-bar', type=int, default=64, help='The resolution. Usually in steps of 4 (4, 8, 16...).' \
        ' Higher gives better note placement but can get big. (default: %(default)s)')

    args = parser.parse_args()
    parser.print_help()
    print()

    return args

def load_midi_file(midi_path):
    if midi_path:
        if not os.path.exists(midi_path):
            print(f"MIDI file not found: {midi_path}")
            sys.exit(1)
        return mido.MidiFile(midi_path)
    
    midi_files = glob.glob("*.mid")
    if not midi_files:
        print("No MIDI files found")
        sys.exit(1)
    return mido.MidiFile(midi_files[0])

def get_timing_values(mid):
    tempo = 500000
    for msg in mid.tracks[0]:
        if msg.type == 'set_tempo':
            tempo = msg.tempo
            break
    
    bpm = mido.tempo2bpm(tempo)
    cycle_len = 60 / bpm * 4
    return tempo, bpm, cycle_len

def collect_note_events(mid, tempo):
    events = defaultdict(list)
    for i, track in enumerate(mid.tracks):
        time_sec = 0
        for msg in track:
            time_sec += mido.tick2second(msg.time, mid.ticks_per_beat, tempo)
            if msg.type == 'note_on' and msg.velocity > 0:
                events[i].append((time_sec, note_num_to_str(msg.note)))
    return events

NOTE_NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def note_num_to_str(n):
    return NOTE_NAMES[n % 12].lower() + str(n // 12 - 1)

def build_tracks(events, cycle_len, args):
    tracks = []
    for track in sorted(events):
        evs = adjust_near_cycle_end(events[track], cycle_len)
        if not evs:
            continue

        max_time = max(t for t, _ in evs)
        num_cycles = min((int(max_time / cycle_len) + 1), args.bar_limit if args.bar_limit > 0 else float('inf'))
        bars = []

        for c in range(num_cycles):
            start = c * cycle_len
            end = start + cycle_len
            notes_in_cycle = [(t, n) for t, n in evs if start <= t < end]

            if not notes_in_cycle:
                bars.append('-')
                continue

            bar = get_flat_mode_bar(notes_in_cycle) if args.flat_sequences \
                else get_poly_mode_bar(notes_in_cycle, start, cycle_len, args.notes_per_bar)
            bars.append(bar)

        if bars and len(bars) > 0:
            tracks.append(bars)

    return tracks

def adjust_near_cycle_end(events, cycle_len):
    adjusted = []
    for t, note in events:
        rel = (t % cycle_len) / cycle_len
        if rel > 0.95:
            adjusted.append((math.ceil(t / cycle_len) * cycle_len, note))
        else:
            adjusted.append((t, note))
    return adjusted

def get_flat_mode_bar(events):
    events.sort()
    notes = [n for _, n in events]
    return notes[0] if len(notes) == 1 else f"[{' '.join(notes)}]"

def get_poly_mode_bar(events, cycle_start, cycle_len, notes_per_bar):
    time_groups = defaultdict(list)
    for t, n in events:
        pos = quantize_time(t, cycle_start, cycle_len, notes_per_bar)
        for existing in time_groups:
            if abs(pos - existing) < 1 / notes_per_bar:
                time_groups[existing].append(n)
                break
        else:
            time_groups[pos].append(n)

    if not time_groups:
        return '-'

    subdivisions = ['-'] * notes_per_bar
    for pos in sorted(time_groups):
        i = int(round(pos * notes_per_bar))
        if i < notes_per_bar:
            group = time_groups[pos]
            subdivisions[i] = group[0] if len(group) == 1 else f"[{','.join(group)}]"

    if all(x == '-' for x in subdivisions):
        return '-'

    simplified = simplify_subdivisions(subdivisions)
    return simplified[0] if len(simplified) == 1 else f"[{' '.join(simplified)}]"

def quantize_time(timestamp, cycle_start, cycle_len, notes_per_bar):
    pos = (timestamp - cycle_start) / cycle_len
    return round(pos * notes_per_bar) / notes_per_bar

def simplify_subdivisions(subdivs):
    current = subdivs
    while len(current) % 2 == 0:
        pairs = list(zip(current[::2], current[1::2]))
        if any(b != '-' for _, b in pairs):
            break

        current = [a for a, _ in pairs]
    
    return current

def build_output(tracks, bpm, tab_size):
    output = [f"setcpm({int(bpm)}/4)\n"]
    
    for bars in tracks:
        output.append('$: note(`<')
        for i in range(0, len(bars), 4):
            chunk = bars[i:i+4]
            line = ' '.join(chunk)
            output.append(f"{get_indent(tab_size, 2)}{line}")
        output.append(f'{get_indent(tab_size)}>`).sound("piano")\n')
    
    return '\n'.join(output)

def get_indent(tab_size, tabs=1):
    return ' ' * (tab_size * tabs)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e, exc_info=True)
        sys.exit(1)
