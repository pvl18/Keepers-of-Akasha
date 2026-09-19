import streamlit as st

from concepts import get_concepts

from agent import (
    start_run,
    submit_answer,
    resume_run,
    PASSED,
    FLAGGED,
    AWAITING_RESPONSE
)

from database import (
    init_db,
    create_user,
    create_concept
)


# ==================================================
# DATABASE INITIALIZATION
# ==================================================

init_db()


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Reasoning Check",
    page_icon="RC",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

    :root {
        --ink: #17211b;
        --muted: #66736b;
        --paper: #f5f4ee;
        --panel: #fffefa;
        --line: #d9ded7;
        --green: #176b4d;
        --lime: #cce982;
        --orange: #e88749;
    }

    .stApp {
        background: var(--paper);
        color: var(--ink);
    }

    [data-testid="stSidebar"] {
        background: #e5eadf;
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }

    h1,
    h2,
    h3,
    p,
    label,
    [data-testid="stMarkdownContainer"] {
        font-family: 'DM Sans', sans-serif;
    }

    h1 {
        font-size: 2.8rem;
        letter-spacing: -0.04em;
        margin-bottom: 0.25rem;
    }

    h2 {
        letter-spacing: -0.03em;
    }

    .brand-mark {
        font: 700 0.75rem 'Space Mono', monospace;
        color: var(--green);
        letter-spacing: 0.08em;
    }

    .eyebrow {
        font: 700 0.7rem 'Space Mono', monospace;
        color: var(--orange);
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .intro {
        color: var(--muted);
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    .scenario {
        background: var(--panel);
        border: 1px solid var(--line);
        border-left: 5px solid var(--green);
        padding: 1.25rem 1.4rem;
        margin: 1rem 0 1.5rem;
    }

    .scenario-title {
        font: 700 0.72rem 'Space Mono', monospace;
        color: var(--green);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.7rem;
    }

    .metric {
        background: var(--panel);
        border: 1px solid var(--line);
        padding: 1rem 1.1rem;
        min-height: 6rem;
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.8rem;
    }

    .metric-value {
        color: var(--green);
        font-size: 1.7rem;
        font-weight: 700;
        margin-top: 0.25rem;
    }

    .stButton > button {
        border-radius: 4px;
        font-weight: 600;
        border: 1px solid var(--green);
    }

    .stButton > button[kind="primary"] {
        background: var(--green);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# CONCEPTS
# ==================================================

CONCEPTS = get_concepts()


# ==================================================
# SIDEBAR BRAND
# ==================================================

def show_brand():
    st.sidebar.markdown(
        '<div class="brand-mark">REASONING CHECK / 01</div>',
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        "## Industrial\n## Biotechnology"
    )

    st.sidebar.caption(
        "A practice space for explaining the science "
        "behind laboratory procedures."
    )


# ==================================================
# STUDENT PAGE
# ==================================================

def student_page():
    st.markdown(
        '<div class="eyebrow">Student workspace</div>',
        unsafe_allow_html=True
    )

    st.title("Make your reasoning visible.")

    st.markdown(
        '<p class="intro">'
        'Work through a laboratory scenario, explain the underlying '
        'cause, and strengthen your answer with focused feedback.'
        '</p>',
        unsafe_allow_html=True
    )

    # ----------------------------------------------
    # SETUP AND PROGRESS
    # ----------------------------------------------

    setup, progress = st.columns(
        [1.4, 1],
        gap="large"
    )

    with setup:
        st.subheader("Start a reasoning check")

        student_name = st.text_input(
            "Student name",
            value=""
        )

        concept = st.selectbox(
            "Concept",
            CONCEPTS
        )

        if st.button(
            "Generate scenario",
            type="primary",
            use_container_width=True
        ):
            if not student_name.strip():
                st.warning(
                    "Enter your name before starting."
                )

            else:
                user_id = create_user(
                    student_name.strip()
                )

                concept_id = create_concept(
                    concept,
                    "medium",
                    (
                        "Explain the reasoning behind "
                        "the observed result."
                    )
                )

                run_id = start_run(
                    user_id=user_id,
                    concept_id=concept_id,
                    concept_name=concept
                )

                st.session_state.run_id = run_id
                st.session_state.active_concept = concept
                st.session_state.student_name = (
                    student_name.strip()
                )
                st.session_state.started = True
                st.session_state.feedback = None

                st.rerun()

    # ----------------------------------------------
    # LOAD CURRENT RUN
    # ----------------------------------------------

    run_state = None

    if st.session_state.get("run_id"):
        try:
            run_state = resume_run(
                st.session_state.run_id
            )

        except ValueError:
            run_state = None

    # ----------------------------------------------
    # PROGRESS
    # ----------------------------------------------

    with progress:
        st.subheader("Your progress")

        if run_state:
            current_status = run_state["status"]

            current_attempt = run_state[
                "current_attempt"
            ]

            attempts_remaining = max(
                0,
                3 - current_attempt
            )

            st.markdown(
                f"""
                <div class="metric">
                    <div class="metric-label">
                        CURRENT RUN
                    </div>
                    <div class="metric-value">
                        {current_status.replace("_", " ").title()}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("\n")

            st.markdown(
                f"""
                <div class="metric">
                    <div class="metric-label">
                        ATTEMPTS AVAILABLE
                    </div>
                    <div class="metric-value">
                        {attempts_remaining}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.markdown(
                """
                <div class="metric">
                    <div class="metric-label">
                        CURRENT RUN
                    </div>
                    <div class="metric-value">
                        Not started
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("\n")

            st.markdown(
                """
                <div class="metric">
                    <div class="metric-label">
                        ATTEMPTS AVAILABLE
                    </div>
                    <div class="metric-value">
                        3
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ----------------------------------------------
    # ACTIVE SCENARIO
    # ----------------------------------------------

    if run_state:
        st.divider()

        active_concept = run_state[
            "concept_name"
        ]

        st.markdown(
            f'<div class="eyebrow">'
            f'Scenario / {active_concept}'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="scenario">
                <div class="scenario-title">
                    Laboratory situation
                </div>
                {run_state["scenario"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        status = run_state["status"]

        # ------------------------------------------
        # STUDENT RESPONSE
        # ------------------------------------------

        if status == AWAITING_RESPONSE:
            st.subheader("Explain the why")

            response = st.text_area(
                "Your reasoning",
                height=190,
                placeholder=(
                    "What happened, why did it happen, "
                    "and how does the procedure cause "
                    "the result?"
                ),
                label_visibility="collapsed",
                key="student_reasoning"
            )

            if st.button(
                "Submit reasoning",
                type="primary"
            ):
                if not response.strip():
                    st.warning(
                        "Write a response before submitting."
                    )

                else:
                    try:
                        result = submit_answer(
                            run_id=st.session_state.run_id,
                            student_response=response.strip()
                        )

                        st.session_state.feedback = result

                        st.rerun()

                    except ValueError as error:
                        st.error(str(error))

        # ------------------------------------------
        # FEEDBACK
        # ------------------------------------------

        feedback = st.session_state.get(
            "feedback"
        )

        if feedback:
            st.divider()
            st.subheader("Feedback")

            evaluation = feedback[
                "evaluation"
            ]

            quality = evaluation[
                "quality"
            ]

            if quality == "strong":
                st.success(
                    "Strong reasoning."
                )

            elif quality == "partial":
                st.warning(
                    "Your reasoning is on the right track, "
                    "but it needs a clearer scientific connection."
                )

            else:
                st.error(
                    "Your response does not yet demonstrate "
                    "the required reasoning."
                )

            st.write(
                evaluation["reasoning"]
            )

            # Show hints only while another retry is available.
            # The evaluator still saves the final hint to the DB.
            if (
                evaluation["hint"]
                and feedback["status"] != FLAGGED
            ):
                st.info(
                    f'Hint: {evaluation["hint"]}'
                )

            if feedback["status"] == PASSED:
                st.success(
                    "Reasoning check passed."
                )

            elif feedback["status"] == FLAGGED:
                st.error(
                    "All three attempts have been used. "
                    "This run has been sent for "
                    "professor review."
                )

        # ------------------------------------------
        # ATTEMPT HISTORY
        # ------------------------------------------

        st.subheader("Attempt history")

        attempts = run_state.get(
            "attempts",
            []
        )

        if attempts:
            for attempt in attempts:
                attempt_number = attempt.get(
                    "attempt_number",
                    "?"
                )

                student_response = attempt.get(
                    "student_response",
                    ""
                )

                with st.expander(
                    f"Attempt {attempt_number}"
                ):
                    st.write(
                        student_response
                    )

                    quality = attempt.get(
                        "quality"
                    )

                    reasoning = attempt.get(
                        "reasoning"
                    )

                    hint = attempt.get(
                        "hint"
                    )

                    if quality:
                        st.caption(
                            f"Evaluation: {quality}"
                        )

                    if reasoning:
                        st.write(
                            reasoning
                        )

                    if hint:
                        st.info(
                            f"Hint: {hint}"
                        )

        else:
            st.caption(
                "No attempts submitted yet."
            )


# ==================================================
# PROFESSOR PAGE
# ==================================================

def professor_page():
    st.markdown(
        '<div class="eyebrow">Review workspace</div>',
        unsafe_allow_html=True
    )

    st.title("Professor dashboard")

    st.markdown(
        '<p class="intro">'
        'Review runs that need attention and inspect '
        'the reasoning behind each result.'
        '</p>',
        unsafe_allow_html=True
    )

    first, second, third = st.columns(3)

    with first:
        st.markdown(
            """
            <div class="metric">
                <div class="metric-label">
                    ACTIVE RUNS
                </div>
                <div class="metric-value">
                    12
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with second:
        st.markdown(
            """
            <div class="metric">
                <div class="metric-label">
                    PASSED TODAY
                </div>
                <div class="metric-value">
                    8
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with third:
        st.markdown(
            """
            <div class="metric">
                <div class="metric-label">
                    NEEDS REVIEW
                </div>
                <div class="metric-value">
                    3
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader(
        "Runs needing review"
    )

    st.dataframe(
        {
            "Student": [
                "student_014",
                "student_009",
                "student_021"
            ],
            "Concept": [
                "Gram Staining",
                "Fermentation",
                "Protein Purification"
            ],
            "Attempts": [
                3,
                3,
                2
            ],
            "Status": [
                "Flagged",
                "Flagged",
                "Retry"
            ],
        },
        hide_index=True,
        use_container_width=True,
    )

    st.caption(
        "Backend connection point: replace demo rows "
        "with persisted flag and attempt records."
    )


# ==================================================
# SESSION STATE
# ==================================================

if "started" not in st.session_state:
    st.session_state.started = False

if "feedback" not in st.session_state:
    st.session_state.feedback = None

if "run_id" not in st.session_state:
    st.session_state.run_id = None

if "active_concept" not in st.session_state:
    st.session_state.active_concept = None

if "student_name" not in st.session_state:
    st.session_state.student_name = None


# ==================================================
# APPLICATION
# ==================================================

show_brand()

page = st.sidebar.radio(
    "Workspace",
    [
        "Student",
        "Professor dashboard"
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()

st.sidebar.caption(
    "Reasoning Check"
)

if page == "Student":
    student_page()
else:
    professor_page()