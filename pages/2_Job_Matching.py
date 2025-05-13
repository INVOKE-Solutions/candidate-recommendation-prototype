import streamlit as st
from utils.auth import authenticate_user
from utils.candidate_evaluation import evaluate_candidate

st.set_page_config(
    page_title='CV Parser',
    layout="centered",    
    initial_sidebar_state="auto"
    )

st.title("Job Matching")
st.caption("Evaluate a candidate's resume against a job description using LLM.")

authenticate_user()

if "resume_text" not in st.session_state:
    st.session_state["resume_text"] = None

if "job_text" not in st.session_state:
    st.session_state["job_text"] = None

resume_text = st.text_area("📄 Candidate Resume",value=st.session_state.get("cv_parsed_result", ""), height=300, placeholder="Paste the candidate's resume here...")

job_text = st.text_area("📌 Job Requirements", value=st.session_state.get("job_text", ""), height=300, placeholder="Paste the job description here...")

if job_text:
    st.session_state["job_text"] = job_text

prompt_text = st.text_area("✍️ Custom Prompt for ChatGPT", value=st.session_state.get("prompt_text", ""), height=300)

if prompt_text:
    st.session_state["prompt_text"] = prompt_text

if "job_matching_result" not in st.session_state:
    st.session_state["job_matching_result"] = None

model = st.selectbox(
    "Select GPT model to use",
    ("gpt-4o-mini", "gpt-4o", "gpt-4.1-mini")
)

st.session_state['model'] = model

if st.button("🚀 Evaluate Candidate"):
    with st.spinner("Evaluating..."):

        result = evaluate_candidate(
            prompt_text=prompt_text,
            resume_text=resume_text,
            job_text=job_text,
            model=st.session_state.get('model', 'gpt-4o-mini')
        )

        st.session_state["job_matching_result"] = result
        st.success("Evaluation completed!")
        st.text_area("Evaluation Result", value=result, height=300)