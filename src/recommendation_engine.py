class RecommendationEngine:

    @staticmethod
    def missing_skills(resume_skills, jd_skills):

        resume_set = set(skill.lower() for skill in resume_skills)
        jd_set = set(skill.lower() for skill in jd_skills)

        missing = sorted(list(jd_set - resume_set))

        return [skill.title() for skill in missing]


    @staticmethod
    def matched_skills(resume_skills, jd_skills):

        resume_set = set(skill.lower() for skill in resume_skills)
        jd_set = set(skill.lower() for skill in jd_skills)

        matched = sorted(list(jd_set & resume_set))

        return [skill.title() for skill in matched]


    @staticmethod
    def generate_suggestions(
        ats_score,
        missing_skills,
        resume_length
    ):

        suggestions = []

        if ats_score < 85:

            suggestions.append(
                "Improve your ATS score by aligning your resume with the job description."
            )

        if len(missing_skills) > 0:

            suggestions.append(
                "Add projects or experience demonstrating: "
                + ", ".join(missing_skills)
            )

        if resume_length < 350:

            suggestions.append(
                "Your resume is relatively short. Add more measurable achievements and project details."
            )

        if len(missing_skills) == 0:

            suggestions.append(
                "Excellent! Your technical skills closely match the job description."
            )

        suggestions.append(
            "Quantify your achievements (e.g., 'Improved model accuracy by 15%' or 'Reduced processing time by 30%')."
        )

        suggestions.append(
            "Use action verbs such as Developed, Built, Designed, Implemented, Optimized, and Automated."
        )

        return suggestions