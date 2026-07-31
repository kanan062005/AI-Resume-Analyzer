class ResumeImprover:

    @staticmethod
    def generate_suggestions(
        ats_result,
        section_result,
        resume_result,
        jd_result
    ):

        suggestions = []

        ####################################################
        # Missing Skills
        ####################################################

        if ats_result["Missing Skills"]:

            suggestions.append(

                "Add these missing skills: "

                + ", ".join(ats_result["Missing Skills"])

            )

        ####################################################
        # Missing Sections
        ####################################################

        for section in section_result["Missing Sections"]:

            suggestions.append(

                f"Add a '{section}' section to your resume."

            )

        ####################################################
        # LinkedIn
        ####################################################

        if not resume_result.get("LinkedIn"):

            suggestions.append(

                "Add your LinkedIn profile."

            )

        ####################################################
        # GitHub
        ####################################################

        if not resume_result.get("GitHub"):

            suggestions.append(

                "Add your GitHub profile."

            )

        ####################################################
        # Resume Length
        ####################################################

        if resume_result["Resume Length"] < 350:

            suggestions.append(

                "Expand your resume by adding more projects or achievements."

            )

        ####################################################
        # Certifications
        ####################################################

        raw = resume_result["Raw Text"].lower()

        cert_words = [

            "coursera",

            "udemy",

            "google",

            "ibm",

            "microsoft",

            "aws",

            "oracle",

            "azure"

        ]

        found = any(

            word in raw

            for word in cert_words

        )

        if not found:

            suggestions.append(

                "Include relevant certifications (Google, IBM, Microsoft, Coursera, AWS, etc.)."

            )

        ####################################################
        # Achievements
        ####################################################

        achievement_words = [

            "accuracy",

            "%",

            "improved",

            "optimized",

            "reduced",

            "increased"

        ]

        count = sum(

            word in raw

            for word in achievement_words

        )

        if count < 2:

            suggestions.append(

                "Quantify your impact using numbers, percentages or measurable achievements."

            )

        ####################################################
        # Summary
        ####################################################

        if not section_result["Detected Sections"]["Summary"]:

            suggestions.append(

                "Add a Professional Summary tailored to the job role."

            )

        return suggestions