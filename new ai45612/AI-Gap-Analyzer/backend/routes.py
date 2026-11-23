
from flask import Blueprint, request, jsonify

from backend.resume_parser import extract_pdf_text
from ai_engine.skill_extractor import extract_skills
from ai_engine.gap_analyzer import analyze_gap
from ai_engine.recommendations import generate_recommendations

api = Blueprint("api", __name__)


@api.route("/analyze-career", methods=["POST"])
def analyze_career():

    career = request.form.get("career", "").strip()
    manual_skills = request.form.get("skills", "")

    resume = request.files.get("resume")

    if not career:
        return jsonify({"error": "Please select a career."}), 400

    resume_text = ""

    if resume and resume.filename:

        if not resume.filename.lower().endswith(".pdf"):
            return jsonify({"error": "Only PDF files are allowed."}), 400

        try:
            resume_text = extract_pdf_text(resume.read())

        except Exception:
            return jsonify({
                "error": "Unable to read your PDF. Please try another PDF."
            }), 400

    combined_text = manual_skills + " " + resume_text

    if not combined_text.strip():
        return jsonify({
            "error": "Please upload a resume or enter your skills."
        }), 400

    user_skills = extract_skills(combined_text)

    result = analyze_gap(user_skills, career)

    if "error" in result:
        return jsonify(result), 400

    result["recommendations"] = generate_recommendations(
        result["missing_skills"]
    )

    result["detected_skills"] = user_skills

    return jsonify(result)

