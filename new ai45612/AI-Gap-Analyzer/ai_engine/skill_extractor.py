
import json
import re
from pathlib import Path

DATA_FILE = Path(__file__).with_name("career_data.json")

with open(DATA_FILE, "r", encoding="utf-8") as file:
    CAREER_DATA = json.load(file)

ALL_SKILLS = sorted(
    set(
        skill
        for skills in CAREER_DATA.values()
        for skill in skills
    ),
    key=len,
    reverse=True
)


def extract_skills(text):

    text = text.lower()

    detected = []

    for skill in ALL_SKILLS:

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(skill.lower())
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, text):
            detected.append(skill)

    return detected
