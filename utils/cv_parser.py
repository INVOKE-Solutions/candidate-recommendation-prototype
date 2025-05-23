import streamlit as st
from pypdf import PdfReader
from openai import OpenAI
import io
from typing import Optional


def format_text(parsed_text: str, prompt_text: Optional[str] = None) -> str:
    """
    Format the text in JSON using LLM.
    """
    client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

    if not prompt_text:
        # Default prompt if none is provided

        prompt_text = f"""
                    Example of the JSON format:
                    
                    "skills": "List of skills in comma-separated format",
                    "education": 
                        "course": "Degree or Course Name",
                        "institution": "Institution Name",
                        "startYear": "Start year",
                        "endYear": "End year. If unspecified, use 'Present'",
                        "cgpa": "CGPA or Percentage"
                        ,
                    "experience": 
                        "company: "Company Name",
                        "role": "Job Title",
                        "startDate": "Start date",
                        "endDate": "End date. If unspecified, use 'Present'",
                        "skills": "Skills used in this role",
                        "description": "Job description"
                    
                    Extract candidate's information from the following text and map it to the above JSON format.
                    Ensure to extract the following fields:
                    - skills
                    - education (course, institution, startYear, endYear, cgpa)
                    - experience (company, role, startDate, endDate, skills, description)
                    
                    CV text:
                    {parsed_text}
    """
    else:
        # Use the provided prompt text
        prompt_text = f"""
                    {prompt_text}
                    
                    CV text:
                    {parsed_text}
    """
    
    # Call OpenAI API to get the evaluation
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system", 
                "content": "You are a sophisticated CV parsing AI tasked to parse a candidate's CV and extract the relevant information. Please ensure to format the output in JSON format. Do not include any additional text or explanations."
            },
            {
                "role": "user", 
                "content": prompt_text
            }
        ],
        temperature=0.5
    )
    cv_json = response.output_text

    return cv_json

def extract_text_from_cv(cv_file:str) -> str:
    """
    Extract text from the uploaded CV file.
    """
    try:
        # Read the file in binary mode
        cv_binary = io.BytesIO(cv_file.read())

        # Extract text from PDF
        reader = PdfReader(cv_binary)

        # Initialize an empty string to store the extracted text
        extracted_text = ""

        # Loop through each page and extract text
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"
        
        # Format the extracted text using LLM
        formatted_text = format_text(extracted_text)
        
        return formatted_text
    
    except Exception as e:
        st.error(f"Error processing the PDF file: {e}")


