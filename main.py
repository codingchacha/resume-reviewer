import streamlit as st
from pypdf import PdfReader
from groq import Groq
import os
#from dotenv import load_dotenv

#load_dotenv()

#setting up groq client
client = Groq(api_key=os.environ.get("API_KEY"))

#getting text from pdf file
def extract_text_from_pdf(file_path):
    pdf_reader = PdfReader(file_path)
    text = ""
    size = 0
    for page in pdf_reader.pages:
        size += 1
        text += page.extract_text()
    return text + f"\nThis resume size is {size} pages"




def call_model(jd , resume):
    chat_history = [{"role":"system" , "content":"you are a resume reviewer , review resume based on job description and also look for general mistakes also , like for someone less than 8 years experience - resume should be single page , you will get the page size in the last line of the user's text do not try to calculate yourself . also give a score out of 10"}]
    chat_history.append({"role":"user" , "content": f"job description: {jd} , resume: {resume}"})
    chat_completion = client.chat.completions.create(messages=chat_history , model="meta-llama/llama-4-scout-17b-16e-instruct" ,temperature=0.7,
    top_p=0.95,)
    response = chat_completion.choices[0].message.content
    return response
    
    



#frontend
st.markdown("""
<h1 style='text-align: center; color: #4CAF50;'>📄 Resume Review App</h1>
<h3 style='text-align: center;'>🔍 Connecting Talent with Opportunity</h3>
<p style='text-align: center;'>Upload your resume and job description to get AI-powered feedback, a resume score, and actionable suggestions.</p>
<hr style="border:1px solid #eee">
""", unsafe_allow_html=True)
job_description = st.text_area("Job description", height=200)
resume_file = st.file_uploader("Upload your resume", type=["pdf"])
if st.button("Submit"):
    if job_description and resume_file:
        with open("resume.pdf", "wb") as f:
            f.write(resume_file.getbuffer())
        text = extract_text_from_pdf("resume.pdf")
        response = call_model(job_description, text)
        st.success(response)
    else:
        st.warning("Please provide both job description and resume")
        st.markdown("""<style>
        .reportview-container .main .block-container{
            max-width: 90%;
            padding-top: 5px;
            padding-right: 5px;
            padding-left: 5px;
            padding-bottom: 10px;
        }
        </style>""", unsafe_allow_html=True)
        st.markdown("""<style>
        .reportview-container .main .block-container{
            max-width: 90%;
            padding-top: 5px;
            padding-right: 5px;
            padding-left: 5px;
            padding-bottom: 10px;
        }
        .reportview-container .main footer{
            visibility: hidden;
        }
        .reportview-container .main footer:after{
            content:'Developed by Tabish Mazhari'; 
            visibility: visible;
            display: block;
            text-align: center;
            color: grey;
            padding: 5px;
            }
        </style>""", unsafe_allow_html=True)












