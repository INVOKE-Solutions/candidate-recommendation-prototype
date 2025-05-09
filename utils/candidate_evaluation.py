import streamlit as st
from openai import OpenAI

def evaluate_candidate(prompt_text: str, resume_text: str, job_text: str, model="gpt-4o-mini") -> str:
    
    """Evaluate the candidate's resume against the job description using OpenAI's API."""

    prompt_text = prompt_text.strip()
    resume_text = resume_text.strip()
    job_text = job_text.strip()

    if not all([prompt_text, resume_text, job_text]):
        st.error("Please fill in all fields.")
        raise ValueError("Please fill in all fields.")
    else:
        # Construct the prompt for OpenAI
        prompt = f"""
        {prompt_text}
        
        Resume:
        {resume_text}
        
        Job Description:
        {job_text}
        """

    client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])
    
    # Call OpenAI API to get the evaluation
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "user", 
                "content": prompt
            }
        ],
        temperature=0.5
    )
    
    # Extract and return the response text
    evaluation_result = response.output_text
    
    return evaluation_result