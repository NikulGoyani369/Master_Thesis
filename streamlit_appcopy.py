import streamlit as st
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
import glob
import os
import pandas as pd
import openai
# openai.organization = 'org-5p4uM0nHTES2niAIq4uMldR6'
# openai.api_key = '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'
openai.api_key =  st.secrets['OPENAI_API_KEY']


if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.student_explanat = 'first time'
    st.session_state.st = 'first time'


def increment_counter():
    st.session_state.count += 1
    st.session_state.answer = ''
    st.session_state.student_explanat = st.session_state.student_explanation
    st.session_state.st = st.session_state.star

# this parth for local machine
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

st.image(use_column_width=True, image=LOGO_URL)
components.html(description, height=340, width=700, scrolling=True)

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

# @st.cache(suppress_st_warning=True)


def load_feedback_form():
    with st.container():
        explanation = response['choices'][0]['text']
        st.subheader(
            'Below we will show the Target_answer and result from a dataset with an explanation generated from the NLP model')
        
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
        df = pd.read_csv("/tmp/j.csv")
        # st.write(f'{student_explanation,star}')
        df2 = {'Question': Ques, 'student_answer': st.session_state.answer, 'correct_incorrect': answerStat,
               'explanation': explanation, 'rating': st.session_state.st, 'student_explanation': st.session_state.student_explanat}
        df.append(df2, ignore_index=True).to_csv("/tmp/j.csv", index=False)


if isSubmitted:
    load_feedback_form()


# Commented out HTML BASED Feedback form, Not in use currently but was made in case we need to convert it into react component.

    #     feedbackForm = """
    #     <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    # <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    # <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    #     <form>
    #     <label class="radio-inline">
    #       <input type="radio" name="optradio" checked>10 Star
    #     </label>
    #     <label class="radio-inline">
    #       <input type="radio" name="optradio">9 Star
    #     </label>
    #     <label class="radio-inline">
    #       <input type="radio" name="optradio">8 Star
    #     </label>
    #             <label class="radio-inline">
    #       <input type="radio" name="optradio">7 Star
    #     </label>
    #             <label class="radio-inline">
    #       <input type="radio" name="optradio">6 Star
    #     </label>
    #             <label class="radio-inline">
    #       <input type="radio" name="optradio">5 Star
    #     </label>
    #             <label class="radio-inline">
    #       <input type="radio" name="optradio">4 Star
    #     </label>
    #             <label class="radio-inline">
    #       <input type="radio" name="optradio">3 Star
    #     </label>
    #     <label class="radio-inline">
    #       <input type="radio" name="optradio">2 Star
    #     </label>
    #     <label class="radio-inline">
    #       <input type="radio" name="optradio">1 Star
    #     </label>
    #     <br>
    #
    #     <div class="card mb-12 shadow-sm" >
    #   <div class="card-body" style='outline-style: solid;padding:10px;outline-color: green;'>
    #     <h4 class="card-title">Your Explanation:</h4>
    #     <textarea class="form-control"></textarea>
    #   </div>
    #     </div>
    #   </form>"""
    #
    #     # my_component = components.html(feedbackForm, height=500)

    # `my_component`'s return value is the data returned from the frontend.
    # st.write("Value = ", my_component)
