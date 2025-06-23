# Midi-to-Strudel

A python script that converts a Midi file to Strudel code. For artists that like remixing :).

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

> Important to note is that it only supports 4/4 for now! PRs are welcome.

## Requirements
- python: I use 3.11.9 but most versions will work
- mido

## Usage
```
  -m, --midi            Path to the Midi file. [default: Uses first .mid in folder]
  -b, --bar-limit       The amount of bars to convert. 0 means no limit. [default: 0]
  -f, --flat-sequences  No complex timing or chords. [default: off]
  -r, --notes-per-bar   The resolution. Usually in steps of 4 (4, 8, 16...).
                        Higher is more error proof but too high can break the code. [default: 128]
  -t, --tab-size        How many spaces to use for indentation in the output. [default: 2]
```

## TODO
- Support more starting time signatures than only 4/4.
- Support mid-song time signature switches.
