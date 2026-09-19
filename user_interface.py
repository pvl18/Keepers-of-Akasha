import streamlit as st


st.set_page_config(
	page_title="Reasoning Check",
	page_icon="RC",
	layout="wide",
	initial_sidebar_state="expanded",
)

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

	.stApp { background: var(--paper); color: var(--ink); }
	[data-testid="stSidebar"] { background: #e5eadf; border-right: 1px solid var(--line); }
	[data-testid="stSidebar"] > div:first-child { padding-top: 2rem; }
	h1, h2, h3, p, label, [data-testid="stMarkdownContainer"] { font-family: 'DM Sans', sans-serif; }
	h1 { font-size: 2.8rem; letter-spacing: -0.04em; margin-bottom: 0.25rem; }
	h2 { letter-spacing: -0.03em; }
	.brand-mark { font: 700 0.75rem 'Space Mono', monospace; color: var(--green); letter-spacing: 0.08em; }
	.eyebrow { font: 700 0.7rem 'Space Mono', monospace; color: var(--orange); letter-spacing: 0.12em; text-transform: uppercase; }
	.intro { color: var(--muted); font-size: 1.05rem; margin-bottom: 2rem; }
	.scenario { background: var(--panel); border: 1px solid var(--line); border-left: 5px solid var(--green); padding: 1.25rem 1.4rem; margin: 1rem 0 1.5rem; }
	.scenario-title { font: 700 0.72rem 'Space Mono', monospace; color: var(--green); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.7rem; }
	.metric { background: var(--panel); border: 1px solid var(--line); padding: 1rem 1.1rem; min-height: 6rem; }
	.metric-label { color: var(--muted); font-size: 0.8rem; }
	.metric-value { color: var(--green); font-size: 1.7rem; font-weight: 700; margin-top: 0.25rem; }
	.stButton > button { border-radius: 4px; font-weight: 600; border: 1px solid var(--green); }
	.stButton > button[kind="primary"] { background: var(--green); color: white; }
	</style>
	""",
	unsafe_allow_html=True,
)


CONCEPTS = [
	"Gram staining",
	"TLC lipid separation",
	"Fermentation",
	"Enzyme immobilization",
	"Protein purification",
]

DEMO_SCENARIOS = {
	"Gram staining": "A student leaves the decolorizer on a Gram-stained slide much longer than instructed. The slide appears unusually pale. Why does timing matter?",
	"TLC lipid separation": "Two lipid samples produce spots at nearly the same height on a TLC plate. What could explain this result?",
	"Fermentation": "A fermentation vessel produces less desired product after its temperature rises above the set point. Explain why.",
	"Enzyme immobilization": "An immobilized enzyme can be reused, but its reaction is slower than the free enzyme. Explain both observations.",
	"Protein purification": "A target protein fails to bind to an affinity column even though the column was prepared correctly. What could cause this?",
}


def show_brand():
	st.sidebar.markdown('<div class="brand-mark">REASONING CHECK / 01</div>', unsafe_allow_html=True)
	st.sidebar.markdown("## Industrial\n## Biotechnology")
	st.sidebar.caption("A practice space for explaining the science behind laboratory procedures.")


def student_page():
	st.markdown('<div class="eyebrow">Student workspace</div>', unsafe_allow_html=True)
	st.title("Make your reasoning visible.")
	st.markdown('<p class="intro">Work through a laboratory scenario, explain the underlying cause, and strengthen your answer with focused feedback.</p>', unsafe_allow_html=True)

	setup, progress = st.columns([1.4, 1], gap="large")
	with setup:
		st.subheader("Start a reasoning check")
		student_id = st.text_input("Student ID", value="student_001")
		concept = st.selectbox("Concept", CONCEPTS)
		if st.button("Generate scenario", type="primary", use_container_width=True):
			st.session_state.active_concept = concept
			st.session_state.started = True
			st.session_state.feedback = None
			st.rerun()
	with progress:
		st.subheader("Your progress")
		st.markdown('<div class="metric"><div class="metric-label">CURRENT RUN</div><div class="metric-value">Not started</div></div>', unsafe_allow_html=True)
		st.markdown("\n")
		st.markdown('<div class="metric"><div class="metric-label">ATTEMPTS AVAILABLE</div><div class="metric-value">3</div></div>', unsafe_allow_html=True)

	if st.session_state.get("started"):
		active_concept = st.session_state.get("active_concept", concept)
		st.divider()
		st.markdown(f'<div class="eyebrow">Scenario / {active_concept}</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="scenario"><div class="scenario-title">Laboratory situation</div>{DEMO_SCENARIOS[active_concept]}</div>', unsafe_allow_html=True)
		st.subheader("Explain the why")
		response = st.text_area("Your reasoning", height=190, placeholder="What happened, why did it happen, and how does the procedure cause the result?", label_visibility="collapsed")
		if st.button("Submit reasoning", type="primary"):
			if response.strip():
				st.session_state.feedback = response
				st.rerun()
			else:
				st.warning("Write a response before submitting.")

		if st.session_state.get("feedback"):
			st.divider()
			st.subheader("Feedback preview")
			st.info("Your response has been received. The evaluator will return a quality rating, concise feedback, and a targeted hint here.")
			st.caption("Backend connection point: replace this preview with your teammates' evaluation result.")

		st.subheader("Attempt history")
		st.caption("Past responses will appear here after the evaluation service is connected.")


def professor_page():
	st.markdown('<div class="eyebrow">Review workspace</div>', unsafe_allow_html=True)
	st.title("Professor dashboard")
	st.markdown('<p class="intro">Review runs that need attention and inspect the reasoning behind each result.</p>', unsafe_allow_html=True)
	first, second, third = st.columns(3)
	with first:
		st.markdown('<div class="metric"><div class="metric-label">ACTIVE RUNS</div><div class="metric-value">12</div></div>', unsafe_allow_html=True)
	with second:
		st.markdown('<div class="metric"><div class="metric-label">PASSED TODAY</div><div class="metric-value">8</div></div>', unsafe_allow_html=True)
	with third:
		st.markdown('<div class="metric"><div class="metric-label">NEEDS REVIEW</div><div class="metric-value">3</div></div>', unsafe_allow_html=True)

	st.divider()
	st.subheader("Runs needing review")
	st.dataframe(
		{
			"Student": ["student_014", "student_009", "student_021"],
			"Concept": ["Gram staining", "Fermentation", "Protein purification"],
			"Attempts": [3, 3, 2],
			"Status": ["Flagged", "Flagged", "Retry"],
		},
		hide_index=True,
		use_container_width=True,
	)
	st.caption("Backend connection point: replace demo rows with persisted flag and attempt records.")


if "started" not in st.session_state:
	st.session_state.started = False
if "feedback" not in st.session_state:
	st.session_state.feedback = None

show_brand()
page = st.sidebar.radio("Workspace", ["Student", "Professor dashboard"], label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.caption("Interface prototype\nBackend integration pending")

if page == "Student":
	student_page()
else:
	professor_page()