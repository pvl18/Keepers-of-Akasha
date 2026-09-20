import streamlit as st
import pandas as pd
from database import (
    get_flagged_students,
    get_complete_run_details,
    save_professor_review
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Professor Dashboard",
    page_icon="🧠",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 1.5rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

.main-title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 0px;
}

.subtitle {
    color: #6b7280;
    font-size: 15px;
    margin-bottom: 25px;
}

.card {
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 15px;
}

.card-title {
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 8px;
}

.metric-number {
    font-size: 28px;
    font-weight: 700;
}

.metric-label {
    color: #6b7280;
    font-size: 13px;
}

.section-title {
    font-size: 21px;
    font-weight: 650;
    margin-top: 20px;
    margin-bottom: 15px;
}

.status-red {
    color: #dc2626;
    font-weight: 600;
}

.status-yellow {
    color: #d97706;
    font-weight: 600;
}

.status-green {
    color: #16a34a;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🧠 LearnWise")

    st.caption("AI-powered learning insights")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Students",
            "Concepts",
            "AI Modules",
            "Needs Attention",
            "Class Insights"
        ]
    )

    st.divider()

    st.markdown("### Course")

    st.write("Industrial Biotechnology")

    st.write("Semester III")


# =========================================================
# SAMPLE DATA
# Replace with database/API data later
# =========================================================

flagged_students = get_flagged_students()

students = []

for flag in flagged_students:
    students.append(
        {
            "student": flag["student_name"],
            "concept": flag["concept_name"],
            "issue": flag["reason"],
            "status": "Needs Attention",
            "run_id": flag["run_id"],
            "flag_id": flag["flag_id"]
        }
    )


concept_data = pd.DataFrame({
    "Concept": [
        "Gram Staining",
        "Fermentation",
        "Protein Purification",
        "Enzyme Activity",
        "TLC"
    ],
    "Mastery": [72, 51, 81, 64, 70]
})


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">Professor Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Monitor class learning, identify gaps and review AI-generated insights.'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # TOP METRICS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="metric-label">👨‍🎓 Students</div>
            <div class="metric-number">42</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="metric-label">📚 Concepts Assessed</div>
            <div class="metric-number">18</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <div class="metric-label">🔄 Active Learning</div>
            <div class="metric-number">27</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="card">
            <div class="metric-label">🚩 Needs Attention</div>
            <div class="metric-number">6</div>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # TWO COLUMN AREA
    # -----------------------------------------------------

    left, right = st.columns([1.4, 1])

    # -----------------------------------------------------
    # STUDENTS NEEDING ATTENTION
    # -----------------------------------------------------

    with left:

        st.markdown(
            '<div class="section-title">'
            '🚩 Students Needing Attention'
            '</div>',
            unsafe_allow_html=True
        )

        df_students = pd.DataFrame(students)

        st.dataframe(
            df_students,
            use_container_width=True,
            hide_index=True
        )

        if st.button(
            "View Student Analysis →",
            use_container_width=True
        ):
            st.session_state["page"] = "Students"

    # -----------------------------------------------------
    # CLASS INSIGHTS
    # -----------------------------------------------------

    with right:

        st.markdown(
            '<div class="section-title">'
            '🧠 Learning Insights'
            '</div>',
            unsafe_allow_html=True
        )

        st.info(
            "🔴 **Common difficulty**\n\n"
            "Students are struggling to connect "
            "decolorization time with Gram staining results."
        )

        st.warning(
            "🟡 **Emerging difficulty**\n\n"
            "Several students need support connecting "
            "fermentation conditions with product formation."
        )

        st.success(
            "🟢 **Strong area**\n\n"
            "Protein purification fundamentals show "
            "relatively strong understanding."
        )

    # -----------------------------------------------------
    # CONCEPT PERFORMANCE
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📚 Concept Performance'
        '</div>',
        unsafe_allow_html=True
    )

    chart_col, insight_col = st.columns([1.5, 1])

    with chart_col:

        st.bar_chart(
            concept_data.set_index("Concept")["Mastery"]
        )

    with insight_col:

        st.markdown("""
        <div class="card">

        <div class="card-title">
        Concept Overview
        </div>

        <p>
        Concepts with lower class performance can be
        investigated through the corresponding AI modules.
        </p>

        <p>
        <b>Lowest current area:</b><br>
        Fermentation
        </p>

        <p>
        <b>Strongest current area:</b><br>
        Protein Purification
        </p>

        </div>
        """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # AI MODULES
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🤖 AI Learning Modules'
        '</div>',
        unsafe_allow_html=True
    )

    m1, m2, m3 = st.columns(3)

    with m1:

        st.markdown("""
        <div class="card">

        <div class="card-title">
        🧠 Reasoning Check
        </div>

        <p>
        Scenario-based reasoning assessment.
        </p>

        <p>
        <b>31</b> students assessed<br>
        <b>5</b> need attention
        </p>

        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Open Module",
            key="reasoning_module",
            use_container_width=True
        ):
            st.info("Reasoning Check module selected.")

    with m2:

        st.markdown("""
        <div class="card">

        <div class="card-title">
        🌍 Real-World Connect
        </div>

        <p>
        Connect classroom concepts with
        real-world situations.
        </p>

        <p>
        <b>24</b> scenarios completed
        </p>

        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Open Module",
            key="realworld_module",
            use_container_width=True
        ):
            st.info("Real-World Connect module selected.")

    with m3:

        st.markdown("""
        <div class="card">

        <div class="card-title">
        ⚗️ Chemical Simulator
        </div>

        <p>
        Interactive exploration of
        chemical processes.
        </p>

        <p>
        <b>18</b> simulations completed
        </p>

        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Open Module",
            key="chemical_module",
            use_container_width=True
        ):
            st.info("Chemical Simulator module selected.")


# =========================================================
# STUDENTS PAGE
# =========================================================

elif page == "Students":

    st.title("👨‍🎓 Students")

    st.caption(
        "Explore individual student learning profiles."
    )

    student_names = [
        "Student 014",
        "Student 021",
        "Student 009"
    ]

    selected_student = st.selectbox(
        "Select Student",
        student_names
    )

    st.divider()

    st.subheader(selected_student)

    a, b, c, d = st.columns(4)

    with a:
        st.metric("Concepts Assessed", 6)

    with b:
        st.metric("Attempts", 11)

    with c:
        st.metric("Needs Attention", 2)

    with d:
        st.metric("Strong Concepts", 4)

    st.divider()

    st.subheader("📚 Concept Progress")

    student_progress = pd.DataFrame({
        "Concept": [
            "Gram Staining",
            "Fermentation",
            "Protein Purification",
            "TLC"
        ],
        "Status": [
            "Needs Attention",
            "Developing",
            "Strong",
            "Strong"
        ]
    })

    st.dataframe(
        student_progress,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🧠 Learning Analysis")

    st.warning(
        "Student initially demonstrated difficulty connecting "
        "experimental procedure with observed results."
    )

    st.success(
        "Reasoning improved after targeted feedback."
    )


# =========================================================
# CONCEPTS PAGE
# =========================================================

elif page == "Concepts":

    st.title("📚 Concept Performance")

    st.caption(
        "View how students are performing across concepts."
    )

    st.dataframe(
        concept_data,
        use_container_width=True,
        hide_index=True
    )

    st.bar_chart(
        concept_data.set_index("Concept")["Mastery"]
    )


# =========================================================
# AI MODULES PAGE
# =========================================================

elif page == "AI Modules":

    st.title("🤖 AI Learning Modules")

    st.caption(
        "Integrated learning modules available in the system."
    )

    modules = [
        (
            "🧠 Reasoning Check",
            "Evaluates student reasoning through "
            "scenario-based challenges."
        ),
        (
            "🌍 Real-World Connect",
            "Connects classroom learning with "
            "real-world situations."
        ),
        (
            "⚗️ Chemical Simulator",
            "Allows students to explore "
            "chemical processes."
        )
    ]

    for title, description in modules:

        st.markdown(
            f"""
            <div class="card">

            <div class="card-title">
            {title}
            </div>

            <p>{description}</p>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# NEEDS ATTENTION PAGE
# =========================================================

elif page == "Needs Attention":

    st.title("🚩 Students Needing Attention")

    st.caption(
        "Review students flagged after three unsuccessful "
        "reasoning attempts."
    )

    if not flagged_students:
        st.success(
            "No students currently need professor review."
        )

    else:
        case_options = {}

        for flag in flagged_students:
            label = (
                f'{flag["student_name"]} — '
                f'{flag["concept_name"]} '
                f'(Run {flag["run_id"]})'
            )

            case_options[label] = flag

        selected_case = st.selectbox(
            "Select flagged case",
            list(case_options.keys())
        )

        selected_flag = case_options[selected_case]

        run_details = get_complete_run_details(
            selected_flag["run_id"]
        )

        if run_details is None:
            st.error(
                "The selected run could not be found."
            )

        else:
            st.divider()

            st.subheader(
                f'{run_details["user_name"]} — '
                f'{run_details["concept_name"]}'
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Attempts",
                    run_details["current_attempt"]
                )

            with col2:
                st.metric(
                    "Run Status",
                    run_details["status"].replace(
                        "_",
                        " "
                    ).title()
                )

            with col3:
                st.metric(
                    "Flag Status",
                    selected_flag["status"].title()
                )

            st.subheader("Laboratory Scenario")

            st.info(
                run_details["scenario"]
            )

            st.subheader("Expected Reasoning")

            st.write(
                run_details["expecting_reasoning"]
            )

            st.subheader("Student Attempts")

            attempts = run_details.get(
                "attempts",
                []
            )

            if not attempts:
                st.warning(
                    "No attempts were found for this run."
                )

            else:
                for attempt in attempts:
                    attempt_number = attempt[
                        "attempt_number"
                    ]

                    with st.expander(
                        f"Attempt {attempt_number}",
                        expanded=True
                    ):
                        st.markdown(
                            "**Student response**"
                        )

                        st.write(
                            attempt["student_response"]
                        )

                        evaluation = attempt.get(
                            "evaluation"
                        )

                        if evaluation:
                            st.markdown(
                                "**AI classification**"
                            )

                            quality = evaluation[
                                "quality"
                            ]

                            if quality == "strong":
                                st.success(
                                    quality.title()
                                )

                            elif quality == "partial":
                                st.warning(
                                    quality.title()
                                )

                            else:
                                st.error(
                                    quality.title()
                                )

                            st.markdown(
                                "**AI reasoning**"
                            )

                            st.write(
                                evaluation["reasoning"]
                            )

                            if evaluation["hint"]:
                                st.markdown(
                                    "**Hint given to student**"
                                )

                                st.info(
                                    evaluation["hint"]
                                )

                        else:
                            st.warning(
                                "No evaluation was stored "
                                "for this attempt."
                            )

            st.divider()

            st.subheader("Flag Details")

            st.write(
                selected_flag["reason"]
            )
            st.divider()

            st.subheader("Professor Review")

            decision = st.radio(
                "Decision",
                [
                    "Approve",
                    "Reject"
                ],
                horizontal=True,
                key=f'review_decision_{selected_flag["flag_id"]}'
            )

            comments = st.text_area(
                "Professor comments",
                placeholder=(
                    "Add comments about the student's "
                    "reasoning or recommended follow-up."
                ),
                key=f'review_comments_{selected_flag["flag_id"]}'
            )

            if st.button(
                "Submit Review",
                type="primary",
                key=f'review_submit_{selected_flag["flag_id"]}'
            ):
                decision_value = decision.lower()

                review_id = save_professor_review(
                    flag_id=selected_flag["flag_id"],
                    decision=decision_value,
                    comments=comments.strip()
                )

                st.success(
                    f"Review {review_id} saved successfully."
                )

                st.rerun()

# =========================================================
# CLASS INSIGHTS PAGE
# =========================================================

elif page == "Class Insights":

    st.title("📈 Class Learning Insights")

    st.caption(
        "Aggregated patterns across student learning activity."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Common Difficulties")

        st.write(
            "• Procedural reasoning in Gram staining"
        )

        st.write(
            "• Connecting conditions with fermentation outcomes"
        )

        st.write(
            "• Understanding purification losses"
        )

    with col2:

        st.subheader("Areas of Strength")

        st.write(
            "• Protein purification fundamentals"
        )

        st.write(
            "• Basic TLC interpretation"
        )

        st.write(
            "• Experimental observation"
        )