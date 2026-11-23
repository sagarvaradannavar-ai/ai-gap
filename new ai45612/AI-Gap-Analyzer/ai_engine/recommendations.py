
def generate_recommendations(missing_skills):

    recommendations = []

    for skill in missing_skills:

        recommendations.append(
            "Start learning " + skill.title()
        )

    if not recommendations:

        recommendations.append(
            "Great job! Continue practising your existing skills."
        )

    return recommendations
