class ExplainableATS:

    @staticmethod
    def generate_feedback(ats_result, section_result):

        feedback = []

        ####################################################
        # Skill Match
        ####################################################

        if ats_result["Skill Match"] >= 90:

            feedback.append(
                "Excellent skill match with the Job Description."
            )

        elif ats_result["Skill Match"] >= 70:

            feedback.append(
                "Good skill match. A few important skills are still missing."
            )

        else:

            feedback.append(
                "Your resume is missing several important skills required by the job."
            )

        ####################################################
        # Semantic Similarity
        ####################################################

        if ats_result["Semantic Similarity"] >= 80:

            feedback.append(
                "Resume content is highly relevant to the Job Description."
            )

        elif ats_result["Semantic Similarity"] >= 60:

            feedback.append(
                "Resume is moderately aligned with the Job Description."
            )

        else:

            feedback.append(
                "Resume content is not sufficiently aligned with the Job Description."
            )

        ####################################################
        # Resume Completeness
        ####################################################

        if ats_result["Resume Completeness"] >= 90:

            feedback.append(
                "Resume structure is excellent."
            )

        elif ats_result["Resume Completeness"] >= 70:

            feedback.append(
                "Resume is mostly complete but can be improved."
            )

        else:

            feedback.append(
                "Resume is missing several important sections."
            )

        ####################################################
        # Missing Skills
        ####################################################

        if len(ats_result["Missing Skills"]) > 0:

            feedback.append(

                "Missing Skills: "

                + ", ".join(

                    ats_result["Missing Skills"]

                )

            )

        ####################################################
        # Missing Sections
        ####################################################

        if len(section_result["Missing Sections"]) > 0:

            feedback.append(

                "Missing Resume Sections: "

                + ", ".join(

                    section_result["Missing Sections"]

                )

            )

        return feedback