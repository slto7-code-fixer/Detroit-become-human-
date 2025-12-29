import re
from pathlib import Path

INPUT_FILE = "script-ar-raw.md"
OUTPUT_FILE = "structured-script.md"

def clean_line(line: str) -> str:
    garbage = [
        "Skip to main content",
        "Next chapter",
        "Next Connor chapter",
        "Contents",
        "Credits",
        "●"
    ]
    for g in garbage:
        line = line.replace(g, "")
    return line.strip()

def is_speaker_line(line: str) -> bool:
    return bool(re.match(r"^[A-Z][A-Za-z ]+$", line))

def is_choice(line: str) -> bool:
    return line.startswith("[") or "Leads to" in line or "Probability" in line

def main():
    raw = Path(INPUT_FILE).read_text(encoding="utf-8").splitlines()

    out = []
    out.append("# Detroit: Become Human — النص العربي المنظم\n")
    out.append("## صيغة مهيأة لمحاكاة الذكاء الاصطناعي\n")
    out.append("---\n")

    current_speaker = None

    for line in raw:
        line = clean_line(line)
        if not line:
            continue

        # فصل
        if re.match(r"^\d+\s*-\s*.*", line):
            out.append(f"\n# الفصل: {line}\n")
            continue

        # عنوان مشهد
        if line.isupper() and len(line) < 50:
            out.append(f"\n## المشهد: {line}\n")
            continue

        # اسم متحدث
        if is_speaker_line(line):
            current_speaker = line
            out.append(f"\n**{current_speaker}:**")
            continue

        # خيارات
        if is_choice(line):
            out.append(f"\n> **خيار / نتيجة:** {line}")
            continue

        # حوار
        if current_speaker:
            out.append(f"{line}")
        else:
            out.append(f"*{line}*")

    Path(OUTPUT_FILE).write_text("\n".join(out), encoding="utf-8")
    print("✔ تم إنشاء structured-script.md بنجاح")

if __name__ == "__main__":
    main()
