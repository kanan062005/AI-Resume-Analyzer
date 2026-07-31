from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


class PDFReport:

    @staticmethod
    def generate(
        filename,
        resume_result,
        jd_result,
        ats_result,
        section_result,
        gap,
        suggestions
    ):

        doc = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        story = []

        ####################################################
        # Title
        ####################################################

        story.append(
            Paragraph(
                "<b><font size=18>AI Resume Analyzer Report</font></b>",
                styles["Title"]
            )
        )

        story.append(Spacer(1,20))

        ####################################################
        # Candidate
        ####################################################

        story.append(
            Paragraph("<b>Candidate Information</b>",styles["Heading2"])
        )

        story.append(
            Paragraph(
                f"Name : {resume_result['Name']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Email : {resume_result['Email']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Phone : {resume_result['Phone']}",
                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1,15)
        )

        ####################################################
        # ATS
        ####################################################

        story.append(
            Paragraph("<b>ATS Results</b>",styles["Heading2"])
        )

        for key,value in ats_result.items():

            story.append(
                Paragraph(
                    f"{key} : {value}",
                    styles["BodyText"]
                )
            )

        story.append(
            Spacer(1,15)
        )

        ####################################################
        # Sections
        ####################################################

        story.append(
            Paragraph("<b>Resume Sections</b>",styles["Heading2"])
        )

        for key,value in section_result["Detected Sections"].items():

            story.append(
                Paragraph(
                    f"{key} : {value}",
                    styles["BodyText"]
                )
            )

        story.append(
            Spacer(1,15)
        )

        ####################################################
        # Gap Analysis
        ####################################################

        story.append(
            Paragraph("<b>Gap Analysis</b>",styles["Heading2"])
        )

        for key,value in gap.items():

            story.append(
                Paragraph(
                    f"{key} : {value}",
                    styles["BodyText"]
                )
            )

        story.append(
            Spacer(1,15)
        )

        ####################################################
        # Suggestions
        ####################################################

        story.append(
            Paragraph("<b>Suggestions</b>",styles["Heading2"])
        )

        for item in suggestions:

            story.append(
                Paragraph(
                    f"• {item}",
                    styles["BodyText"]
                )
            )

        doc.build(story)