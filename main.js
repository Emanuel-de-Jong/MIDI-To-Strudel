/* ---------- helpers ---------- */
const NOTE_NAMES = [
  "c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"];

const STRUDEL_SOUNDS = [
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
];

const MIDI_SOUNDS = [
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
];

const SOUND_IMPROVEMENT_MAPS = {
  gm_lead_1_square: "square",
  gm_lead_2_sawtooth: "saw"
};

const SOUND_FALLBACK = "piano";

function getSoundName(track) {
  if (!track.instrument) return SOUND_FALLBACK;

  const programNumber = track.instrument.number;
  if (
    typeof programNumber !== "number" ||
    programNumber < 0 ||
    programNumber > MIDI_SOUNDS.length - 1
  ) {
    return SOUND_FALLBACK;
  }

  let soundName = MIDI_SOUNDS[programNumber];
  if (soundName in SOUND_IMPROVEMENT_MAPS)
    return SOUND_IMPROVEMENT_MAPS[soundName];
  if (STRUDEL_SOUNDS.includes(soundName.replace("gm_", "")))
    return soundName.replace("gm_", "");
  if (STRUDEL_SOUNDS.includes(soundName)) return soundName;
  return SOUND_FALLBACK;
}

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
      instrument: track.instrument
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

        if (opts.flatSequences) {
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

      if (bars.length && bars.some((b) => b !== "-")) {
        tracks.push({ bars, track: midi.tracks[trackIdx] });
      }
    });

  /* build text */
  const indent = (n) => " ".repeat(n);

  let longestBarLength = 0;
  tracks.forEach((trackData) => {
    trackData.bars.forEach((bar) => {
      if (bar.length > longestBarLength) longestBarLength = bar.length;
    });
  });

  let barsPerRow = 8;
  if (longestBarLength > 0) {
    const barsFit = Math.floor((160 + 1) / (longestBarLength + 1));
    barsPerRow = Math.max(1, Math.min(8, barsFit));
  }

  const out = [`setcpm(${Math.round(bpm)}/4)\n`];
  console.log("tracks@", tracks);
  tracks.forEach((trackData) => {
    const bars = trackData.bars;
    const track = trackData.track;

    if (opts.smallPrint) {
      out.push(`$: note(\`<${bars.join("")}>\`)`);
    } else {
      out.push("$: note(`<");
      for (let i = 0; i < bars.length; i += barsPerRow) {
        const chunk = bars.slice(i, i + barsPerRow).join(" ");
        out.push(`${indent(opts.tabSize * 2)}${chunk}`);
      }

      out[out.length - 1] += ">`)";
    }

    let soundName = SOUND_FALLBACK;
    if (opts.guessInstrument) {
      soundName = getSoundName(track);
    }

    out.push(`${indent(opts.tabSize)}.sound("${soundName}")\n`);
  });
  return out.join("\n");
}

/* ---------- UI ---------- */
const $ = (q) => document.querySelector(q);
function run(file) {
  const opts = {
    barLimit: parseInt($("#barLimit").value) || 0,
    notesPerBar: parseInt($("#notesPerBar").value) || 64,
    tabSize: parseInt($("#tabSize").value) || 2,
    guessInstrument: $("#guessInstrument").checked,
    flatSequences: $("#flatSequences").checked,
    smallPrint: $("#smallPrint").checked
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
["dragenter", "dragover", "drop"].forEach((eventType) =>
  window.addEventListener(
    eventType,
    (e) => {
      e.preventDefault();
      e.stopPropagation();
    },
    false
  )
);

function handleFileSelect(e) {
  const file = [...e.dataTransfer.files].find((x) =>
    /\.(mid|midi)$/i.test(x.name)
  );
  if (file) {
    $("#file").files = e.dataTransfer.files;
    run(file);
  }
}

window.addEventListener("drop", handleFileSelect, false);
