from src.parser import ResumeParser

from src.information_extractor import (
    extract_name,
    extract_email,
    extract_phone,
    extract_linkedin,
    extract_github
)

from src.skill_extractor import extract_skills


class ResumeAnalyzer:

    @staticmethod
    def analyze(file_path):

        text = ResumeParser.extract_text(file_path)

        return {

            "Name": extract_name(text),

            "Email": extract_email(text),

            "Phone": extract_phone(text),

            "LinkedIn": extract_linkedin(text),

            "GitHub": extract_github(text),

            "Skills": extract_skills(text),   # <-- THIS LINE MUST BE PRESENT

            "Resume Length": len(text.split()),

            "Raw Text": text
        }