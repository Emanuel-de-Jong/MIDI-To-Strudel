# MIDI To Strudel code (Web)

> Webapp - https://github.com/rayanfer32/midi-to-strudel-web

A simple browser-based converter is included so you can try conversions without installing Python. The web UI accepts a MIDI file via drag & drop or file picker and shows the resulting Strudel code directly in the page.

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

Notes:

- The web version runs entirely client-side. No files are uploaded to a server and the conversion happens in your browser.
- If you encounter browser permission or CORS issues, serve the repo with `python -m http.server`

## TODO

- Support more starting time signatures than only 4/4.
- Support mid-song time signature switches.
