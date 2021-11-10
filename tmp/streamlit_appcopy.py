import glob
import streamlit as st
import openai
import pymongo as mongo
import streamlit.components.v1 as components
from bs4 import BeautifulSoup

COUNT = 'count'
STUDENT_EXPLANATION = 'student_explanation'
STUDENT_RATING = 'rating'

EXPLANATION_HTML = """
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@1,495&display=swap" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    
<div class="card mb-12 shadow-sm"   >
      <div class="card-body"  style='outline-style: solid;padding:10px;outline-color: blue;'>
        <h2 class="card-title">Result:</h2>
        Your answer is {answerStatus}.
    </div>
</div>
<br>
<div class="card mb-12 shadow-sm">
      <div class="card-body" style='outline-style: solid;padding:10px;outline-color: red;'>
        <h2 class="card-title">reference_answer:</h2>
        {reference_ans}
    </div>
</div>
<div class="card mb-12 shadow-sm" >
      <div class="card-body" style='outline-style: solid;padding:10px;outline-color: green;'>
        <h2 class="card-title">Explanation:</h2>
        {explanation}
    </div>
</div>
<br>
<div class="card mb-12 shadow-sm">
    <div class="card-header">
        <h3 style="float:center; font-size:20px; "class="text-muted">What do you think this explanation is good. Why not?</h3>
        <h3 style="float:center; font-size:20px; "class="text-muted">What do you think this explanation is good. Why not?</h3>
        <h3 style="float:center; font-size:20px; "class="text-muted">What do you think this explanation is good. Why not?</h3>
        <h3 style="float:center; font-size:20px; "class="text-muted">What do you think this explanation is good. Why not?</h3>
    </div>
</div>
"""

st.markdown("University Department:- [Language Technology Lab](https://www.ltl.uni-due.de)")

LOGO_URL = "https://www.ltl.uni-due.de/assets/images/logo3.png"

description = """
<h2>Master Thesis Topic:- Collecting and analyse automatically generated feedback explanations</h2>
<h3 style='font-weight: normal; font-family:'Open Sans', sans-serif;'>Contact Email-ID:- nikulkumar.goyani@stud.uni-due.de</h3>
<p style='outline-style: solid;padding:10px;outline-color: green; font-size:16px; text-align: center; font-family:'Open Sans', sans-serif; '> <b>PROTECTION OF DATA:-</b><br>
<ul style='font-size:18px;font-family: "Source Sans Pro", sans-serif;  text-align: justify;'>
  <li> The dataset comprises student replies to explanation and definition questions found in practise activities and exams. 
  The Student Response Analysis dataset is split into two parts: Beetle and SciEntsBank. 
  Answers to explanation and definition questions are meticulously labelled. The data set includes a sample question, reference answer, and student response.
  In this thesis, a human annotator classifies each student response as one of five evaluations. 
  We used the SRA dataset to build our dataset. </li> <br>
  <li> Original principle of this thesis is to take an answers from the student, which can then be classified as either correct or incorrect.
  Based on the student answers, generate an explanation of why the student's answer is incorrect or correct. Firstly, it is a machine-generated explanation by
  the model of Natural Language Processing (NLP). Finally, it asks the student to evaluate if the machine-generated explanation is viable or write a student explanation</li> <br>
  <li> Whatever data is provided in this survey will be taken into use only for this thesis work. The data will not be shared in any place. This data will remain completly anonymous</li>
</ul>
</p>
"""


def save_into_session(key, value):
    st.session_state[key] = value


def feedback_form_submitted():
    write_to_db(create_dict())
    increment_counter()
    clear_session_state()


def write_to_db(dict_to_save):
    db = client.nlp_db
    csv_collection = db.csv_collection
    return csv_collection.insert_one(dict_to_save)


def create_dict():
    return {
        'question': data['question'],
        'student_answer': data['student_answer'],
        'accuracy': data['accuracy'],
        'explanation': data['explanation'],
        'rating': st.session_state[STUDENT_RATING],
        'student_explanation': st.session_state[STUDENT_EXPLANATION]
    }


def increment_counter():
    st.session_state.count += 1


def clear_session_state():
    st.session_state[STUDENT_EXPLANATION] = ''
    st.session_state[STUDENT_RATING] = '1 Star'
    print(st.session_state)


# def get_list_of_file_names():
#     return glob.glob("./tmp/semeval2013-Task7-2and3way/*/2way/*/*.xml") + \
#            glob.glob("./tmp/semeval2013-Task7-2and3way/test/2way/*/*/*.xml")


def create_question_string():
    st.write("Question :-")
    return f"<p style='outline-style: solid;padding:10px;outline-color: green;'> {data['question']}</p>"


def load_student_question_form():
    components.html(question_str)
    st.write("Student Answer :")
    st.text_area("", value=data['student_answer'])
    components.html(
        EXPLANATION_HTML.format(
            answerStatus=data['accuracy'],
            explanation=data['explanation'],
            reference_ans=data['ref_answer']
        ),
        height=500,
        scrolling=True
    )
    st.write(
        '<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    st.write(
        '<style>div.row-widget.stButton > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    radioOptions = ['1 Star', '2 Star', '3 Star', '4 Star', '5 Star']

    with st.form("form", clear_on_submit=True):
        st.radio("Select Rating", radioOptions, key=STUDENT_RATING)
        st.text_area("Student Explanation", key=STUDENT_EXPLANATION)
        st.form_submit_button(
            "Next Question", on_click=feedback_form_submitted)


def initialize_session_state():
    st.session_state[COUNT] = 1
    st.session_state[STUDENT_RATING] = '1 Star'
    st.session_state[STUDENT_EXPLANATION] = ''


def initialize_few_session_state():
    st.session_state[STUDENT_RATING] = '1 Star'
    st.session_state[STUDENT_EXPLANATION] = ''


# main routine
openai.api_key = st.secrets['OPENAI_API_KEY']
client = mongo.MongoClient(**st.secrets["mongo"])
enableLogo = True

if COUNT not in st.session_state:
    initialize_session_state()
else:
    initialize_few_session_state()

# read the created dataset file
file = open("./tmp/open_ai_questions_final.csv", encoding='utf-8')
lines = file.readlines()
line = lines[st.session_state[COUNT]]

row = line.split('|')
data = {
    'question': row[0],
    'ref_answer': row[1],
    'student_answer': row[2],
    'accuracy': row[3],
    'explanation': row[4],
}

if enableLogo:
    st.image(use_column_width=True, image=LOGO_URL)
    components.html(description, height=340, width=700, scrolling=True)

st.markdown("___")
question_str = create_question_string()
load_student_question_form()
