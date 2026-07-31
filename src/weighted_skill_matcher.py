from rapidfuzz import fuzz


class WeightedSkillMatcher:

    @staticmethod
    def match_skills(
        resume_skills,
        jd_skills,
        threshold=80
    ):
        """
        Fuzzy match resume skills with JD skills.

        Returns:
            Matched skills
            Missing skills
            Weighted skill score
        """

        # Handle empty JD skills
        if not jd_skills:
            return {
                "Matched": [],
                "Missing": [],
                "Skill Score": 100
            }

        weights = {}

        for i, skill in enumerate(jd_skills):

            if i < 3:
                weights[skill] = 3

            elif i < 6:
                weights[skill] = 2

            else:
                weights[skill] = 1

        matched = []
        missing = []

        obtained_weight = 0
        total_weight = sum(weights.values())

        for jd_skill in jd_skills:

            found = False

            for resume_skill in resume_skills:

                similarity = fuzz.ratio(
                    jd_skill.lower(),
                    resume_skill.lower()
                )

                if similarity >= threshold:

                    matched.append({
                        "JD Skill": jd_skill,
                        "Resume Skill": resume_skill,
                        "Similarity": similarity
                    })

                    obtained_weight += weights[jd_skill]
                    found = True
                    break

            if not found:
                missing.append(jd_skill)

        # Prevent division by zero
        if total_weight == 0:
            score = 100
        else:
            score = round(
                (obtained_weight / total_weight) * 100,
                2
            )

        return {
            "Matched": matched,
            "Missing": missing,
            "Skill Score": score
        }