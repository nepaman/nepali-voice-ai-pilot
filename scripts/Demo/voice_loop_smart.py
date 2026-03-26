def normalize(text: str) -> str:
    """हल्का normalization: space हटाउने, fullstop आदि हटाउने, Devanagari मा नै रहने।"""
    t = text.strip()
    for ch in ["।", ".", "!", "?", ","]:
        t = t.replace(ch, "")
    return t


def generate_smart_response(user_text: str):
    """
    Whisper ले नेपालीलाई प्रायः phonetic spelling मा लेख्ने भएकाले
    exact शब्द होइन, root pattern र common गल्तीहरू match गरिन्छ।
    """
    t = normalize(user_text)

    # --- GREETING: नमस्ते / नमस्कार ---
    # उदाहरण: "नास्ते", "नमस्", "नसते"
    greeting_keys = [
        "नमस्ते", "नमस्कार", "नमस्", "नास्ते", "नासते", "नास्टी",
    ]
    if any(k in t for k in greeting_keys):
        return "नमस्कार! तपाईंलाई भेटेर खुशी लाग्यो। म नेपाली भ्वाइस एआई हुँ।", "greeting"

    # --- MORNING: शुभ प्रभात / शुभ बिहानी ---
    # उदाहरण: "शुब प्रबात", "सु प्रबात", "शुब बिहानी"
    morning_keys = [
        "प्रभात", "प्रबात", "प्रबाद", "शुभप्रभात", "शुभ प्रभात",
        "बिहानी", "शुभ बिहानी", "शुब बिहानी", "सु प्रबात", "सुप्रभात",
    ]
    if any(k in t for k in morning_keys):
        return "शुभ प्रभात! आज तपाईंको दिन शुभ रहोस्।", "morning"

    # --- THANKS: धन्यवाद ---
    # Whisper output: "तन्ने बाद", "धन्यबाद"
    thanks_keys = [
        "धन्यवाद", "धन्यबाद", "धन्यबाद", "तन्ने बाद", "तन्यबाद", "तन्य बाद",
    ]
    if any(k in t for k in thanks_keys):
        return "तपाईंलाई पनि धन्यवाद! सधैं खुशी छु सहयोग गर्न।", "thanks"

    # --- GOODNIGHT: शुभ रात्रि ---
    # Whisper output: "सुबरात्री", "शुबरात्री", "शुबरा त्री", "सुबराति"
    goodnight_keys = [
        "शुभ रात्रि", "शुभरात्रि", "सुबरात्री", "सुबराति",
        "शुबरात्री", "शुबरा त्री", "सु ब्रात्री", "शुबराति",
        "रात्रि", "रात्री", "राति",
    ]
    if any(k in t for k in goodnight_keys):
        return "शुभ रात्रि! राम्रोसँग सुत्नुहोस्।", "goodnight"

    # --- HOW ARE YOU: कस्तो छ ---
    # Whisper output: "कोस्तु साद", "कोस्त सा", "कोस्तु छ"
    howru_keys = [
        "कस्तो छ", "कस्तो हुनुहुन्छ", "के छ", "खबर",  # general "कस्तो"/"के छ" हरु
        "कोस्तु साद", "कोस्तु सा", "कोस्तो सा", "कोस्तु छ", "कोस्त्छा", "कोस्तु चा",
    ]
    if any(k in t for k in howru_keys):
        return "म ठीक छु, धन्यवाद! तपाईं कस्तो हुनुहुन्छ?", "howru"

    # Default
    return f"तपाईंले भन्नुभयो: {user_text}। म अझै सिक्दैछु!", "default"
