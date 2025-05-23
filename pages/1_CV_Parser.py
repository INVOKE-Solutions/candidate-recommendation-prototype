import streamlit as st
from utils.auth import authenticate_user
from utils.cv_parser import extract_text_from_cv

# Set the page configuration
st.set_page_config(
    page_title='CV Parser',
    layout="centered",    
    initial_sidebar_state="auto"
    )

st.title("CV Parser")
st.caption("Parse a candidate's resume using LLM.")

# Authenticate the user
authenticate_user()

# File uploader for CV
cv_file = st.file_uploader(label="Upload CV", type=["pdf"])

# Initialize session state for parsed result
if "cv_parsed_result" not in st.session_state:
    st.session_state["cv_parsed_result"] = None

if cv_file is not None:

    cv_parser_prompt = st.text_area("Custom prompt for parsing CV", height=300, placeholder="Enter your custom prompt here. Leave it empty to use the default prompt.")
    
    if cv_parser_prompt:
        st.session_state["cv_parser_prompt"] = cv_parser_prompt
    
    if st.button("Parse CV"):
    
        with st.spinner("Parsing CV..."):

            result = extract_text_from_cv(cv_file)
            
            st.session_state["cv_parsed_result"] = result
            st.success(f"CV parsed successfully!")


st.text_area("Parsed CV", value=st.session_state.get("cv_parsed_result", ""), height=300, placeholder="Parsed CV will appear here...")