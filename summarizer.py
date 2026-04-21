from io import BytesIO
from pypdf import PdfReader

from llm_provider import get_llm


# ---------------- EXTRACT TEXT ----------------
def extract_text(file):
    file.seek(0)

    if file.name.endswith(".txt"):
        return file.read().decode("utf-8", errors="ignore")

    if file.name.endswith(".pdf"):
        pdf = PdfReader(BytesIO(file.read()))
        return "\n".join([p.extract_text() or "" for p in pdf.pages])

    return ""


# ---------------- SPLIT ----------------
def split_text(text, chunk_size=1000):
    words = text.split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]


# ---------------- CLEAN ----------------
def to_bullets(text):
    lines = text.split("\n")
    bullets = []
    seen = set()

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # ❌ remove unwanted phrases
        if any(x in line.lower() for x in [
            "here are", "key points", "summary", "following"
        ]):
            continue

        # clean bullet symbols
        if line.startswith(("-", "*", "•")):
            line = line[1:].strip()

        # skip very short noise
        if len(line.split()) < 5:
            continue

        # 🔥 deduplicate
        key = line.lower()
        if key in seen:
            continue
        seen.add(key)

        bullets.append(f"- {line}")

    return "\n".join(bullets[:6]) if bullets else "- No clear insights found."


# ---------------- MAIN ----------------
def summarize_uploaded_file(file):
    text = extract_text(file)

    if not text or len(text.strip()) < 20:
        return "⚠️ No meaningful content found."

    llm = get_llm()

    chunks = split_text(text)

    outputs = []

    for chunk in chunks[:5]:  # limit for speed
        prompt = f"""
You are an expert sustainability analyst.

Extract ONLY key insights.

Rules:
- Output bullet points ONLY
- No headings or intro text
- Focus on:
  * energy inefficiencies
  * abnormal usage
  * recommendations
  * cost or optimization opportunities

Text:
{chunk}
"""
        try:
            result = llm.invoke(prompt).content
            outputs.append(result)
        except:
            continue

    combined = "\n".join(outputs)

    return to_bullets(combined)