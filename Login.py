import streamlit as st
import logging
from utils.auth import authenticate_user
# --------------------Configure logging--------------------


# Configure logging
logging.basicConfig(filename="user_login.log", level=logging.INFO, 
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

_left, middle, _right = st.columns([0.5, 1, 0.5])

with middle:
    st.image("photos/puzzle_match.gif")

# --------------------Start main page--------------------

def main():
    st.title("adnexio Job Matching Playground")
    st.caption("Evaluate a candidate's resume against a job using LLM.")
    
    # Authenticate user
    authenticate_user()

    st.write("""
    ## How to use this app:
    1. **Login**: Use your credentials to log in.
    2. **Upload CV**: Go to the CV Parser page and upload a candidate's resume (in pdf format).
    3. **Job Matching**: Go to the Job Matching page and paste the job description.
    4. **Evaluate**: Click on the "Evaluate Candidate" button to get the evaluation result. You may choose a different model from the dropdown.
    5. **View Results**: The evaluation result will be displayed in the text area.
    6. **Logout**: Use the logout button to exit the app.
             """) 

if __name__ == "__main__":
    main()