# MIDI To Strudel 

> You can try the web version here - https://github.com/rayanfer32/midi-to-strudel-web

Read more about webapp - [README.web](/README.web.md)

A python script that converts a Midi file to Strudel code. For artists that like remixing.

It sets the right cpm and creates a new sound source per Midi track. Example output:
```
setcpm(91/4)

$: note(`<
    [g#4 c5 g4 g#4 f4 g4 d#4 d4] [- - - - - - - g#4] [- c5 g4 g#4 f4 g4 g#4 a#4] -
    [- - f4 f4 g#4 g#4 f4 f4] [c5 c5 - c5 - g#4 - -] [a#4 a#4 - a#4 - g4 - -] [a#4 a#4 - a#4 - g#4 g4 f4]
  >`).sound("piano")

$: note(`<
    [- [g#3,c4] f3 [g#3,c4]] [a#3 [d4,f4] a#3 [d4,f4]] [f3 [g#3,c4] f3 [g#3,c4]] [a#3 [d4,f4] a#3 [d4,f4]]
    [f3 [g#3,c4] f3 [g#3,c4]] [g#3 [c4,d#4] g#3 [c4,d#4]] [d#3 [g3,a#3] d#3 [g3,a#3]] [a#3 [d4,f4] a#3 [d4,f4]]
  >`).sound("piano")
```

> [!NOTE]
> Only 4/4 time signature is supported for now! PRs are welcome.

**Active Development:** 2025-06-23 - 2025-06-23<br>
**Last Change:** 2025-06-27<br>

| | |
| :---: | :---: |
| ![](/Screenshots/.png) | ![](/Screenshots/.png) |

## Requirements
- python: I use 3.11.9 but most versions will work
- mido

## Usage
1. Run `pip install -r requirements.txt` to install the dependencies.
2. There are two ways to run the tool:
    - If you're on Windows, the easiest way is dragging your Midi file onto the `Drag-and-Drop.bat` script. However, this way you can't set console arguments.
    - Run the tool directly with `python Midi-to-Strudel.py`.
3. Get the Strudel code. Either from the text in the console or the content of the new `result.txt` file.

### Arguments
```
usage: Midi-to-Strudel.py [-h] [-m MIDI] [-b BAR_LIMIT] [-f] [-t TAB_SIZE] [-n NOTES_PER_BAR]
  -m, --midi            Path to the Midi file. (default: Uses first .mid in folder)
  -b, --bar-limit       The amount of bars to convert. 0 means no limit. (default: 0)
  -f, --flat-sequences  No complex timing or chords. (default: off)
  -t, --tab-size        How many spaces to use for indentation in the output. (default: 2)
  -n, --notes-per-bar   The resolution. Usually in steps of 4 (4, 8, 16...).
                        Higher gives better note placement but can get big. (default: 64)
```

## TODO
- Support more starting time signatures than only 4/4.
- Support mid-song time signature switches.
 