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


EXTRA_SENTENCES = [
    ("मेरो नाम गयानेन्द्र हो", "mero naam gyanendra ho"),
    ("म नेपालमा बस्छु", "ma nepalma baschhu"),
    ("नेपाल मेरो देश हो", "nepal mero desh ho"),
    ("मलाई नेपाली खाना मन पर्छ", "malai nepali khana man parchha"),
    ("आज मौसम राम्रो छ", "aaja mausam ramro chha"),
    ("भोलि पानी पर्छ", "bholi paani parchha"),
    ("खाना खाने समय भयो", "khana khaane samay bhayo"),
    ("चिया पिउनु छ", "chiya piunu chha"),
    ("पानी ल्याउनुहोस्", "paani lyaaunuhos"),
    ("ढोका बन्द गर्नुहोस्", "dhoka band garnuhos"),
    ("बत्ती बाल्नुहोस्", "batti baalunhos"),
    ("झ्याल खोल्नुहोस्", "jhyal kholnuhos"),
    ("मलाई मद्दत गर्नुहोस्", "malai maddat garnuhos"),
    ("यो ठाउँ कहाँ हो", "yo thaau kahaa ho"),
    ("अस्पताल नजिकै छ", "aspatal najikai chha"),
    ("विद्यालय टाढा छ", "vidyalay taadha chha"),
    ("मूल्य कति हो", "mulya kati ho"),
    ("यो किन्नु छ", "yo kinnu chha"),
    ("पैसा छैन", "paisa chhaina"),
    ("सस्तो छ", "sasto chha"),
    ("महँगो छ", "mahango chha"),
    ("एक किलो चाहियो", "ek kilo chaahiyo"),
    ("दुई लिटर दूध दिनुहोस्", "dui liitar dudh dinuhos"),
    ("तरकारी ताजा छ", "tarkari taaja chha"),
    ("फलफूल मीठो छ", "phalphul meetho chha"),
    ("भात पाक्यो", "bhaat paakyo"),
    ("दाल तयार छ", "daal tayaar chha"),
    ("रोटी बनाउनुहोस्", "roti banaaunuhos"),
    ("तिखो छ", "tikho chha"),
    ("नुन थप्नुहोस्", "nun thapnuhos"),
    ("मेरो घर काठमाडौंमा छ", "mero ghar kathmadauma chha"),
    ("पोखरा सुन्दर शहर हो", "pokhara sundar shahar ho"),
    ("लुम्बिनी बुद्धको जन्मस्थल हो", "lumbini buddhako janmasthala ho"),
    ("एभरेस्ट संसारकै अग्लो हो", "everest sansarakai aglo ho"),
    ("नेपालमा धेरै पहाड छन्", "nepalma dherai pahad chhan"),
    ("हिमालय सुन्दर छ", "himalay sundar chha"),
    ("आकाश निलो छ", "aakaash nilo chha"),
    ("बादल आयो", "baadal aayo"),
    ("घाम लाग्यो", "ghaam laagyo"),
    ("हावा चल्यो", "haawa chalyo"),
    ("हिउँ पर्यो", "hiun paryo"),
    ("पानी परिरहेको छ", "paani parirahaeko chha"),
    ("राम्रो दृश्य छ", "ramro drishya chha"),
    ("फोटो खिच्नुहोस्", "photo khichnuhos"),
    ("मेरो फोन हराएको छ", "mero phone haraeko chha"),
    ("ब्याट्री सकियो", "byaatri sakiyo"),
    ("चार्ज गर्नुहोस्", "charge garnuhos"),
    ("इन्टरनेट ढिलो छ", "internet dhilo chha"),
    ("वाइफाइ छैन", "wifi chhaina"),
    ("कम्प्युटर बिग्रियो", "computer bigryo"),
    ("इमेल आयो", "email aayo"),
    ("कल गर्नुहोस्", "call garnuhos"),
    ("नेटवर्क छैन", "network chhaina"),
    ("पासवर्ड बिर्सिएँ", "password birsien"),
    ("मेरो उमेर तीस वर्ष हो", "mero umar tees barsha ho"),
    ("परिवारमा पाँच जना छन्", "parivaarma paach jana chhan"),
    ("बुवा काम गर्नुहुन्छ", "buwa kaam garnuhunchha"),
    ("आमा घरमा हुनुहुन्छ", "aama gharma hunuhunchha"),
    ("मेरो साथी राम्रो छ", "mero saathi ramro chha"),
    ("हामी सँगै पढ्छौं", "haami sangai padhchhau"),
    ("शिक्षक राम्रो पढाउनुहुन्छ", "shikshak ramro padhaaunuhunchha"),
    ("परीक्षा गाह्रो थियो", "pareeksha gaahro thiyo"),
    ("नतिजा राम्रो आयो", "natija ramro aayo"),
    ("पुस्तक पढ्नु राम्रो हो", "pustak padhnuu ramro ho"),
    ("ज्ञान शक्ति हो", "gyaan shakti ho"),
    ("मेरो काम राम्रो छ", "mero kaam ramro chha"),
    ("बैठक बिहान छ", "baithak bihaan chha"),
    ("समयमा आउनुहोस्", "samayama aaunuhos"),
    ("काम सकियो", "kaam sakiyo"),
    ("थकान लाग्यो", "thakaan laagyo"),
    ("आराम गर्नुहोस्", "aaraam garnuhos"),
    ("डाक्टरकहाँ जानुपर्छ", "daaktarkahaa jaanuparchha"),
    ("औषधि खानुहोस्", "aushadhi khaanuhos"),
    ("ज्वरो आयो", "jwaro aayo"),
    ("खोकी लाग्यो", "khoki laagyo"),
    ("पेट दुख्यो", "pet dukhyo"),
    ("दाँत दुख्यो", "daant dukhyo"),
    ("व्यायाम गर्नुहोस्", "vyaayam garnuhos"),
    ("पानी धेरै पिउनुहोस्", "paani dherai piunuhos"),
    ("व्यस्त छु", "byasta chhu"),
    ("फुर्सद छैन", "phursad chhaina"),
    ("पछि कुरा गरौं", "pachhi kuraa garaun"),
    ("अहिले जान्छु", "ahile jaanchhu"),
    ("भेटौंला", "bhetaula"),
    ("माफ गर्नुहोस्", "maaf garnuhos"),
    ("स्वागत छ", "swaagat chha"),
    ("खुसी भएँ", "khusi bhaen"),
    ("राम्रो लाग्यो", "ramro laagyo"),
    ("गाह्रो छ", "gaahro chha"),
    ("सजिलो छ", "sajilo chha"),
    ("बुझिनँ", "bujhinan"),
    ("फेरि भन्नुहोस्", "pheri bhanunuhos"),
    ("बिस्तारै बोल्नुहोस्", "bistarai bolnuhos"),
    ("गीत गाउँछु", "geet gaunchhu"),
    ("संगीत सुन्छु", "sangeet sunchu"),
    ("फुटबल मन पर्छ", "football man parchha"),
    ("दौडन मन लाग्छ", "dauddana man laagchha"),
    ("पहाड चढ्न मन लाग्छ", "pahaad chadhna man laagchha"),
    ("प्रकृति सुन्दर छ", "prakriti sundar chha"),
    ("सगरमाथा हाम्रो गर्व हो", "sagarmatha haamro garva ho"),
    ("नेपाली संस्कृति अनोखो छ", "nepali sanskriti anokho chha"),
    ("दशैं ठूलो चाड हो", "dashain thulo chaad ho"),
    ("तिहार उज्यालोको चाड हो", "tihar ujyaaloko chaad ho"),
    ("मेरो सपना ठूलो छ", "mero sapana thulo chha"),
    ("नेपाल विकास गर्नुपर्छ", "nepal bikaas garnuparchha"),
    ("इमानदारी महत्त्वपूर्ण छ", "imaanaadaari mahattwapurna chha"),
    ("देश प्रेम गर्नुपर्छ", "desh prem garnuparchha"),
    ("मिलेर काम गरौं", "milera kaam garaun"),
    ("प्रकृति जोगाउनुपर्छ", "prakriti jogaunuparchha"),
    ("वातावरण सफा राख्नुपर्छ", "waataawaran saphaa raakhnuparchha"),
    ("बिजुली बचत गर्नुहोस्", "bijuli bachat garnuhos"),
    ("खेतीपाती महत्त्वपूर्ण छ", "khetipati mahattwapurna chha"),
    ("किसानले मेहनत गर्छन्", "kisaanle mehnat garchhan"),
    ("रातो रंग मन पर्छ", "raato rang man parchha"),
    ("हरियो रंग प्रकृतिको हो", "hariyo rang prakritiko ho"),
    ("सुन पहेंलो हुन्छ", "sun pahelo huncha"),
    ("फलाम बलियो हुन्छ", "phalaama baliyo huncha"),
    ("दौरासुरुवाल राष्ट्रिय पोशाक हो", "daurasuruwal raashtriya poshaak ho"),
    ("टोपी लगाउनुहोस्", "topi lagaunuhos"),
    ("छाता लिनुहोस्", "chhata linuhos"),
    ("यो बाटो सहि हो", "yo baato sahi ho"),
    ("बायाँ मोड्नुहोस्", "bayan modnuhos"),
    ("दायाँ जानुहोस्", "daayaa jaanuhos"),
    ("सीधा जानुहोस्", "sidhaa jaanuhos"),
    ("गाडी ढिलो चलाउनुहोस्", "gaadi dhilo chalaaunuhos"),
    ("ट्राफिक जाम छ", "traffic jam chha"),
    ("बस कहिले आउँछ", "bus kahile aunchha"),
    ("भाडा कति लाग्छ", "bhaadaa kati laagchha"),
    ("विमानस्थल टाढा छ", "wimaansthala taadha chha"),
    ("पासपोर्ट देखाउनुहोस्", "passport dekhaunuhos"),
    ("होटल बुकिंग गरेको छ", "hotel booking gareko chha"),
    ("कोठा खाली छ", "kotha khaali chha"),
    ("बिहानको खाना समावेश छ", "bihaanko khaana samaabesh chha"),
    ("जीवन सुन्दर छ", "jeevan sundar chha"),
    ("आशा नछोड्नुहोस्", "aasha nachhordnuhos"),
    ("मेहनत गर्नुहोस्", "mehnat garnuhos"),
    ("सफलता आउँछ", "saphalata aunchha"),
    ("हार नमान्नुहोस्", "haar namaannuhos"),
    ("अगाडि बढ्नुहोस्", "agaadi badhunuhos"),
    ("नेपाल जिन्दाबाद", "nepal zindabaad"),
    ("जय नेपाल", "jaya nepal"),
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

    stream = sd.InputStream(device=1, samplerate=SAMPLE_RATE, channels=CHANNELS,
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
    ALL_SENTENCES = NEW_SENTENCES + EXTRA_SENTENCES
    todo = [(np_text, roman) for np_text, roman in ALL_SENTENCES
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
