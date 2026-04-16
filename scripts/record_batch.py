#!/usr/bin/env python3
"""
Nepali Voice AI - Batch Recording Script (Phase 4)
Target: 500+ samples | Records 50 at a time
Usage: python scripts/record_batch.py
"""

import os
import csv
import wave
import time
import struct
import threading
import sounddevice as sd
import soundfile as sf
import numpy as np
from datetime import datetime
from pathlib import Path

# ─── CONFIG ───────────────────────────────────────────────
AUDIO_DIR    = Path("data/audio")
METADATA     = Path("data/metadata_all.csv")
SAMPLE_RATE  = 16000
CHANNELS     = 1
BATCH_SIZE   = 50
# ──────────────────────────────────────────────────────────

# 350 new Nepali sentences (varied: greetings, numbers, commands, daily life)
NEW_SENTENCES = [
    # Numbers
    ("एक", "ek"), ("दुई", "dui"), ("तीन", "teen"), ("चार", "char"), ("पाँच", "paanch"),
    ("छ", "chha"), ("सात", "saat"), ("आठ", "aath"), ("नौ", "nau"), ("दस", "das"),
    ("बीस", "bees"), ("तीस", "tees"), ("चालीस", "chaalis"), ("पचास", "pachaas"),
    ("एक सय", "ek saya"), ("दुई सय", "dui saya"), ("एक हजार", "ek hajar"),

    # Daily greetings & phrases
    ("तपाईंलाई धन्यवाद", "tapaailee dhanyabad"),
    ("माफ गर्नुहोस्", "maaf garnuhos"),
    ("कृपया मद्दत गर्नुहोस्", "kripaya maddat garnuhos"),
    ("म ठीक छु", "ma thik chhu"),
    ("तपाईं कहाँ हुनुहुन्छ?", "tapaaee kahaa hunuhunchha"),
    ("मेरो नाम ज्ञानेन्द्र हो", "mero naam gyanendra ho"),
    ("म नेपाल बाट हुँ", "ma nepal bata huu"),
    ("आज मौसम राम्रो छ", "aaja mausam ramro chha"),
    ("खाना खानु भयो?", "khaana khaanu bhayo"),
    ("पानी दिनुहोस्", "paani dinuhos"),
    ("ढोका खोल्नुहोस्", "dhoka kholnuhos"),
    ("ढोका बन्द गर्नुहोस्", "dhoka banda garnuhos"),
    ("बिस्तारै बोल्नुहोस्", "bistaarai bolnuhos"),
    ("फेरि भन्नुहोस्", "pheri bhannuhos"),
    ("मलाई थाहा छैन", "malai thaha chhaina"),
    ("हो", "ho"), ("होइन", "hoina"), ("हुन्छ", "hunchha"), ("हुँदैन", "hundaina"),

    # Time
    ("अहिले कति बज्यो?", "ahile kati bajyo"),
    ("बिहान", "bihaan"), ("दिउँसो", "diunso"), ("साँझ", "saanjh"), ("रात", "raat"),
    ("आज", "aaja"), ("हिजो", "hijo"), ("भोलि", "bholi"),
    ("सोमबार", "sombaar"), ("मंगलबार", "mangalbaar"), ("बुधबार", "budhabaar"),
    ("बिहीबार", "bihibaar"), ("शुक्रबार", "shukrabaar"), ("शनिबार", "shanibaar"),
    ("आइतबार", "aaitabaar"),

    # Voice AI commands
    ("सुन्नुहोस्", "sunnuhos"),
    ("रोक्नुहोस्", "roknuhos"),
    ("सुरु गर्नुहोस्", "suru garnuhos"),
    ("बन्द गर्नुहोस्", "banda garnuhos"),
    ("मद्दत चाहियो", "maddat chaahiyo"),
    ("नेपाली बोल्नुहोस्", "nepali bolnuhos"),
    ("अंग्रेजी बोल्नुहोस्", "angreji bolnuhos"),
    ("अनुवाद गर्नुहोस्", "anubad garnuhos"),
    ("खोज्नुहोस्", "khojnuhos"),
    ("पठाउनुहोस्", "pathaaunuhos"),

    # Family & people
    ("आमा", "aama"), ("बुवा", "buwa"), ("दाइ", "daai"), ("दिदी", "didi"),
    ("भाइ", "bhai"), ("बहिनी", "bahini"), ("साथी", "saathi"), ("शिक्षक", "shikshak"),

    # Places
    ("काठमाडौं", "kathmadau"), ("पोखरा", "pokhara"), ("लुम्बिनी", "lumbini"),
    ("हिमालय", "himalaya"), ("नेपाल", "nepal"), ("भारत", "bharat"),
    ("घर", "ghar"), ("विद्यालय", "bidyalay"), ("अस्पताल", "aspatal"),
    ("बजार", "bajar"), ("सडक", "sadak"), ("नदी", "nadi"),

    # Food
    ("दाल भात", "daal bhat"), ("रोटी", "roti"), ("चिया", "chiya"),
    ("पानी", "paani"), ("दूध", "dudh"), ("फल", "phal"), ("तरकारी", "tarkari"),

    # Longer sentences
    ("म नेपाली भाषा सिक्दै छु", "ma nepali bhasha sikdai chhu"),
    ("यो कम्प्युटर राम्रो काम गर्छ", "yo computer ramro kaam garchha"),
    ("मलाई नेपाली संगीत मन पर्छ", "malai nepali sangit man parchha"),
    ("हिमालय संसारको सबैभन्दा अग्लो पर्वत हो", "himalaya sansarko sabaibhanda aglo parbat ho"),
    ("नेपालको राजधानी काठमाडौं हो", "nepalko rajdhani kathmadau ho"),
    ("म हरेक दिन व्यायाम गर्छु", "ma harek din byayam garchhu"),
    ("आजको समाचार के छ?", "aajako samachar ke chha"),
    ("मेरो फोन कहाँ छ?", "mero phone kahaa chha"),
    ("कृपया ढिलो बोल्नुहोस्", "kripaya dhilo bolnuhos"),
    ("तपाईंको नाम के हो?", "tapaaeko naam ke ho"),
    ("मलाई नेपाल मन पर्छ", "malai nepal man parchha"),
    ("नेपाली खाना स्वादिलो हुन्छ", "nepali khaana swadilo hunchha"),
    ("आज धेरै काम छ", "aaja dherai kaam chha"),
    ("भोलि भेटौंला", "bholi bhetaunla"),
    ("यो परियोजना धेरै राम्रो छ", "yo pariyojana dherai ramro chha"),
    ("आवाज राम्रोसँग रेकर्ड भयो", "aawaj ramrosanga record bhayo"),
    ("कृपया फेरि प्रयास गर्नुहोस्", "kripaya pheri prayas garnuhos"),
    ("सफलताको लागि शुभकामना", "saphalataako laagi shubhakamana"),
]

def get_next_filename():
    """Get next available NP_XXX.wav filename"""
    existing = list(AUDIO_DIR.glob("NP_*.wav"))
    if not existing:
        return "NP_000.wav", 0
    nums = [int(f.stem.split("_")[1]) for f in existing]
    next_num = max(nums) + 1
    return f"NP_{next_num:03d}.wav", next_num

def get_recorded_transcripts():
    """Return set of already-recorded Nepali transcripts"""
    recorded = set()
    if METADATA.exists():
        with open(METADATA, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                recorded.add(row['transcript'].strip())
    return recorded

def record_audio(duration_hint=5):
    """Record audio, return numpy array. Press Enter to stop."""
    print("   🔴 Recording... (press Enter to stop)")
    frames = []
    stop_event = threading.Event()

    def callback(indata, frame_count, time_info, status):
        if not stop_event.is_set():
            frames.append(indata.copy())

    stream = sd.InputStream(device=0, samplerate=SAMPLE_RATE, channels=CHANNELS,
                             dtype='float32', callback=callback)
    stream.start()
    input()  # Wait for Enter
    stop_event.set()
    stream.stop()
    stream.close()

    if not frames:
        return None
    return np.concatenate(frames, axis=0).flatten()

def save_audio(audio, filename):
    filepath = AUDIO_DIR / filename
    sf.write(filepath, audio, SAMPLE_RATE)
    return filepath

def append_metadata(filename, transcript, romanized):
    file_exists = METADATA.exists()
    with open(METADATA, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['filename', 'transcript', 'romanized'])
        writer.writerow([filename, transcript, romanized])

def main():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    recorded = get_recorded_transcripts()

    # Filter out already recorded sentences
    todo = [(np_text, roman) for np_text, roman in NEW_SENTENCES
            if np_text not in recorded]

    if not todo:
        print("✅ All sentences already recorded!")
        return

    total_existing = len(list(AUDIO_DIR.glob("NP_*.wav")))
    print(f"\n{'='*55}")
    print(f"  🇳🇵 Nepali Voice AI — Phase 4 Recording Session")
    print(f"{'='*55}")
    print(f"  Already recorded : {total_existing} samples")
    print(f"  New to record    : {len(todo)} sentences")
    print(f"  Session batch    : {min(BATCH_SIZE, len(todo))} sentences")
    print(f"{'='*55}")
    print("  Instructions:")
    print("  • Read the Nepali sentence aloud clearly")
    print("  • Press Enter to START recording")
    print("  • Press Enter again to STOP")
    print("  • Type 's' + Enter to SKIP a sentence")
    print("  • Type 'q' + Enter to QUIT and save progress")
    print(f"{'='*55}\n")

    session_count = 0
    batch = todo[:BATCH_SIZE]

    for i, (nepali, roman) in enumerate(batch):
        filename, num = get_next_filename()

        print(f"  [{i+1}/{len(batch)}] {filename}")
        print(f"  🇳🇵  {nepali}")
        print(f"  📖  {roman}")
        print()

        action = input("  Press Enter to record (s=skip, q=quit): ").strip().lower()

        if action == 'q':
            print("\n✅ Session saved. Great work!")
            break
        elif action == 's':
            print("  ⏭  Skipped\n")
            continue

        audio = record_audio()

        if audio is None or len(audio) < SAMPLE_RATE * 0.3:
            print("  ⚠️  Too short, skipping\n")
            continue

        save_audio(audio, filename)
        append_metadata(filename, nepali, roman)
        session_count += 1

        duration = len(audio) / SAMPLE_RATE
        print(f"  ✅ Saved! ({duration:.1f}s)\n")

    total_now = len(list(AUDIO_DIR.glob("NP_*.wav")))
    print(f"\n{'='*55}")
    print(f"  Session complete!")
    print(f"  Recorded this session : {session_count}")
    print(f"  Total samples now     : {total_now}")
    print(f"  Target                : 500")
    print(f"  Remaining             : {max(0, 500 - total_now)}")
    print(f"{'='*55}\n")

if __name__ == "__main__":
    main()
