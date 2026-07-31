import re


class ResumeSectionAnalyzer:

    SECTIONS = {

        "Summary": [
            "summary",
            "professional summary",
            "career objective",
            "objective",
            "profile"
        ],

        "Skills": [
            "skills",
            "technical skills",
            "core competencies"
        ],

        "Experience": [
            "experience",
            "work experience",
            "employment",
            "internship"
        ],

        "Projects": [
            "projects",
            "academic projects",
            "personal projects"
        ],

        "Education": [
            "education",
            "academic qualification",
            "qualification"
        ],

        "Certifications": [
            "certifications",
            "certificates",
            "courses"
        ],

        "Achievements": [
            "achievements",
            "awards",
            "accomplishments"
        ],

        "Languages": [
            "languages",
            "language proficiency"
        ]
    }

    @staticmethod
    def detect_sections(text):

        text = text.lower()

        detected = {}

        for section, keywords in ResumeSectionAnalyzer.SECTIONS.items():

            found = False

            for keyword in keywords:

                pattern = r"\b" + re.escape(keyword) + r"\b"

                if re.search(pattern, text):

                    found = True
                    break

            detected[section] = found

        return detected

    @staticmethod
    def calculate_section_score(detected):

        total = len(detected)

        present = sum(detected.values())

        return round((present / total) * 100, 2)

    @staticmethod
    def missing_sections(detected):

        return [

            section

            for section, exists in detected.items()

            if not exists

        ]

    @staticmethod
    def analyze(text):

        detected = ResumeSectionAnalyzer.detect_sections(text)

        score = ResumeSectionAnalyzer.calculate_section_score(
            detected
        )

        missing = ResumeSectionAnalyzer.missing_sections(
            detected
        )

        return {

            "Detected Sections": detected,

            "Section Score": score,

            "Missing Sections": missing

        }