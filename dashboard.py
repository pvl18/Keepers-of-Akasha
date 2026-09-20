import streamlit as st
import pandas as pd
from database import (
    get_flagged_students,
    get_complete_run_details,
    save_professor_review,
    get_students,
    get_student_concept_progress,
    get_student_runs,
    get_dashboard_summary,
    get_concept_performance
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
    color: #111827;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 15px;
}

.card p {
    color: #374151;
}

.card-title {
    color: #111827;
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
# DASHBOARD DATA
# =========================================================

flagged_students = get_flagged_students()
dashboard_summary = get_dashboard_summary()
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


concept_performance = get_concept_performance()

concept_data = pd.DataFrame(
    [
        {
            "Concept": concept["concept_name"],
            "Performance": concept["performance"]
        }
        for concept in concept_performance
    ]
)

if concept_performance:
    lowest_concept = min(
        concept_performance,
        key=lambda concept: concept["performance"]
    )
    strongest_concept = max(
        concept_performance,
        key=lambda concept: concept["performance"]
    )
else:
    lowest_concept = None
    strongest_concept = None


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
        st.markdown(
            f"""
            <div class="card">
                <div class="metric-label">👨‍🎓 Students</div>
                <div class="metric-number">
                    {dashboard_summary["total_students"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="card">
                <div class="metric-label">📚 Concepts Assessed</div>
                <div class="metric-number">
                    {dashboard_summary["concepts_assessed"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="card">
                <div class="metric-label">🔄 Active Learning</div>
                <div class="metric-number">
                    {dashboard_summary["active_learning"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="card">
                <div class="metric-label">🚩 Needs Attention</div>
                <div class="metric-number">
                    {dashboard_summary["needs_attention"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

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

        if students:
            df_students = pd.DataFrame(students)

            st.dataframe(
                df_students,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success(
                "No students currently need professor review."
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

        if not concept_performance:
            st.info(
                "No concept performance data is available yet."
            )
        else:
            st.warning(
                "🟡 **Lowest current outcome rate**\n\n"
                f'{lowest_concept["concept_name"]}: '
                f'{lowest_concept["performance"]}% '
                f'across {lowest_concept["total_runs"]} run(s).'
            )

            st.success(
                "🟢 **Highest current outcome rate**\n\n"
                f'{strongest_concept["concept_name"]}: '
                f'{strongest_concept["performance"]}% '
                f'across {strongest_concept["total_runs"]} run(s).'
            )

            st.caption(
                "Outcome rate is based on completed run statuses "
                "and is not a student grade."
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
            concept_data.set_index("Concept")["Performance"]
        )

    with insight_col:

        if lowest_concept and strongest_concept:
            st.markdown(
                f"""
                <div class="card">

                <div class="card-title">
                Concept Overview
                </div>

                <p>
                Performance is calculated from completed
                learning-run outcomes.
                </p>

                <p>
                <b>Lowest current outcome rate:</b><br>
                {lowest_concept["concept_name"]}
                ({lowest_concept["performance"]}%)
                </p>

                <p>
                <b>Highest current outcome rate:</b><br>
                {strongest_concept["concept_name"]}
                ({strongest_concept["performance"]}%)
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("No concept performance data is available yet.")

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

        st.markdown(
            f"""
            <div class="card">

            <div class="card-title">
            🧠 Reasoning Check
            </div>

            <p>
            Scenario-based reasoning assessment.
            </p>

            <p>
            <b>{dashboard_summary["total_students"]}</b>
            students assessed<br>
            <b>{dashboard_summary["needs_attention"]}</b>
            need attention
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

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
        Planned module
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
        Planned module
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

    student_records = get_students()

    if not student_records:
        st.info(
            "No student learning activity has been recorded yet."
        )

    else:
        student_options = {
            student["student_name"]: student
            for student in student_records
        }

        selected_student = st.selectbox(
            "Select Student",
            list(student_options.keys())
        )

        student = student_options[selected_student]

        st.divider()

        st.subheader(selected_student)

        a, b, c, d = st.columns(4)

        with a:
            st.metric(
                "Concepts Assessed",
                student["concepts_assessed"]
            )

        with b:
            st.metric(
                "Attempts",
                student["total_attempts"]
            )

        with c:
            st.metric(
                "Needs Attention",
                student["needs_attention"]
            )

        with d:
            st.metric(
                "Total Runs",
                student["total_runs"]
            )
        st.divider()

        st.subheader("📚 Concept Progress")

        concept_progress = get_student_concept_progress(
            student["user_id"]
        )

        if not concept_progress:
            st.info(
                "No concept activity found for this student."
            )

        else:
            progress_rows = []

            for concept in concept_progress:
                if concept["pending_flags"] > 0:
                    status = "Needs Attention"

                elif concept["reviewed_runs"] > 0:
                    status = "Reviewed"

                elif concept["passed_runs"] > 0:
                    status = "Passed"

                elif concept["flagged_runs"] > 0:
                    status = "Flagged"

                else:
                    status = "In Progress"

                progress_rows.append(
                    {
                        "Concept": concept["concept_name"],
                        "Runs": concept["total_runs"],
                        "Attempts": concept["total_attempts"],
                        "Passed": concept["passed_runs"],
                        "Flagged": concept["flagged_runs"],
                        "Reviewed": concept["reviewed_runs"],
                        "Pending Review": concept["pending_flags"],
                        "Status": status
                    }
                )

            progress_df = pd.DataFrame(progress_rows)

            st.dataframe(
                progress_df,
                use_container_width=True,
                hide_index=True
            )
            st.divider()

            st.subheader("🧪 Run History")

            concept_names = [
                concept["concept_name"]
                for concept in concept_progress
            ]

            selected_concept = st.selectbox(
                "Select Concept",
                concept_names,
                key="student_concept_history"
            )

            student_runs = get_student_runs(
                student["user_id"],
                selected_concept
            )

            if not student_runs:
                st.info(
                    "No runs found for this concept."
                )

            else:
                run_rows = []

                for run in student_runs:
                    run_rows.append(
                        {
                            "Run": run["run_id"],
                            "Status": run["status"]
                            .replace("_", " ")
                            .title(),
                            "Attempts": run["attempts"],
                            "Created": run["created_at"][:19]
                            .replace("T", " ")
                        }
                    )

                run_df = pd.DataFrame(run_rows)

                st.dataframe(
                    run_df,
                    use_container_width=True,
                    hide_index=True
                )
                st.divider()

                st.subheader("🔎 Inspect Run")

                run_options = {
                    (
                        f'Run {run["run_id"]} — '
                        f'{run["status"].replace("_", " ").title()}'
                    ): run["run_id"]
                    for run in student_runs
                }

                selected_run_label = st.selectbox(
                    "Select Run",
                    list(run_options.keys()),
                    key="student_run_inspection"
                )

                selected_run_id = run_options[
                    selected_run_label
                ]

                run_details = get_complete_run_details(
                    selected_run_id
                )

                if run_details is None:
                    st.error(
                        "The selected run could not be found."
                    )

                else:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Status",
                            run_details["status"]
                            .replace("_", " ")
                            .title()
                        )

                    with col2:
                        st.metric(
                            "Attempts",
                            run_details["current_attempt"]
                        )

                    st.markdown("**Laboratory Scenario**")

                    st.info(
                        run_details["scenario"]
                    )

                    st.markdown("**Expected Reasoning**")

                    st.write(
                        run_details["expecting_reasoning"]
                    )

                    st.markdown("**Student Attempts**")

                    attempts = run_details.get(
                        "attempts",
                        []
                    )

                    if not attempts:
                        st.warning(
                            "No attempts were recorded for this run."
                        )

                    else:
                        for attempt in attempts:
                            attempt_number = attempt[
                                "attempt_number"
                            ]

                            with st.expander(
                                f"Attempt {attempt_number}"
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
                                    quality = evaluation[
                                        "quality"
                                    ]

                                    st.markdown(
                                        "**AI classification**"
                                    )

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
                                            "**Hint**"
                                        )

                                        st.info(
                                            evaluation["hint"]
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
        concept_data.set_index("Concept")["Performance"]
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

    if not concept_performance:
        st.info(
            "No class learning data is available yet."
        )

    else:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Lower Outcome Areas")

            lower_areas = sorted(
                concept_performance,
                key=lambda concept: concept["performance"]
            )

            for concept in lower_areas:
                st.write(
                    f'• {concept["concept_name"]}: '
                    f'{concept["performance"]}% '
                    f'across {concept["total_runs"]} run(s)'
                )

        with col2:
            st.subheader("Higher Outcome Areas")

            higher_areas = sorted(
                concept_performance,
                key=lambda concept: concept["performance"],
                reverse=True
            )

            for concept in higher_areas:
                st.write(
                    f'• {concept["concept_name"]}: '
                    f'{concept["performance"]}% '
                    f'across {concept["total_runs"]} run(s)'
                )

        st.caption(
            "These are run-outcome summaries, not student grades or "
            "formal mastery scores."
        )
