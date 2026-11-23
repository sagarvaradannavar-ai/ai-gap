
def clean_text(text):

    if not text:
        return ""

    return " ".join(text.lower().split())


def format_skill(skill):

    return skill.strip().title()



