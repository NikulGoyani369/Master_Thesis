from typing import Any
import streamlit as st
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
import glob
import os
import pandas as pd
import openai
import pymongo as mongo

openai.api_key = st.secrets['OPENAI_API_KEY']
client = mongo.MongoClient(**st.secrets["mongo"])
logoEnabled = False
submitted_first_form = False
submitted_feedback_form = False


def init_state():
    if 'count' not in st.session_state:
        st.session_state.count = 0
        st.session_state.answer = ''
        st.session_state.explanation = ''
        st.session_state.rating = ''
        st.session_state.student_explanation = ''


def after_submit():
    write_to_db(create_dict())
    clear_session_state()
    increment_counter()


def clear_session_state():
    st.session_state['answer'] = ''
    st.session_state['explanation'] = ''
    st.session_state['rating'] = ''
    st.session_state['student_explanation'] = ''


def write_to_db(dict_to_save):
    db = client.nlp_db
    csv_collection = db.csv_collection
    return csv_collection.insert_one(dict_to_save)


def create_dict():
    return {
        'question': [question],
        'student_answer': [st.session_state.answer],
        'correct_incorrect': [answerStat],
        'explanation': [st.session_state.explanation],
        'rating': [st.session_state.rating],
        'student_explanation': [st.session_state.student_explanation]
    }


def increment_counter():
    st.session_state.count += 1


def open_files():
    return glob.glob("./tmp/semeval2013-Task7-2and3way/*/2way/*/*.xml") + \
           glob.glob("./tmp/semeval2013-Task7-2and3way/test/2way/*/*/*.xml")


def find_question(data):
    soup = BeautifulSoup(data, "xml")
    question = soup.find('questionText').string
    return question


def find_correct_answers(data):
    soup = BeautifulSoup(data, "xml")
    answers = []
    for tag in soup.find_all('studentAnswer', accuracy="correct"):
        print(tag.string)
        answers.append(tag.string)
    print(answers)
    return answers


def get_logo_and_description():
    LOGO_URL = "https://www.ltl.uni-due.de/assets/images/logo3.png"
    description = """
<h2>Master Thesis Topic:- Collecting and analyse automatically generated feedback explanations</h2>
<p style='outline-style: solid;padding:10px;outline-color: green; font-size:16px; text-align: center; font-family:'Open Sans', sans-serif; '> <b>PROTECTION OF DATA:-</b><br>
<ol style='font-size:18px;font-family: "Source Sans Pro", sans-serif;'>
  <li>The owners of this website take the security of your personal information very seriously. We handle your personal data with confidentiality and in compliance with the applicable data protection laws and this data protection statement.</li>
  <li>Various personal data are gathered when you use this website. Personal data are pieces of information that may be used to identify you personally. This data protection statement outlines what information we gather and how we utilize it. It also discusses why and how this is accomplished.</li>
  <li>We'd like to emphasize that data transfer via the Internet (for example, while interacting through e-mail) may have security flaws. It is not feasible to completely secure data from unauthorized access.</li>
</ol>
</p>
"""
    return LOGO_URL, description


def get_explanation():
    return """
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


def call_openai(question, answer, target_answer):
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Question: {question}\nStudentAnswer: {answer}\nTargetAnswer: {target_answer}\nExplanation",
        temperature=1,
        max_tokens=64,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=2,
        stop=["\n"]
    )
    return response


def find_target_answer(answer, correct_answers):
    return "correct" if answer in correct_answers else "incorrect"


def load_first_form(data):
    question = find_question(data)
    LOGO_URL, description = get_logo_and_description()
    if logoEnabled:
        st.image(use_column_width=True, image=LOGO_URL)
        components.html(description, height=340, width=700, scrolling=True)
    st.markdown("___")
    with st.form("my_form"):
        st.write("Question")
        question_str = f"<p style='outline-style: solid;padding:10px;outline-color: green;'> {question}</p>"
        components.html(question_str)
        st.text_input("Answer", key='answer')
        global submitted_first_form
        submitted_first_form = st.form_submit_button("Submit", on_click=test_call)


def test_call():
    print("test")


def get_data(file):
    f = open(f'{file}', 'r')
    return f.read()


def get_files():
    FILEs = open_files()
    return FILEs


# @st.cache(suppress_st_warning=True)


def load_feedback_form(explanation, answer_stat, reference_answer):
    with st.container():
        save_exp_to_session(explanation)
        components.html(
            get_explanation().format(
                answerStatus=answer_stat,
                explanation=explanation,
                reference_ans=reference_answer
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
            st.radio("Select Rating", radioOptions, key='rating')

            st.text_area("Student Explanation", key='student_explanation')

            global submitted_feedback_form
            submitted_feedback_form = st.form_submit_button(
                "Next Question", on_click=after_submit)


def extract_explanation(response):
    return response['choices'][0]['text']


def save_exp_to_session(exp):
    st.session_state.explanation = exp


def find_reference_answer(data):
    soup = BeautifulSoup(data, "xml")
    return soup.find('referenceAnswer', category="BEST").string



def main():
    init_state()
    file = get_files()[0]
    data = get_data(file)
    load_first_form(data)
    if submitted_first_form:
        answer = st.session_state
        correct_answers = find_correct_answers(data)
        reference_answer = find_reference_answer(data)
        target_answer = find_target_answer(answer, correct_answers)
        response = call_openai(find_question(data), answer, target_answer)
        load_feedback_form(extract_explanation(response), target_answer, reference_answer)


if __name__ == '__main__':
    main()
