from collections import defaultdict
import argparse
import logging
import glob
import math
import sys
import os
import mido

NOTE_NAMES = [
    'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']

STRUDEL_SOUNDS = [
    "agogo","balafon","balafon_hard","balafon_soft","ballwhistle","belltree",
    "bongo","bytebeat","cabasa","cajon","casio","clash","clash2","clave",
    "clavisynth","conga","cowbell","dantranh","dantranh_tremolo",
    "dantranh_vibrato","darbuka","didgeridoo","fingercymbal","flexatone",
    "fmpiano","folkharp","framedrum","glockenspiel","gm_accordion",
    "gm_acoustic_bass","gm_acoustic_guitar_nylon","gm_acoustic_guitar_steel",
    "gm_agogo","gm_alto_sax","gm_applause","gm_bagpipe","gm_bandoneon",
    "gm_banjo","gm_baritone_sax","gm_bassoon","gm_bird_tweet",
    "gm_blown_bottle","gm_brass_section","gm_breath_noise","gm_celesta",
    "gm_cello","gm_choir_aahs","gm_church_organ","gm_clarinet","gm_clavinet",
    "gm_contrabass","gm_distortion_guitar","gm_drawbar_organ","gm_dulcimer",
    "gm_electric_bass_finger","gm_electric_bass_pick","gm_electric_guitar_clean",
    "gm_electric_guitar_jazz","gm_electric_guitar_muted","gm_english_horn",
    "gm_epiano1","gm_epiano2","gm_fiddle","gm_flute","gm_french_horn",
    "gm_fretless_bass","gm_fx_atmosphere","gm_fx_brightness","gm_fx_crystal",
    "gm_fx_echoes","gm_fx_goblins","gm_fx_rain","gm_fx_sci_fi",
    "gm_fx_soundtrack","gm_glockenspiel","gm_guitar_fret_noise",
    "gm_guitar_harmonics","gm_gunshot","gm_harmonica","gm_harpsichord",
    "gm_helicopter","gm_kalimba","gm_koto","gm_lead_1_square",
    "gm_lead_2_sawtooth","gm_lead_3_calliope","gm_lead_4_chiff",
    "gm_lead_5_charang","gm_lead_6_voice","gm_lead_7_fifths",
    "gm_lead_8_bass_lead","gm_marimba","gm_melodic_tom","gm_music_box",
    "gm_muted_trumpet","gm_oboe","gm_ocarina","gm_orchestra_hit",
    "gm_orchestral_harp","gm_overdriven_guitar","gm_pad_bowed",
    "gm_pad_choir","gm_pad_halo","gm_pad_metallic","gm_pad_new_age",
    "gm_pad_poly","gm_pad_sweep","gm_pad_warm","gm_pan_flute",
    "gm_percussive_organ","gm_piano","gm_piccolo","gm_pizzicato_strings",
    "gm_recorder","gm_reed_organ","gm_reverse_cymbal","gm_rock_organ",
    "gm_seashore","gm_shakuhachi","gm_shamisen","gm_shanai","gm_sitar",
    "gm_slap_bass_1","gm_slap_bass_2","gm_soprano_sax","gm_steel_drums",
    "gm_string_ensemble_1","gm_string_ensemble_2","gm_synth_bass_1",
    "gm_synth_bass_2","gm_synth_brass_1","gm_synth_brass_2","gm_synth_choir",
    "gm_synth_drum","gm_synth_strings_1","gm_synth_strings_2",
    "gm_taiko_drum","gm_telephone","gm_tenor_sax","gm_timpani",
    "gm_tinkle_bell","gm_tremolo_strings","gm_trombone","gm_trumpet",
    "gm_tuba","gm_tubular_bells","gm_vibraphone","gm_viola","gm_violin",
    "gm_voice_oohs","gm_whistle","gm_woodblock","gm_xylophone",
    "gong","gong2","guiro","handbells","handchimes","harmonica",
    "harmonica_soft","harmonica_vib","harp","kalimba","kalimba2","kalimba3",
    "kalimba4","kalimba5","kawai","korgkrz_fx","krz_fx","marimba",
    "marktrees","mc303_fx","mridangam_ardha","mridangam_chaapu",
    "mridangam_dhi","mridangam_dhin","mridangam_dhum","mridangam_gumki",
    "mridangam_ka","mridangam_ki","mridangam_na","mridangam_nam",
    "mridangam_ta","mridangam_tha","mridangam_thom","ocarina",
    "ocarina_small","ocarina_small_stacc","ocarina_vib","oceandrum",
    "organ_4inch","organ_8inch","organ_full","piano","piano1",
    "pipeorgan_loud","pipeorgan_loud_pedal","pipeorgan_quiet",
    "pipeorgan_quiet_pedal","psaltery_bow","psaltery_pluck",
    "psaltery_spiccato","pulse","recorder_alto_stacc","recorder_alto_sus",
    "recorder_alto_vib","recorder_bass_stacc","recorder_bass_sus",
    "recorder_bass_vib","recorder_soprano_stacc","recorder_soprano_sus",
    "recorder_tenor_stacc","recorder_tenor_sus","recorder_tenor_vib",
    "rolandmc303_fx","rx5_fx","saw","sawtooth","sax","sax_stacc","sax_vib",
    "saxello","saxello_stacc","saxello_vib","shaker_large","shaker_small",
    "sin","sine","sleighbells","slitdrum","sqr","square","steinway",
    "strumstick","super64","super64_acc","super64_vib","supersaw",
    "tambourine","tambourine2","tg33_fx","timpani","timpani_roll","timpani2",
    "tri","triangle","triangles","tubularbells","tubularbells2",
    "vibraphone","vibraphone_bowed","vibraphone_soft","vibraslap",
    "woodblock","wt_digital","wt_digital_bad_day","wt_digital_basique",
    "wt_digital_crickets","wt_digital_curses","wt_digital_echoes",
    "wt_vgame","xylophone_hard_ff","xylophone_hard_pp",
    "xylophone_medium_ff","xylophone_medium_pp","xylophone_soft_ff",
    "xylophone_soft_pp","yamaharx5_fx","yamahatg33_fx","z_sawtooth",
    "z_sine","z_square","z_tan","z_triangle","zzfx"
]

MIDI_SOUNDS = [
    "gm_piano","gm_piano","gm_epiano1","gm_piano","gm_epiano1","gm_epiano2","gm_harpsichord","gm_clavinet",
    "gm_celesta","gm_glockenspiel","gm_music_box","gm_vibraphone","gm_marimba","gm_xylophone","gm_tubular_bells","gm_dulcimer",
    "gm_drawbar_organ","gm_percussive_organ","gm_rock_organ","gm_church_organ","gm_reed_organ","gm_accordion","gm_harmonica","gm_bandoneon",
    "gm_acoustic_guitar_nylon","gm_acoustic_guitar_steel","gm_electric_guitar_jazz","gm_electric_guitar_clean",
    "gm_electric_guitar_muted","gm_overdriven_guitar","gm_distortion_guitar","gm_guitar_harmonics",
    "gm_acoustic_bass","gm_electric_bass_finger","gm_electric_bass_pick","gm_fretless_bass",
    "gm_slap_bass_1","gm_slap_bass_2","gm_synth_bass_1","gm_synth_bass_2",
    "gm_violin","gm_viola","gm_cello","gm_contrabass",
    "gm_tremolo_strings","gm_pizzicato_strings","gm_orchestral_harp","gm_timpani",
    "gm_string_ensemble_1","gm_string_ensemble_2","gm_synth_strings_1","gm_synth_strings_2",
    "gm_choir_aahs","gm_voice_oohs","gm_synth_choir","gm_orchestra_hit",
    "gm_trumpet","gm_trombone","gm_tuba","gm_muted_trumpet",
    "gm_french_horn","gm_brass_section","gm_synth_brass_1","gm_synth_brass_2",
    "gm_soprano_sax","gm_alto_sax","gm_tenor_sax","gm_baritone_sax",
    "gm_oboe","gm_english_horn","gm_bassoon","gm_clarinet",
    "gm_piccolo","gm_flute","gm_recorder","gm_pan_flute",
    "gm_blown_bottle","gm_shakuhachi","gm_whistle","gm_ocarina",
    "gm_lead_1_square","gm_lead_2_sawtooth","gm_lead_3_calliope","gm_lead_4_chiff",
    "gm_lead_5_charang","gm_lead_6_voice","gm_lead_7_fifths","gm_lead_8_bass_lead",
    "gm_pad_new_age","gm_pad_warm","gm_pad_poly","gm_pad_choir",
    "gm_pad_bowed","gm_pad_metallic","gm_pad_halo","gm_pad_sweep",
    "gm_fx_rain","gm_fx_soundtrack","gm_fx_crystal","gm_fx_atmosphere",
    "gm_fx_brightness","gm_fx_goblins","gm_fx_echoes","gm_fx_sci_fi",
    "gm_sitar","gm_banjo","gm_shamisen","gm_koto",
    "gm_kalimba","gm_shanai","gm_fiddle","gm_shanai",
    "gm_tinkle_bell","gm_agogo","gm_steel_drums","gm_woodblock",
    "gm_taiko_drum","gm_melodic_tom","gm_synth_drum","gm_reverse_cymbal",
    "gm_guitar_fret_noise","gm_breath_noise","gm_fx_rain","gm_fx_brightness",
    "gm_fx_echoes","gm_fx_echoes","gm_fx_echoes","gm_fx_echoes"
]

SOUND_IMPROVEMENT_MAPS = {
    "gm_piano": "piano",
    "gm_lead_1_square": "square",
    "gm_lead_2_sawtooth": "saw"
}

SOUND_FALLBACK = "piano"

def get_sound_name(program_number):
    if not isinstance(program_number, int) or program_number < 0 or program_number > len(MIDI_SOUNDS) - 1:
        return SOUND_FALLBACK

    sound_name = MIDI_SOUNDS[program_number]

    if sound_name in SOUND_IMPROVEMENT_MAPS:
        return SOUND_IMPROVEMENT_MAPS[sound_name]

    stripped_sound_name = sound_name.replace("gm_", "")
    if stripped_sound_name in STRUDEL_SOUNDS:
        return stripped_sound_name

    if sound_name in STRUDEL_SOUNDS:
        return sound_name

    return SOUND_FALLBACK

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
    events, instruments = collect_note_events(mid, tempo)
    tracks = build_tracks(events, cycle_len, args)
    output = build_output(tracks, bpm, instruments, args)

    print(output)
    with open('result.txt', 'w', encoding='utf-8') as f:
        f.write(output + '\n')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--midi', type=str, help='Path to the Midi file. (default: Uses first .mid in folder)')
    parser.add_argument('-b', '--bar-limit', type=int, default=0, help='The amount of bars to convert. 0 means no limit. (default: %(default)s)')
    parser.add_argument('-n', '--notes-per-bar', type=int, default=64, help='The resolution. Usually in steps of 4 (4, 8, 16...).' \
        ' Higher gives better note placement but can get big. (default: %(default)s)')
    parser.add_argument('-t', '--tab-size', type=int, default=2, help='How many spaces to use for indentation in the output. (default: %(default)s)')
    parser.add_argument('-g', '--guess-instrument', action='store_true', help='Use the sounds closest to the instruments mentioned in the MIDI. (default: off)')
    parser.add_argument('-f', '--flat-sequences', action='store_true', help='No complex timing or chords. (default: off)')

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
    
    midi_files = glob.glob("*.mid") + glob.glob("*.midi")
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
    instruments = {}
    programs = {}
    for track_index, track in enumerate(mid.tracks):
        time_sec = 0
        for msg in track:
            time_sec += mido.tick2second(msg.time, mid.ticks_per_beat, tempo)

            if msg.type == 'program_change':
                programs[(track_index, msg.channel)] = msg.program

            if msg.type == 'note_on' and msg.velocity > 0:
                key = (track_index, msg.channel)
                events[key].append((time_sec, note_num_to_str(msg.note)))
                if key not in instruments:
                    instruments[key] = programs.get(key)

    return events, instruments

def note_num_to_str(n):
    return NOTE_NAMES[n % 12].lower() + str(n // 12 - 1)

def build_tracks(events, cycle_len, args):
    tracks = []
    for track_key in sorted(events):
        evs = adjust_near_cycle_end(events[track_key], cycle_len)
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

        if bars and any(bar != '-' for bar in bars):
            tracks.append((track_key, bars))

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
    notes = [n for _, n in sorted(events)]
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
    rel_time = (timestamp - cycle_start) / cycle_len
    quantized = round(rel_time * notes_per_bar) / notes_per_bar
    return min(quantized, 1.0 - 1e-9)

def simplify_subdivisions(subdivs):
    current = subdivs
    while len(current) % 2 == 0:
        pairs = list(zip(current[::2], current[1::2]))
        if any(second != '-' for _, second in pairs):
            break

        current = [first for first, _ in pairs]
    
    return current

def build_output(tracks, bpm, instruments, args):
    output = [f"setcpm({int(bpm)}/4)\n"]
    
    for track_key, bars in tracks:
        output.append('$: note(`<')
        for i in range(0, len(bars), 4):
            chunk = bars[i:i+4]
            output.append(f"{get_indent(args.tab_size, 2)}{' '.join(chunk)}")
        
        output[len(output) - 1] += '>`)'

        sound_name = SOUND_FALLBACK
        if args.guess_instrument:
            sound_name = get_sound_name(instruments.get(track_key))

        output.append(f"{get_indent(args.tab_size, 1)}.sound(\"{sound_name}\")\n")
    
    return '\n'.join(output)

def get_indent(tab_size, tabs=1):
    return ' ' * (tab_size * tabs)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e, exc_info=True)
        sys.exit(1)
