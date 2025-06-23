from collections import defaultdict
import argparse
import logging
import glob
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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--midi', type=str, help='Path to the Midi file. (default: Uses first .mid in folder)')
    parser.add_argument('-b', '--bar-limit', type=int, default=0, help='The amount of bars to convert. 0 means no limit. (default: %(default)s)')
    parser.add_argument('-f', '--flat-sequences', action='store_true', help='No complex timing or chords. (default: off)')
    parser.add_argument('-t', '--tab-size', type=int, default=2, help='How many spaces to use for indentation in the output. (default: %(default)s)')
    parser.add_argument('-n', '--notes-per-bar', type=int, default=128, help='The resolution. Usually in steps of 4 (4, 8, 16...).' \
        ' Higher is more error proof but too high can break the code. (default: %(default)s)')

    args = parser.parse_args()
    parser.print_help()
    print()

    return args

def get_indent(tab_size, tabs=1):
    return ' ' * (tab_size * tabs)

NOTE_NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def note_num_to_str(n):
    return NOTE_NAMES[n % 12].lower() + str(n // 12 - 1)

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

def get_tempo_and_bpm(mid):
    tempo = 500000
    for msg in mid.tracks[0]:
        if msg.type == 'set_tempo':
            tempo = msg.tempo
            break
    
    bpm = mido.tempo2bpm(tempo)
    return tempo, bpm

def quantize_time(timestamp, cycle_start, cycle_len, notes_per_bar):
    pos = (timestamp - cycle_start) / cycle_len
    return round(pos * notes_per_bar) / notes_per_bar

def simplify_subdivisions(subdivs):
    current = subdivs[:]
    n = len(current)
    target_lengths = [n // (2 ** i) for i in range(n.bit_length()) if n % (2 ** i) == 0]
    for target_len in target_lengths:
        step = len(current) // target_len
        valid = True
        for i in range(target_len):
            chunk = current[i * step:(i + 1) * step]
            notes = [x for x in chunk if x != '-']
            if len(notes) > 1 or (notes and chunk.index(notes[0]) != 0):
                valid = False
                break

        if not valid:
            break

        current = [
            next((x for x in current[i * step:(i + 1) * step] if x != '-'), '-')
            for i in range(target_len)
        ]

    return current

def collect_note_events(mid, tempo):
    events = {}
    for idx, track in enumerate(mid.tracks):
        time_sec = 0
        for msg in track:
            time_sec += mido.tick2second(msg.time, mid.ticks_per_beat, tempo)
            if msg.type == 'note_on' and msg.velocity > 0:
                events.setdefault(idx, []).append((time_sec, note_num_to_str(msg.note)))
    return events

def adjust_near_cycle_end(events, cycle_len):
    adjusted = []
    for t, note in events:
        rel = (t % cycle_len) / cycle_len
        if rel > 0.95:
            adjusted.append((((t // cycle_len) + 1) * cycle_len, note))
        else:
            adjusted.append((t, note))
    return adjusted

def flat_mode_output(events):
    events.sort()
    notes = [n for _, n in events]
    return notes[0] if len(notes) == 1 else f"[{' '.join(notes)}]"

def poly_mode_output(events, cycle_start, cycle_len, notes_per_bar):
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
        idx = int(round(pos * notes_per_bar))
        if idx < notes_per_bar:
            group = time_groups[pos]
            subdivisions[idx] = group[0] if len(group) == 1 else f"[{','.join(group)}]"

    if all(x == '-' for x in subdivisions):
        return '-'

    simplified = simplify_subdivisions(subdivisions)
    return simplified[0] if len(simplified) == 1 else f"[{' '.join(simplified)}]"

def build_track_output(events, cycle_len, bpm, args):
    output = [f"setcpm({int(bpm)}/4)\n"]

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

            bar = flat_mode_output(notes_in_cycle) if args.flat_sequences \
                else poly_mode_output(notes_in_cycle, start, cycle_len, args.notes_per_bar)
            bars.append(bar)

        if bars:
            output.append('$: note(`<')

            for i in range(0, len(bars), 4):
                chunk = bars[i:i+4]
                line = ' '.join(chunk)
                output.append(f"{get_indent(args.tab_size, 2)}{line}")

            output.append(f'{get_indent(args.tab_size)}>`).sound("piano")\n')

    return output

def main():
    args = parse_args()
    mid = load_midi_file(args.midi)
    tempo, bpm = get_tempo_and_bpm(mid)
    events = collect_note_events(mid, tempo)
    cycle_len = 60 / bpm * 4
    result = build_track_output(events, cycle_len, bpm, args)

    output_str = '\n'.join(result)
    print(output_str)

    with open('result.txt', 'w') as f:
        f.write(output_str + '\n')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e, exc_info=True)
        sys.exit(1)
