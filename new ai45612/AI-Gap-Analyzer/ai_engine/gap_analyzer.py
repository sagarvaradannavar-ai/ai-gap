
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("career_data.json")

with open(DATA_FILE, "r", encoding="utf-8") as file:
    CAREER_DATA = json.load(file)


def analyze_gap(user_skills, career):

    if career not in CAREER_DATA:
        return {"error": "Career not found."}

    required_skills = CAREER_DATA[career]

    matched = [
        skill for skill in required_skills
        if skill in user_skills
    ]

    missing = [
        skill for skill in required_skills
        if skill not in user_skills
    ]

    percentage = round(
        len(matched) / len(required_skills) * 100
    )

    return {
        "career": career,
        "match_percentage": percentage,
        "matched_skills": matched,
        "missing_skills": missing,
        "total_required_skills": len(required_skills)
    }
