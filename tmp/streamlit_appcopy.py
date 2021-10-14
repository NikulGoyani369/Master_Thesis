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


if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.answer = ''
    st.session_state.explanation = ''
    st.session_state.rating = ''
    st.session_state.student_explanation = ''


def after_submit():
    write_to_db(create_dict())
    increment_counter()


def write_to_db(dict_to_save):
    db = client.nlp_db
    csv_collection = db.csv_collection
    return csv_collection.insert_one(dict_to_save)


def create_dict():
    return {
        'question': [Ques],
        'student_answer': [st.session_state.answer],
        'correct_incorrect': [answerStat],
        'explanation': [st.session_state.explanation],
        'rating': [st.session_state.rating],
        'student_explanation': [st.session_state.student_explanation]
    }


def increment_counter():
    st.session_state.count += 1
    st.session_state.answer = ''
    st.session_state.student_explanation = ''
    st.session_state.rating = '1 Star'


def for_server():
    return glob.glob("./tmp/semeval2013-Task7-2and3way/*/2way/*/*.xml") + \
        glob.glob("./tmp/semeval2013-Task7-2and3way/test/2way/*/*/*.xml")


FILEs = for_server()


try:
    f = open(f'{FILEs[st.session_state.count]}', 'r')
    data = f.read()
except IndexError:
    st.session_state.count = 0
    f = open(f'{FILEs[st.session_state.count]}', 'r')
    data = f.read()

# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object
Bs_data = BeautifulSoup(data, "xml")

# Finding all instances of tag
# `unique`
b_unique = Bs_data.find_all('questionText')
Anse = Bs_data.find_all('studentAnswer', accuracy="correct")
sub1 = "<questionText>"
sub2 = '</questionText>'
# getting index of substrings
idx1 = str(b_unique[0]).index(sub1)
idx2 = str(b_unique[0]).index(sub2)
# length of substring 1 is added to
# get string from next character
Ques = str(b_unique[0])[idx1 + len(sub1): idx2]
currentCsvLine = ""

# LOGO_URL = "https://www.ltl.uni-due.de/assets/images/logo3.png"
# description = """
# <h2>Master Thesis Topic:- Collecting and analyse automatically generated feedback explanations</h2>
# <p style='outline-style: solid;padding:10px;outline-color: green; font-size:16px; text-align: center; font-family:'Open Sans', sans-serif; '> <b>PROTECTION OF DATA:-</b><br>
# <ol style='font-size:18px;font-family: "Source Sans Pro", sans-serif;'>
#   <li>The owners of this website take the security of your personal information very seriously. We handle your personal data with confidentiality and in compliance with the applicable data protection laws and this data protection statement.</li>
#   <li>Various personal data are gathered when you use this website. Personal data are pieces of information that may be used to identify you personally. This data protection statement outlines what information we gather and how we utilize it. It also discusses why and how this is accomplished.</li>
#   <li>We'd like to emphasize that data transfer via the Internet (for example, while interacting through e-mail) may have security flaws. It is not feasible to completely secure data from unauthorized access.</li>
# </ol>
# </p>
# """

resultAndExplanationHTML = """
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

# st.image(use_column_width=True, image=LOGO_URL)
# components.html(description, height=340, width=700, scrolling=True)

st.markdown("___")
with st.form("my_form"):
    # st.subheader('Below we will show the all questions come form dataset')
    st.write("Question")
    question = f"<p style='outline-style: solid;padding:10px;outline-color: green;'> {Ques}</p>"
    Q = Ques
    components.html(question)
    # st.subheader('Below student will write their answers')
    st.text_input("Answer", key='answer')
    isSubmitted = st.form_submit_button("Submit")

    # Every form must have a submit button.
    realans = []
    for i in Anse:
        sub1 = ">"
        sub2 = '</studentAnswer>'
        # getting index of substrings
        idx1 = str(i).index(sub1)
        idx2 = str(i).index(sub2)
        # length of substring 1 is added to
        # get string from next character
        res = str(i)[idx1 + len(sub1): idx2]
        realans.append(res)
    if st.session_state.answer in realans:
        answerStat = "correct"
    elif st.session_state.answer not in realans:
        answerStat = "incorrect"
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Question: {Ques}\nStudentAnswer: {st.session_state.answer}\nTargetAnswer: {realans[0]}\nExplanation",
        temperature=1,
        max_tokens=64,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=2,
        stop=["\n"]
    )

# @st.cache(suppress_st_warning=True)


def load_feedback_form():
    with st.container():

        explanation = response['choices'][0]['text']
        save_exp_to_session(explanation)
        components.html(
            resultAndExplanationHTML.format(
                answerStatus=answerStat,
                explanation=explanation,
                reference_ans=realans[0]
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

            st.form_submit_button(
                "Next Question", on_click=after_submit)


def save_exp_to_session(exp):
    st.session_state.explanation = exp


if isSubmitted:
    load_feedback_form()
