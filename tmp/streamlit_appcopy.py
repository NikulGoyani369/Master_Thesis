import glob
import streamlit as st
import openai
import pymongo as mongo
import streamlit.components.v1 as components
from bs4 import BeautifulSoup

STUDENT_ANSWER = 'student_answer'
QUESTION = 'question'
ANSWER_STATE = 'answer_state'
ANSWER = 'answer'
REF_ANSWER = 'ref_answer'
COUNT = 'count'
OPEN_AI_EXPLANATION = 'explanation'
STUDENT_EXPLANATION = 'student_explanation'
STUDENT_RATING = 'rating'
STUDENT_FORM_SUBMITTED = 'student_form_submitted'

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
        <h3 style="float:center; font-size:20px; "class="text-muted">What do you think this explanation is good. Why not?<br>Below write your explanation.</h3>
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
  <li>The dataset comprises student replies to explanation and definition questions found in practise activities and exams. 
  The Student Response Analysis dataset is split into two parts: Beetle and SciEntsBank. 
  Answers to explanation and definition questions are meticulously labelled. The data set includes a sample question, reference answer, and student response.
  In this thesis, a human annotator classifies each student response as one of five evaluations. 
  We used the SRA dataset to build our dataset. </li> <br>
  <li> Original principle of this thesis is to take an answers from the student, which can then be classified as either correct or incorrect.
  Based on the student answers, generate an explanation of why the student's answer is incorrect or correct. Firstly, it is a machine-generated explanation by
  the model of Natural Language Processing (NLP). Finally, it asks the student to evaluate if the machine-generated explanation is viable or write a student explanation</li> <br>
  <li>Whatever data is provided in this survey will be taken into use only for this thesis work. The data will not be shared in any place. This data will remain completly anonymous</li>
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
        'question': st.session_state[QUESTION],
        'student_answer': st.session_state[STUDENT_ANSWER],
        'correct_incorrect': st.session_state[ANSWER_STATE],
        'explanation': st.session_state[OPEN_AI_EXPLANATION],
        'rating': st.session_state[STUDENT_RATING],
        'student_explanation': st.session_state[STUDENT_EXPLANATION]
    }


def increment_counter():
    st.session_state.count += 1


def clear_session_state():
    st.session_state[ANSWER] = ''
    st.session_state[REF_ANSWER] = ''
    st.session_state[ANSWER_STATE] = ''
    st.session_state[STUDENT_EXPLANATION] = ''
    st.session_state[OPEN_AI_EXPLANATION] = ''
    st.session_state[STUDENT_ANSWER] = ''
    st.session_state[STUDENT_RATING] = '1 Star'
    st.session_state[STUDENT_FORM_SUBMITTED] = False
    st.session_state[QUESTION] = ''
    print(st.session_state)


def get_list_of_file_names():
    return glob.glob("./tmp/semeval2013-Task7-2and3way/*/2way/*/*.xml") + \
           glob.glob("./tmp/semeval2013-Task7-2and3way/test/2way/*/*/*.xml")


def get_question():
    return soup.find('questionText').string


def get_explaination_from_responce():
    return response['choices'][0]['text']


def find_answers():
    tags = []
    for tag in soup.find_all('studentAnswer', accuracy="correct"):
        tags.append(tag.string)
    return tags


def create_question_string():
    return f"<p style='outline-style: solid;padding:10px;outline-color: green;'> {st.session_state[QUESTION]}</p>"


def get_reference_ans():
    return soup.find('referenceAnswer', category="BEST").string


def find_target_answer():
    return "correct" if st.session_state[STUDENT_ANSWER] in answers else "incorrect"


def student_form_submitted():
    save_into_session(STUDENT_FORM_SUBMITTED, True)


def load_feedback_form():
    with st.container():
        components.html(
            EXPLANATION_HTML.format(
                answerStatus=st.session_state[ANSWER_STATE],
                explanation=st.session_state[OPEN_AI_EXPLANATION],
                reference_ans=st.session_state[REF_ANSWER]
            ),
            height=500,
            scrolling=True
        )
        st.write(
            '<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        st.write(
            '<style>div.row-widget.stButton > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        with st.form("feedbackform"):
            radioOptions = ['1 Star', '2 Star', '3 Star', '4 Star', '5 Star']
            st.radio("Select Rating", radioOptions, key=STUDENT_RATING)

            st.text_area("Student Explanation", key=STUDENT_EXPLANATION)

            st.form_submit_button(
                "Next Question", on_click=feedback_form_submitted)


def load_student_question_form():
    with st.container():
        with st.form(key="my_form"):
            components.html(question_str)
            st.text_area("Answer", value='', key=STUDENT_ANSWER)
            st.form_submit_button(
                "Submit", on_click=student_form_submitted)


def get_openai_response():
    return openai.Completion.create(
        engine="davinci",
        prompt=f"Question: {question_str}\nStudentAnswer: {st.session_state[STUDENT_ANSWER]}\nTargetAnswer: {target_answer}\nExplanation",
        temperature=1,
        max_tokens=64,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=2,
        stop=["\n"]
    )


def initialize_session_state():
    st.session_state[COUNT] = 0
    st.session_state[ANSWER_STATE] = ''
    st.session_state[ANSWER] = ''
    st.session_state[REF_ANSWER] = ''
    st.session_state[QUESTION] = ''
    st.session_state[OPEN_AI_EXPLANATION] = ''
    st.session_state[STUDENT_RATING] = '1 Star'
    st.session_state[STUDENT_EXPLANATION] = ''
    st.session_state[STUDENT_ANSWER] = ''
    st.session_state[STUDENT_FORM_SUBMITTED] = False


def initialize_few_session_state():
    st.session_state[ANSWER_STATE] = ''
    st.session_state[ANSWER] = ''
    st.session_state[REF_ANSWER] = ''
    st.session_state[QUESTION] = ''
    st.session_state[OPEN_AI_EXPLANATION] = ''
    st.session_state[STUDENT_RATING] = '1 Star'
    st.session_state[STUDENT_EXPLANATION] = ''
    st.session_state[STUDENT_ANSWER] = ''


# main routine
openai.api_key = st.secrets['OPENAI_API_KEY']
client = mongo.MongoClient(**st.secrets["mongo"])
enableLogo = True

if 'count' not in st.session_state:
    initialize_session_state()
else:
    initialize_few_session_state()

files = get_list_of_file_names()

try:
    f = open(f'{files[st.session_state.count]}', 'r')
    data = f.read()
except IndexError:
    st.session_state.count = 0
    f = open(f'{files[st.session_state.count]}', 'r')
    data = f.read()

soup = BeautifulSoup(data, "xml")

answers = find_answers()
question = get_question()
save_into_session(QUESTION, question)

if enableLogo:
    st.image(use_column_width=True, image=LOGO_URL)
    components.html(description, height=340, width=700, scrolling=True)

st.markdown("___")
question_str = create_question_string()
load_student_question_form()

target_answer = find_target_answer()
response = get_openai_response()

if st.session_state[STUDENT_FORM_SUBMITTED]:
    explanation = get_explaination_from_responce()
    ref_answer = get_reference_ans()
    save_into_session(OPEN_AI_EXPLANATION, explanation)
    save_into_session(REF_ANSWER, ref_answer)
    save_into_session(ANSWER_STATE, target_answer)

    load_feedback_form()
