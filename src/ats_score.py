from src.section_analyzer import ResumeSectionAnalyzer
import re
from src.weighted_skill_matcher import WeightedSkillMatcher


def normalize_similarity(score):
    score = float(score)

    if score < 30:
        return 30

    if score > 85:
        return 100

    normalized = ((score - 30) / 55) * 70 + 30

    return round(min(max(normalized, 30), 100), 2)


class ATSScorer:

    @staticmethod
    def calculate_experience_score(resume_years, required_years):
        # Fresher-friendly scoring
        if required_years <= 2:
            return 100

        if resume_years >= required_years:
            return 100

        if required_years == 0:
            return 100

        return round((resume_years / required_years) * 100, 2)

    @staticmethod
    def calculate_education_score(resume_education, jd_education):
        if len(jd_education) == 0:
            return 100

        resume = [x.lower() for x in resume_education]

        for degree in jd_education:
            if degree.lower() in resume:
                return 100

        return 50

    @staticmethod
    def calculate_project_score(resume_text):
        text = resume_text.lower()

        keywords = [
            "project",
            "machine learning",
            "deep learning",
            "streamlit",
            "dashboard",
            "tableau",
            "power bi",
            "classification",
            "prediction",
            "nlp",
            "transformer",
        ]

        count = sum(
            1
            for word in keywords
            if word in text
        )

        return min(count * 15, 100)

    @staticmethod
    def calculate_certification_score(resume_text):
        certs = [
            "coursera",
            "udemy",
            "ibm",
            "google",
            "microsoft",
            "aws",
            "azure",
            "oracle",
            "nptel",
        ]

        text = resume_text.lower()

        count = 0

        for cert in certs:
            if cert in text:
                count += 1

        return min(count * 25, 100)

    @staticmethod
    def calculate_achievement_score(resume_text):
        text = resume_text.lower()

        keywords = [
            "%",
            "improved",
            "developed",
            "built",
            "implemented",
            "optimized",
            "accuracy",
            "reduced",
            "increased",
        ]

        score = sum(
            1
            for word in keywords
            if word in text
        )

        return min(score * 12, 100)

    @staticmethod
    def calculate_resume_completeness(result):
        score = 0

        if result.get("Name"):
            score += 15

        if result.get("Email"):
            score += 15

        if result.get("Phone"):
            score += 15

        if result.get("LinkedIn"):
            score += 15

        if result.get("GitHub"):
            score += 15

        if len(result.get("Skills", [])) >= 5:
            score += 15

        if result.get("Resume Length", 0) >= 350:
            score += 10

        return score

    @staticmethod
    def calculate_final_score(
        semantic_similarity,
        resume_skills,
        jd_skills,
        resume_years,
        jd_years,
        resume_education,
        jd_education,
        result,
    ):
        ####################################################
        # Normalize Semantic Similarity
        ####################################################
        semantic_similarity = normalize_similarity(
            semantic_similarity
        )

        ####################################################
        # Weighted Skill Matching
        ####################################################
        skill_result = WeightedSkillMatcher.match_skills(
            resume_skills,
            jd_skills
        )

        skill = skill_result["Skill Score"]

        ####################################################
        # Other Scores
        ####################################################
        experience = ATSScorer.calculate_experience_score(
            resume_years,
            jd_years
        )

        education = ATSScorer.calculate_education_score(
            resume_education,
            jd_education
        )

        resume_text = result.get("Raw Text", "")

        section_result = ResumeSectionAnalyzer.analyze(
            resume_text
        )

        section_score = section_result["Section Score"]

        project = ATSScorer.calculate_project_score(
            resume_text
        )

        certification = ATSScorer.calculate_certification_score(
            resume_text
        )

        achievement = ATSScorer.calculate_achievement_score(
            resume_text
        )

        basic = ATSScorer.calculate_resume_completeness(
            result
        )

        completeness = round(

            basic * 0.4 +

            section_score * 0.6,

            2

)

        ####################################################
        # Final ATS Formula (Fresher Optimized)
        ####################################################
        ats = (
            skill * 0.30 +
            semantic_similarity * 0.20 +
            experience * 0.05 +
            education * 0.10 +
            project * 0.15 +
            certification * 0.05 +
            achievement * 0.05 +
            completeness * 0.10
        )

        ####################################################
        # Return Scores
        ####################################################
        return {
            "Matched Skills": skill_result["Matched"],
            "Matched Skill Count": len(skill_result["Matched"]),
            "Missing Skills": skill_result["Missing"],
            "Skill Match": round(skill, 2),
            "Semantic Similarity": round(semantic_similarity, 2),
            "Experience Score": round(experience, 2),
            "Education Score": round(education, 2),
            "Project Score": round(project, 2),
            "Certification Score": round(certification, 2),
            "Achievement Score": round(achievement, 2),
            "Resume Completeness": round(completeness, 2),
            "Final ATS Score": round(ats, 2),
        }