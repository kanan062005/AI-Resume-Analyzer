import re
from src.skill_database import SKILLS


class JobDescriptionParser:

    @staticmethod
    def extract_skills(text):
        """
        Extract skills mentioned in the Job Description.
        """
        text = text.lower()
        skills = []

        for skill in SKILLS:
            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, text):
                skills.append(skill.title())

        return sorted(list(set(skills)))

    @staticmethod
    def extract_experience(text):
        """
        Extract required years of experience.
        Example:
        '2+ years' -> 2
        """
        pattern = r'(\d+)\+?\s*(?:years|year)'

        match = re.search(pattern, text.lower())

        if match:
            return int(match.group(1))

        return 0

    @staticmethod
    def extract_education(text):
        """
        Extract education requirements.
        """
        education = []

        degrees = [
            "b.tech",
            "b.e",
            "bachelor",
            "master",
            "m.tech",
            "mba",
            "phd"
        ]

        text = text.lower()

        for degree in degrees:
            if degree in text:
                education.append(degree.title())

        return education

    @staticmethod
    def extract_job_title(text):
        """
        Detect the job title from the Job Description.
        """

        titles = [
            "data scientist",
            "data analyst",
            "machine learning engineer",
            "software engineer",
            "python developer",
            "ai engineer",
            "business analyst",
            "data engineer",
            "backend developer",
            "frontend developer",
            "full stack developer"
        ]

        text = text.lower()

        for title in titles:
            if title in text:
                return title.title()

        return "Unknown"

    @staticmethod
    def analyze(text):
        """
        Analyze the complete Job Description.
        """

        return {

            "Job Title": JobDescriptionParser.extract_job_title(text),

            "Skills": JobDescriptionParser.extract_skills(text),

            "Experience": JobDescriptionParser.extract_experience(text),

            "Education": JobDescriptionParser.extract_education(text)
        }