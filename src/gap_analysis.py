class GapAnalyzer:

    @staticmethod
    def analyze(
        ats_result,
        section_result,
        resume_result,
        jd_result
    ):

        report = {}

        ###################################################
        # Job Role
        ###################################################

        report["Job Role"] = jd_result["Job Title"]

        ###################################################
        # ATS
        ###################################################

        report["ATS Score"] = ats_result["Final ATS Score"]

        ###################################################
        # Skills
        ###################################################

        report["Matched Skills"] = ats_result["Matched Skills"]

        report["Missing Skills"] = ats_result["Missing Skills"]

        ###################################################
        # Experience
        ###################################################

        resume_years = 0

        report["Resume Experience"] = resume_years

        report["Required Experience"] = jd_result["Experience"]

        if resume_years >= jd_result["Experience"]:

            report["Experience Status"] = "Matched"

        elif jd_result["Experience"] <= 2:

            report["Experience Status"] = "Acceptable for Freshers"

        else:

            report["Experience Status"] = "Needs Improvement"

        ###################################################
        # Education
        ###################################################

        report["Resume Education"] = "Bachelor"

        report["Required Education"] = jd_result["Education"]

        if "Bachelor" in jd_result["Education"]:

            report["Education Status"] = "Matched"

        else:

            report["Education Status"] = "Check Requirements"

        ###################################################
        # Sections
        ###################################################

        report["Present Sections"] = []

        report["Missing Sections"] = []

        for section, status in section_result[
            "Detected Sections"
        ].items():

            if status:

                report["Present Sections"].append(section)

            else:

                report["Missing Sections"].append(section)

        ###################################################
        # Suggestions
        ###################################################

        suggestions = []

        for skill in ats_result["Missing Skills"]:

            suggestions.append(
                f"Add skill: {skill}"
            )

        for sec in report["Missing Sections"]:

            suggestions.append(
                f"Add section: {sec}"
            )

        if not resume_result.get("GitHub"):

            suggestions.append(
                "Add GitHub profile"
            )

        if not resume_result.get("LinkedIn"):

            suggestions.append(
                "Add LinkedIn profile"
            )

        report["Suggestions"] = suggestions

        ###################################################
        # Predicted ATS
        ###################################################

        predicted = ats_result["Final ATS Score"]

        predicted += len(
            ats_result["Missing Skills"]
        ) * 4

        predicted += len(
            report["Missing Sections"]
        ) * 2

        predicted = min(predicted,100)

        report["Estimated ATS"] = round(
            predicted,
            2
        )

        return report