def analyze_text(text):
    if not text.strip():
        return "Suspicious"

    keywords = ["name", "university", "degree", "certified", "registration"]
    match_count = sum(1 for word in keywords if word.lower() in text.lower())

    if match_count >= 4:
        return "Authentic"
    elif match_count == 3:
        return "Suspicious"
    else:
        return "Forged"
