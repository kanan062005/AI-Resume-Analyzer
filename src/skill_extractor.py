import re

from src.skill_database import SKILLS


def extract_skills(text):

    text = text.lower()

    extracted = set()

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):

            extracted.add(skill.title())

    return sorted(list(extracted))