import os
import streamlit as st
import plotly.graph_objects as go


from src.resume_analyzer import ResumeAnalyzer
from src.jd_parser import JobDescriptionParser
from src.similarity import ResumeMatcher
from src.ats_score import ATSScorer
from src.section_analyzer import ResumeSectionAnalyzer
from src.resume_improver import ResumeImprover
from src.gap_analysis import GapAnalyzer
from src.pdf_report import PDFReport
from src.bullet_rewriter import BulletRewriter



st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)


st.title("🤖 AI Resume Analyzer")

st.markdown(
    "Upload your resume and paste the Job Description to calculate your ATS score."
)



uploaded_resume = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)


jd = st.text_area(
    "Paste Job Description",
    height=250
)



resume_path = None



if uploaded_resume:

    os.makedirs(
        "uploads",
        exist_ok=True
    )


    resume_path = os.path.join(
        "uploads",
        uploaded_resume.name
    )


    with open(resume_path, "wb") as f:

        f.write(
            uploaded_resume.read()
        )



if st.button("Analyze Resume"):


    if uploaded_resume is None:

        st.error(
            "Please upload a resume."
        )


    elif jd.strip() == "":

        st.error(
            "Please paste a Job Description."
        )


    else:


        with st.spinner(
            "Analyzing Resume..."
        ):


            resume_result = ResumeAnalyzer.analyze(
                resume_path
            )


            jd_result = JobDescriptionParser.analyze(
                jd
            )


            matcher = ResumeMatcher()


            similarity = matcher.calculate_similarity(
                resume_result["Raw Text"],
                jd
            )


            section_result = ResumeSectionAnalyzer.analyze(
                resume_result["Raw Text"]
            )



            ats_result = ATSScorer.calculate_final_score(

                semantic_similarity=similarity,

                resume_skills=resume_result["Skills"],

                jd_skills=jd_result["Skills"],

                resume_years=0,

                jd_years=jd_result["Experience"],

                resume_education=["Bachelor"],

                jd_education=jd_result["Education"],

                result=resume_result
            )



            suggestions = ResumeImprover.generate_suggestions(

                ats_result,

                section_result,

                resume_result,

                jd_result
            )



            rewritten_bullets = BulletRewriter.rewrite(

                resume_result["Raw Text"]

            )



            gap = GapAnalyzer.analyze(

                ats_result,

                section_result,

                resume_result,

                jd_result

            )



            PDFReport.generate(

                filename="ATS_Report.pdf",

                resume_result=resume_result,

                jd_result=jd_result,

                ats_result=ats_result,

                section_result=section_result,

                gap=gap,

                suggestions=suggestions

            )


        st.success(
            "Analysis Completed Successfully!"
        )
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
            [
                "📊 Dashboard",
                "🧠 Skills",
                "📄 Sections",
                "🎯 Gap Analysis",
                "📑 Reports",
                "✨ AI Rewriter"
            ]
        )



        # ================= Dashboard ================= #

        with tab1:


            st.write("Resume Skills:", resume_result["Skills"])
            st.write("JD Skills:", jd_result["Skills"])
            score = ats_result["Final ATS Score"]



            if score >= 85:

                st.success(
                    f"ATS Score : {score}%"
                )


            elif score >= 70:

                st.warning(
                    f"ATS Score : {score}%"
                )


            else:

                st.error(
                    f"ATS Score : {score}%"
                )



            # -------- ATS Gauge -------- #

            fig = go.Figure(

                go.Indicator(

                    mode="gauge+number",

                    value=score,

                    title={
                        "text": "ATS Score"
                    },


                    gauge={

                        "axis": {
                            "range": [0,100]
                        },


                        "bar": {
                            "color": "darkblue"
                        },


                        "steps":[

                            {
                                "range":[0,50],
                                "color":"red"
                            },

                            {
                                "range":[50,75],
                                "color":"orange"
                            },

                            {
                                "range":[75,100],
                                "color":"green"
                            }

                        ]

                    }

                )

            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )



            # -------- Metrics -------- #

            c1,c2,c3 = st.columns(3)



            c1.metric(

                "Skill Match",

                f'{ats_result["Skill Match"]}%'

            )


            c2.metric(

                "Similarity",

                f'{ats_result["Semantic Similarity"]}%'

            )


            c3.metric(

                "Resume Completeness",

                f'{ats_result["Resume Completeness"]}%'

            )



            # -------- ATS Breakdown Chart -------- #

            fig = go.Figure(

                data=[

                    go.Bar(

                        x=[

                            "Skill",

                            "Similarity",

                            "Education",

                            "Experience",

                            "Projects",

                            "Certification",

                            "Achievement",

                            "Completeness"

                        ],


                        y=[

                            ats_result["Skill Match"],

                            ats_result["Semantic Similarity"],

                            ats_result["Education Score"],

                            ats_result["Experience Score"],

                            ats_result["Project Score"],

                            ats_result["Certification Score"],

                            ats_result["Achievement Score"],

                            ats_result["Resume Completeness"]

                        ]

                    )

                ]

            )


            fig.update_layout(

                title="ATS Score Breakdown",

                yaxis_title="Score"

            )


            st.plotly_chart(

                fig,

                use_container_width=True

            )



            # -------- Candidate Information -------- #

            st.subheader(
                "Candidate Information"
            )



            st.write(
                "### Name"
            )

            st.write(
                resume_result["Name"]
            )



            st.write(
                "### Email"
            )

            st.write(
                resume_result["Email"]
            )



            st.write(
                "### Phone"
            )

            st.write(
                resume_result["Phone"]
            )



            st.write(
                "### LinkedIn"
            )

            st.write(

                resume_result["LinkedIn"]
                or
                "Not Found"

            )



            st.write(
                "### GitHub"
            )

            st.write(

                resume_result["GitHub"]
                or
                "Not Found"

            )



            # -------- Resume Statistics -------- #

            st.subheader(
                "Resume Statistics"
            )



            col1,col2,col3 = st.columns(3)



            col1.metric(

                "Resume Words",

                resume_result["Resume Length"]

            )


            col2.metric(

                "Matched Skills",

                len(
                    ats_result["Matched Skills"]
                )

            )


            col3.metric(

                "Missing Skills",

                len(
                    ats_result["Missing Skills"]
                )

            )

        # ================= Skills ================= #

        with tab2:


            st.subheader(
                "✅ Matched Skills"
            )


            if ats_result["Matched Skills"]:


                cols = st.columns(3)


                for i, skill in enumerate(
                    ats_result["Matched Skills"]
                ):

                    cols[i % 3].success(
                        skill
                    )


            else:

                st.info(
                    "No matched skills found."
                )



            st.subheader(
                "❌ Missing Skills"
            )



            if ats_result["Missing Skills"]:


                cols = st.columns(3)


                for i, skill in enumerate(
                    ats_result["Missing Skills"]
                ):

                    cols[i % 3].error(
                        skill
                    )


            else:

                st.success(
                    "No missing skills detected!"
                )



            st.subheader(
                "💡 Improvement Suggestions"
            )



            for suggestion in suggestions:

                st.warning(
                    suggestion
                )



            # -------- Skill Distribution -------- #

            matched = len(
                ats_result["Matched Skills"]
            )


            missing = len(
                ats_result["Missing Skills"]
            )



            fig = go.Figure(

                data=[

                    go.Pie(

                        labels=[
                            "Matched",
                            "Missing"
                        ],

                        values=[
                            matched,
                            missing
                        ],

                        hole=0.45

                    )

                ]

            )



            fig.update_layout(

                title="Skill Match Distribution"

            )



            st.plotly_chart(

                fig,

                use_container_width=True

            )




        # ================= Sections ================= #

        with tab3:


            st.subheader(
                "📄 Resume Sections"
            )



            for section, present in section_result["Detected Sections"].items():



                if present:


                    st.success(
                        f"✔ {section}"
                    )


                else:


                    st.error(
                        f"✘ {section}"
                    )




        # ================= Gap Analysis ================= #

        with tab4:


            st.subheader(
                "🎯 Gap Analysis"
            )



            st.json(
                gap
            )



            st.divider()



            st.subheader(
                "Job Role"
            )


            st.info(
                gap["Job Role"]
            )



            st.subheader(
                "Experience"
            )



            col1,col2 = st.columns(2)



            col1.metric(

                "Resume",

                gap["Resume Experience"]

            )



            col2.metric(

                "Required",

                gap["Required Experience"]

            )



            st.write(

                "**Status:**",

                gap["Experience Status"]

            )



            st.subheader(
                "Education"
            )


            st.write(
                gap["Education Status"]
            )



            st.subheader(
                "Estimated ATS"
            )



            st.progress(

                int(
                    gap["Estimated ATS"]
                )

            )



            st.metric(

                "Predicted ATS",

                f'{gap["Estimated ATS"]}%'

            )
       # ================= Reports ================= #

        with tab5:


            st.subheader(
                "📑 Download ATS Report"
            )


            with open(
                "ATS_Report.pdf",
                "rb"
            ) as pdf:


                st.download_button(

                    label="📄 Download ATS Report",

                    data=pdf,

                    file_name="ATS_Report.pdf",

                    mime="application/pdf"

                )



            st.divider()



            with st.expander(
                "ATS Report",
                expanded=False
            ):

                st.json(
                    ats_result
                )



            with st.expander(
                "Resume Report",
                expanded=False
            ):

                st.json(
                    resume_result
                )



            with st.expander(
                "JD Report",
                expanded=False
            ):

                st.json(
                    jd_result
                )



            with st.expander(
                "Section Report",
                expanded=False
            ):

                st.json(
                    section_result
                )



            with st.expander(
                "Gap Report",
                expanded=False
            ):

                st.json(
                    gap
                )



            st.divider()



            st.subheader(
                "Resume Statistics"
            )



            c1,c2,c3 = st.columns(3)



            c1.metric(

                "Words",

                resume_result["Resume Length"]

            )



            c2.metric(

                "Matched Skills",

                len(
                    ats_result["Matched Skills"]
                )

            )



            c3.metric(

                "Missing Skills",

                len(
                    ats_result["Missing Skills"]
                )

            )




        # ================= AI Bullet Rewriter ================= #

        with tab6:


            st.header(
                "✨ AI Resume Bullet Rewriter"
            )



            st.write(

                "AI-generated stronger resume bullet points."

            )



            if rewritten_bullets:


                for bullet in rewritten_bullets:


                    st.success(
                        bullet
                    )


            else:


                st.info(
                    "No rewritten bullets generated."
                )




        # ================= Footer ================= #

        st.markdown(
            "---"
        )



        st.caption(

            "Developed by Kanan Mundra | "
            "AI Resume Analyzer using NLP, "
            "Sentence Transformers & Streamlit"

        )