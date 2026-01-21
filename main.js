/* ---------- helpers ---------- */
const NOTE_NAMES = [
  "c",
  "c#",
  "d",
  "d#",
  "e",
  "f",
  "f#",
  "g",
  "g#",
  "a",
  "a#",
  "b",
];

const gmInstruments = [
  "gm_piano",
  "gm_epiano1",
  "gm_epiano2",
  "gm_harpsichord",
  "gm_clavinet",
  "gm_celesta",
  "gm_glockenspiel",
  "gm_music_box",
  "gm_vibraphone",
  "gm_marimba",
  "gm_xylophone",
  "gm_tubular_bells",
  "gm_dulcimer",
  "gm_drawbar_organ",
  "gm_percussive_organ",
  "gm_rock_organ",
  "gm_church_organ",
  "gm_reed_organ",
  "gm_accordion",
  "gm_harmonica",
  "gm_bandoneon",
  "gm_acoustic_guitar_nylon",
  "gm_acoustic_guitar_steel",
  "gm_electric_guitar_jazz",
  "gm_electric_guitar_clean",
  "gm_electric_guitar_muted",
  "gm_overdriven_guitar",
  "gm_distortion_guitar",
  "gm_guitar_harmonics",
  "gm_acoustic_bass",
  "gm_electric_bass_finger",
  "gm_electric_bass_pick",
  "gm_fretless_bass",
  "gm_slap_bass_1",
  "gm_slap_bass_2",
  "gm_synth_bass_1",
  "gm_synth_bass_2",
  "gm_violin",
  "gm_viola",
  "gm_cello",
  "gm_contrabass",
  "gm_tremolo_strings",
  "gm_pizzicato_strings",
  "gm_orchestral_harp",
  "gm_timpani",
  "gm_string_ensemble_1",
  "gm_string_ensemble_2",
  "gm_synth_strings_1",
  "gm_synth_strings_2",
  "gm_choir_aahs",
  "gm_voice_oohs",
  "gm_synth_choir",
  "gm_orchestra_hit",
  "gm_trumpet",
  "gm_trombone",
  "gm_tuba",
  "gm_muted_trumpet",
  "gm_french_horn",
  "gm_brass_section",
  "gm_synth_brass_1",
  "gm_synth_brass_2",
  "gm_soprano_sax",
  "gm_alto_sax",
  "gm_tenor_sax",
  "gm_baritone_sax",
  "gm_oboe",
  "gm_english_horn",
  "gm_bassoon",
  "gm_clarinet",
  "gm_piccolo",
  "gm_flute",
  "gm_recorder",
  "gm_pan_flute",
  "gm_blown_bottle",
  "gm_shakuhachi",
  "gm_whistle",
  "gm_ocarina",
  "gm_lead_1_square",
  "gm_lead_2_sawtooth",
  "gm_lead_3_calliope",
  "gm_lead_4_chiff",
  "gm_lead_5_charang",
  "gm_lead_6_voice",
  "gm_lead_7_fifths",
  "gm_lead_8_bass_lead",
  "gm_pad_new_age",
  "gm_pad_warm",
  "gm_pad_poly",
  "gm_pad_choir",
  "gm_pad_bowed",
  "gm_pad_metallic",
  "gm_pad_halo",
  "gm_pad_sweep",
  "gm_fx_rain",
  "gm_fx_soundtrack",
  "gm_fx_crystal",
  "gm_fx_atmosphere",
  "gm_fx_brightness",
  "gm_fx_goblins",
  "gm_fx_echoes",
  "gm_fx_sci_fi",
  "gm_sitar",
  "gm_banjo",
  "gm_shamisen",
  "gm_koto",
  "gm_kalimba",
  "gm_bagpipe",
  "gm_fiddle",
  "gm_shanai",
  "gm_tinkle_bell",
  "gm_agogo",
  "gm_steel_drums",
  "gm_woodblock",
  "gm_taiko_drum",
  "gm_melodic_tom",
  "gm_synth_drum",
  "gm_reverse_cymbal",
  "gm_guitar_fret_noise",
  "gm_breath_noise",
  "gm_seashore",
  "gm_bird_tweet",
  "gm_telephone",
  "gm_helicopter",
  "gm_applause",
  "gm_gunshot",
];

function noteNumToStr(n) {
  return NOTE_NAMES[n % 12] + (Math.floor(n / 12) - 1);
}

function quantizeTime(t, cycleStart, cycleLen, notesPerBar) {
  const rel = (t - cycleStart) / cycleLen;
  const q = Math.round(rel * notesPerBar) / notesPerBar;
  return Math.min(q, 1 - 1e-9);
}

function simplifySubdivisions(arr) {
  let cur = arr;
  while (cur.length % 2 === 0) {
    const ok = cur.every((_, i) => (i % 2 === 1 ? cur[i] === "-" : true));
    if (!ok) break;
    cur = cur.filter((_, i) => i % 2 === 0);
  }
  return cur;
}

/* ---------- core ---------- */
function midiToStrudel(arrayBuffer, opts) {
  const midi = new Midi(arrayBuffer); // <- @tonejs/midi
  console.log("midi@", midi);
  const ppq = midi.header.ppq;
  const bpm = midi.header.tempos.length ? midi.header.tempos[0].bpm : 120;
  const cycleLen = (60 / bpm) * 4; // 1 cycle = 4 beats

  /* collect note_on events */
  const events = {}; // trackIndex -> [{time,note},...]
  midi.tracks.forEach((track, idx) => {
    if (!track.notes.length) return;
    events[idx] = track.notes.map((n) => ({
      time: n.time,
      note: noteNumToStr(n.midi),
      instrument: track.instrument,
    }));
  });

  /* build bars */
  const tracks = [];
  Object.keys(events)
    .sort((a, b) => a - b)
    .forEach((trackIdx) => {
      const evs = events[trackIdx];
      /* push notes >95% into next cycle */
      const adj = evs.map((e) => {
        const rel = (e.time % cycleLen) / cycleLen;
        return rel > 0.95
          ? { ...e, time: Math.ceil(e.time / cycleLen) * cycleLen }
          : e;
      });
      const maxT = Math.max(...adj.map((e) => e.time));
      const numCycles =
        opts.barLimit > 0
          ? Math.min(Math.floor(maxT / cycleLen) + 1, opts.barLimit)
          : Math.floor(maxT / cycleLen) + 1;
      const bars = [];
      for (let c = 0; c < numCycles; c++) {
        const start = c * cycleLen,
          end = start + cycleLen;
        const inCycle = adj.filter((e) => e.time >= start && e.time < end);
        if (!inCycle.length) {
          bars.push("-");
          continue;
        }

        if (opts.flat) {
          const notes = inCycle.map((e) => e.note);
          bars.push(notes.length === 1 ? notes[0] : `[${notes.join(" ")}]`);
        } else {
          const groups = {}; // pos -> [notes]
          inCycle.forEach((e) => {
            const pos = quantizeTime(e.time, start, cycleLen, opts.notesPerBar);
            const key = Math.round(pos * opts.notesPerBar) / opts.notesPerBar;
            (groups[key] || (groups[key] = [])).push(e.note);
          });
          const subdiv = Array(opts.notesPerBar).fill("-");
          Object.keys(groups)
            .sort((a, b) => a - b)
            .forEach((k) => {
              const idx = Math.round(parseFloat(k) * opts.notesPerBar);
              if (idx < opts.notesPerBar) {
                const g = groups[k];
                subdiv[idx] = g.length === 1 ? g[0] : `[${g.join(",")}]`;
              }
            });
          const simp = simplifySubdivisions(subdiv);
          const bar = simp.length === 1 ? simp[0] : `[${simp.join(" ")}]`;
          bars.push(
            bar === "[" + Array(opts.notesPerBar).fill("-").join(" ") + "]"
              ? "-"
              : bar
          );
        }
      }
      if (bars.length) tracks.push(bars);
    });

  /* build text */
  const indent = (n) => " ".repeat(n);

  const getInstrumentName = (track) => {
    return track.instrument.family || "piano";
  };

  const out = [`setcpm(${Math.round(bpm)}/4)`];
  console.log("tracks@", tracks);
  tracks.forEach((bars, idx) => {
    out.push("$: note(`<");
    for (let i = 0; i < bars.length; i += 4) {
      const chunk = bars.slice(i, i + 4).join(" ");
      out.push(`${indent(opts.tabSize * 2)}${chunk}`);
    }
    out[out.length - 1] += ">`)";
    let _track = midi.tracks[idx];
    console.log("_track@", _track);
    out.push(`.sound("${getInstrumentName(_track)}")`);
    out.push("");
  });
  return out.join("\n");
}

/* ---------- UI ---------- */
const $ = (q) => document.querySelector(q);
function run(file) {
  const opts = {
    barLimit: parseInt($("#barLimit").value) || 0,
    notesPerBar: parseInt($("#notesPerBar").value) || 64,
    flat: $("#flat").checked,
    tabSize: parseInt($("#tabSize").value) || 2,
  };
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      $("#output").value = midiToStrudel(e.target.result, opts);
      $("#openBtn").classList.remove("hidden");
    } catch (err) {
      $("#output").value = "Error: " + err.message;
      $("#openBtn").classList.add("hidden");
    }
  };
  reader.readAsArrayBuffer(file);
}
$("#openBtn").addEventListener("click", () => {
  const txt = $("#output").value;
  if (!txt) return;
  const b64 = btoa(unescape(encodeURIComponent(txt)));
  window.open("https://strudel.cc/#" + b64, "_blank");
});
// Only set file input, don't auto-convert
$("#file").addEventListener("change", (e) => {
  // No conversion here; wait for manual button
});

// Manual convert button
$("#convertBtn").addEventListener("click", () => {
  const fileInput = $("#file");
  if (fileInput.files && fileInput.files[0]) {
    run(fileInput.files[0]);
  } else {
    $("#output").value = "No MIDI file selected.";
    $("#openBtn").classList.add("hidden");
  }
});
/* drag & drop */
["dragenter", "dragover", "drop"].forEach((ev) =>
  window.addEventListener(
    ev,
    (e) => {
      e.preventDefault();
      e.stopPropagation();
    },
    false
  )
);
window.addEventListener(
  "drop",
  (e) => {
    const f = [...e.dataTransfer.files].find((x) => /\.mid$/i.test(x.name));
    if (f) {
      $("#file").files = e.dataTransfer.files;
      run(f);
    }
  },
  false
);
