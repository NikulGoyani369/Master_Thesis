import streamlit as st
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
import glob
import os
import pandas as pd
import openai
# openai.organization = 'org-5p4uM0nHTES2niAIq4uMldR6'
openai.api_key = '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'


# openai.api_key = os.getenv('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')


if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.student_explanat = 'first time'
    st.session_state.st = 'first time'


def increment_counter():
    st.session_state.count += 1
    st.session_state.answer = ''
    st.session_state.student_explanat = st.session_state.student_explanation
    st.session_state.st = st.session_state.star


# FILEs = glob.glob("/Users/Nikul/Downloads/inner/inner/semeval2013-Task7-2and3way/*/2way/*/*.xml") + \
#     glob.glob(
#         "/Users/Nikul/Downloads/inner/inner/semeval2013-Task7-2and3way/test/2way/*/*/*.xml")

# this parth for Live searver
FILEs = glob.glob("./semeval2013-Task7-2and3way/*/2way/*/*.xml") + \
    glob.glob("./semeval2013-Task7-2and3way/test/2way/*/*/*.xml")


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

description = """
<p style='outline-style: solid;padding:10px;outline-color: green;'>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum</p
"""

resultAndExplanationHTML = """
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>


<div class="card mb-12 shadow-sm">
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
<div class="card mb-12 shadow-sm">
      <div class="card-body" style='outline-style: solid;padding:10px;outline-color: green;'>
        <h2 class="card-title">Explanation:</h2>
        {explanation}
    </div>
</div>
<br>
<h3>Below we will ask student to evaluate the generated model explanation </h3>
<div class="card mb-12 shadow-sm">
    <div class="card-header">
        <h3 style="float:center; font-size:20px; "class="text-muted">What do you think this explanation is good. Why not?<br>Below write your explanation.</h3>
    </div>
</div>
"""


st.markdown("___")
with st.form("my_form"):
    st.subheader('Below we will show the all questions come form dataset')
    st.write("Question")
    question = f"<p style='outline-style: solid;padding:10px;outline-color: green;'> {Ques}</p>"
    Q = Ques
    components.html(question)
    st.subheader('Below student will write their answers')
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
        prompt=f"Question: {Ques}\nStudentAnswer: {st.session_state.answer}\nTargetAnswer: {realans[0]}\nCorrect or Incorrect Explanation:",
        temperature=1,
        max_tokens=64,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=2,
        stop=["\n"]
    )


def load_feedback_form():
    with st.container():
        st.subheader(
            'Below we will show the Target_answer and result from a dataset with an explanation generated from the NLP model')
        explanation = response['choices'][0]['text']

        components.html(resultAndExplanationHTML.format(answerStatus=answerStat,
                        explanation=explanation, reference_ans=realans[0]), height=500, scrolling=True)
        st.write(
            '<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        st.write(
            '<style>div.row-widget.stButton > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        with st.form("feedbackform"):
            radioOptions = ['1 Star', '2 Star', '3 Star', '4 Star', '5 Star']
            # radioOptions = ['10 Star', '9 Star', '8 Star', '7 Star', '6 Star', '5 Star', '4 Star', '3 Star', '2 Star',
            #                 '1 Star']
            st.radio("Select Rating", radioOptions, key='star')

            st.text_area("Student Explanation", key='student_explanation')
            feedbackFormSubmission = st.form_submit_button(
                "Next Question", on_click=increment_counter)
        df = pd.read_csv('j.csv')
        # st.write(f'{student_explanation,star}')
        df2 = {'Question': Ques, 'student_answer': st.session_state.answer, 'correct_incorrect': answerStat,
               'explanation': explanation, 'rating': st.session_state.st, 'student_explanation': st.session_state.student_explanat}
        df.append(df2, ignore_index=True).to_csv('j.csv', index=False)


if isSubmitted:
    load_feedback_form()