from openai import OpenAI
import streamlit as st
from utils.auth import authenticate_user
from utils.candidate_evaluation import evaluate_candidate
import logging

# Disable SSL certificate verification
# os.environ.pop("SSL_CERT_FILE", None)

# Configure logging
logging.basicConfig(filename="user_prompts.log", level=logging.INFO, 
                    format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# --------------------Page configuration--------------------

st.set_page_config(
    page_title='adnexio Job Matching Playground',
    layout="centered",    
    initial_sidebar_state="auto"
)

hide_streamlit_style = """
            <style>
            header {visibility: hidden;}
            footer {visibility: hidden;}
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem; padding-bottom: 4rem;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

_left, _mid_left, middle, _mid_right, _right = st.columns([0.1, 0.1, 0.1, 0.1, 0.1])

with middle:
    st.image("photos/puzzle_match.gif")

# --------------------Start main page--------------------

def main():
    st.title("adnexio Job Matching Playground")
    st.caption("Evaluate a candidate's resume against a job description using LLM.")
    
    # Authenticate user
    authenticate_user()

    # col1, col2 = st.columns(2)


    resume_text = st.text_area("📄 Candidate Resume", height=300, placeholder="Paste the candidate's resume here...")

    job_text = st.text_area("📌 Job Requirements", height=300, placeholder="Paste the job description here...")

    prompt_text = st.text_area("✍️ Custom Prompt for ChatGPT", height=300)

    # Select which model to use
    model = st.selectbox(
        "Select GPT model to use",
        ("gpt-4o-mini", "gpt-4o", "gpt-4.1-mini")
        )

    if "result" not in st.session_state:
        st.session_state["result"] = None

    if st.button("🚀 Evaluate Candidate"):
        with st.spinner("Evaluating..."):

            result = evaluate_candidate(
                prompt_text=prompt_text,
                resume_text=resume_text,
                job_text=job_text,
                model=model
            )

            st.session_state["result"] = result
            st.success("Evaluation completed!")
            st.text_area("Evaluation Result", value=result, height=300)

if __name__ == "__main__":
    main()

    