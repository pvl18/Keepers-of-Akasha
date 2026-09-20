import html

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

    /* Slightly darker shades of the sidebar's existing soft green palette. */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #667460 !important;
        -webkit-text-fill-color: #667460 !important;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label p {
        color: #5b6956 !important;
        -webkit-text-fill-color: #5b6956 !important;
    }

    .partial-feedback {
        background: #fff4b8;
        color: #9a7410;
        border-radius: 0.5rem;
        padding: 1rem 1.1rem;
        margin: 0.5rem 0 1rem;
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
    }

    .evaluation-unavailable {
        background: #fff4e5;
        border: 1px solid #efc27b;
        border-left: 5px solid #d97706;
        border-radius: 0.5rem;
        padding: 1.1rem 1.2rem;
        margin: 0.5rem 0 1rem;
        font-family: 'DM Sans', sans-serif;
    }

    .evaluation-unavailable-title {
        color: #9a5b08;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .evaluation-unavailable-text {
        color: #6f5634;
        font-size: 0.95rem;
        line-height: 1.5;
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

    .scenario-text {
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        line-height: 1.65;
        white-space: pre-wrap;
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

    /* Keep student typing clearly visible on the dark textarea. */
    div[data-testid="stTextArea"] textarea {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: #ffffff !important;
    }

    div[data-testid="stTextArea"] textarea::placeholder {
        color: #bfc5cc !important;
        -webkit-text-fill-color: #bfc5cc !important;
        opacity: 1 !important;
    }


    /* Attempt history expander - normal state */
    div[data-testid="stExpander"] details summary {
        background-color: #e9ebe7 !important;
        color: #25352b !important;
        border-radius: 4px !important;
    }

    /* Attempt history expander text */
    div[data-testid="stExpander"] details summary p {
        color: #25352b !important;
        -webkit-text-fill-color: #25352b !important;
    }

    /* Expander arrow */
    div[data-testid="stExpander"] details summary svg {
        fill: #25352b !important;
        color: #25352b !important;
    }

    /* Hover state - only slightly darker */
    div[data-testid="stExpander"] details summary:hover {
        background-color: #dde1dc !important;
        color: #25352b !important;
    }

    /* Keep text visible while hovering */
    div[data-testid="stExpander"] details summary:hover p {
        color: #25352b !important;
        -webkit-text-fill-color: #25352b !important;
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
# EVALUATION HELPERS
# ==================================================

def evaluation_unavailable(evaluation):
    reasoning = str(evaluation.get("reasoning", "")).strip().lower()
    return reasoning in {
        "evaluation could not be completed.",
        "evaluation couldn't be made",
        "evaluation could not be made",
    }


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

        scenario_text = html.escape(run_state["scenario"])

        st.markdown(
            f"""
            <div class="scenario">
                <div class="scenario-title">Laboratory situation</div>
                <div class="scenario-text">{scenario_text}</div>
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

            if evaluation_unavailable(evaluation):
                st.markdown(
                    """
                    <div class="evaluation-unavailable">
                        <div class="evaluation-unavailable-title">
                            Evaluation couldn't be made
                        </div>
                        <div class="evaluation-unavailable-text">
                            Servers might be busy or check your network connection.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:
                quality = evaluation[
                    "quality"
                ]

                if quality == "strong":
                    st.success(
                        "Strong reasoning."
                    )

                elif quality == "partial":
                    st.markdown(
                        '<div class="partial-feedback">'
                        'Your reasoning is on the right track, '
                        'but it needs a clearer scientific connection.'
                        '</div>',
                        unsafe_allow_html=True
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

st.sidebar.markdown("### Workspace")
st.sidebar.markdown("**Student**")

# The professor dashboard is intentionally a separate Streamlit app.
# Run dashboard.py on port 8502, then this opens it in a new browser tab.
st.sidebar.link_button(
    "Professor dashboard ↗",
    "http://localhost:8502",
    use_container_width=True,
)

st.sidebar.divider()
st.sidebar.caption("Reasoning Check")

student_page()
