import csv
import random

import openai
import pymongo as mongo
import streamlit as st
import streamlit.components.v1 as components

COUNT = 'count'
# STUDENT_EXPLANATION = 'student_explanation'
STUDENT_RATING = 'rating'
STUDENT_EVALUTION_QUESITON1 = 'What do you think about the generated explanation?'
STUDENT_EVALUTION_QUESITON2 = 'Does the generated explanation convey meaning of the original text?',
STUDENT_EVALUTION_QUESITON3 = 'How useful did you find the generated explanation?',
STUDENT_EVALUTION_QUESITON4 = 'Is there an alternative explanation that solves the same problem?',
STUDENT_EVALUTION_QUESITON5 = 'Does the generated explanation is readable?',
STUDENT_EVALUTION_QUESITON6 = 'What is wrong with this generated explanation?',

EXPLANATION_HTML = """
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@1,495&display=swap" rel="stylesheet">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400&display=swap" rel="stylesheet">
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    
<div class="card mb-12 shadow-sm border-primary">
      <div class="card-body"  style='font-size:20px; text-align: justify; class=text-muted;'>
        <h2 class="card-title"> Result :</h2>
        Your answer is {answerStatus}.
    </div>
</div>
<br>
<div class="card mb-12 shadow-sm border-primary style="margin-top: 60px;">
      <div class="card-body" style='font-size:20px; text-align: justify; class=text-muted;'>
        <h2 class="card-title">Reference Answer :</h2>
        {reference_ans}
    </div>
</div>
<br>
<div class="card mb-12 shadow-sm  border-primary">
      <div class="card-body" style='font-size:20px;text-align: justify; class=text-muted;'>
        <h2 class="card-title"> Generated Explanation :</h2>
        {explanation}
    </div>
</div>
"""
EVOLUTION_HTML = """
<div class="card border-primary">
<div class="card mb-12 shadow-sm border-primary">
    <div class="card-header">
    <div class="card-body" style='font-size:20px;text-align: justify; class=text-muted;font-family: 'IBM Plex Sans', sans-serif;'>
         <h3 class="card-title" style="text-align: justify; class=text-muted;font-family: 'IBM Plex Sans', sans-serif; float:center; font-size:20px;"> For the generated explanation, read the below questions, and you could do the Evaluation based on rating and write your feedback in the section below.</h3>
    </div>
        <ul style=" font-family: 'IBM Plex Sans', sans-serif;float:center;">
            <li><p style="float:center; font-size:20px;text-align: justify; class=text-muted;">What do you think about the generated explanation?  Good or Bad? </p></li>
            <li><p style="float:center; font-size:20px;text-align: justify; class=text-muted;">Does the generated explanation convey meaning of the original text?</p></li>
            <li><p style="float:center; font-size:20px;text-align: justify; class=text-muted;">How useful did you find the generated explanation?</p></li>
            <li><p style="float:center; font-size:20px;text-align: justify; class=text-muted;">Is generated explanation easy to understand?</p></li>
            <li><p style="float:center; font-size:20px;text-align: justify; class=text-muted;">Does the generated explanation is readable?</p></li>
            <li><p style="float:center; font-size:20px;text-align: justify; class=text-muted;">What is wrong with this generated explanation?</p></li>
        </ul>
    </div>
</div>
</div>
"""

st.markdown("University Department:- [Language Technology Lab](https://www.ltl.uni-due.de)")

LOGO_URL = "https://www.ltl.uni-due.de/assets/images/logo3.png"

description = """
<h2 style='font-family: 'IBM Plex Sans', sans-serif;'>Master Thesis Topic:- Collecting and analyse automatically generated feedback explanations.</h2>
<h3 style='font-weight: normal; font-family: 'IBM Plex Sans', sans-serif;'>Contact Email-ID:- nikulkumar.goyani@stud.uni-due.de</h3>
<p style='outline-style: solid;padding:10px;outline-color: rgba(170, 50, 220, .6);font-size:20px; text-align: center; class=text-muted;font-family:'Open Sans', sans-serif; '> <b>PROTECTION OF DATA:-</b><br>
<ul style='font-size:20px;class=text-muted;text-align: justify;'>
  <li>In this master thesis research, we used the Student Response Analysis dataset comprises student replies to explanation and definition questions found in practice activities and exams. 
  The SRA dataset is split into two parts: Beetle and SciEntsBank. 
  Answers to explanation and definition questions are meticulously labelled. The data set includes an question, reference answer, and student response.
  In this thesis, a human annotator classifies each student response as one of five evaluations. 
  We used the SRA dataset to build our dataset. </li> <br>
  <li> The original principle of this thesis is to generate an explanation and get evaluation feedback from the student, which can then classify as either Rating or Student Feedback .
Based on the student answers, generate an explanation of why the student's answer is correct or incorrect. Firstly, it is a model-generated explanation by the model of Natural Language Processing (NLP). Finally, it asks the student to evaluate if the model-generated explanation is viable, asking students to write feedback.</li> <br>
  <li> Whatever data is provided in this survey will be taken into use only for this thesis work. The data will not be 
  shared in any place. This data will remain completely anonymous.
  The feedback form started after a generated explanation. </li>
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
    csv_collection = db.csv_collection_2
    return csv_collection.insert_one(dict_to_save)


def create_dict():
    return {
        'question': data['question'],
        'student_answer': data['student_answer'],
        'accuracy': data['accuracy'],
        'explanation': data['explanation'],
        'What do you think about the generated explanation?':
            st.session_state[STUDENT_EVALUTION_QUESITON1],
        'rating':
            st.session_state[STUDENT_RATING],
        'Does the generated explanation convey meaning of the original text?':
            st.session_state[STUDENT_EVALUTION_QUESITON2],
        'How useful did you find the generated explanation?':
            st.session_state[STUDENT_EVALUTION_QUESITON3],
        'Is there an alternative explanation that solves the same problem?':
            st.session_state[STUDENT_EVALUTION_QUESITON4],
        'Does the generated explanation is readable?':
            st.session_state[STUDENT_EVALUTION_QUESITON5],
        'What is wrong with this generated explanation?':
            st.session_state[STUDENT_EVALUTION_QUESITON6],
        # 'student_explanation': st.session_state[STUDENT_EXPLANATION]
    }


def increment_counter():
    st.session_state.count += 1


def clear_session_state():
    # st.session_state[STUDENT_EXPLANATION] = ''
    st.session_state[STUDENT_RATING] = '1 Star'
    print(st.session_state)


# def get_list_of_file_names():
#     return glob.glob("./tmp/semeval2013-Task7-2and3way/*/2way/*/*.xml") + \
#            glob.glob("./tmp/semeval2013-Task7-2and3way/test/2way/*/*/*.xml")


def create_question_string():
    # st.write("Question :")
    return f"<h3 style='font-family: 'IBM Plex Sans', sans-serif; font-size:22px; class=text-muted;text-align: justify;display: none;'>Question :</h3>" \
           f"<p style='outline-style: solid; margin:auto; padding:15px;outline-color: rgba(170, 50, 220, .6);text-align: justify;font-size:25px; class=text-muted'>" \
           f"{data['question']}</p>"


def create_answer_string():
    return f"<h3 style=' font-family: 'IBM Plex Sans', sans-serif; font-size:22px; class=text-muted;text-align: justify;display: none;'>Student Answer :</h3>" \
           f"<p style='outline-style: solid;padding:10px; outline-color: rgba(170, 50, 220, .6);font-size:25px; class=text-muted;text-align: justify;'>" \
           f" {data['student_answer']}</p>"


def load_student_question_form():

    components.html(question_str, scrolling=True)
    # st.write("Student Answer :")
    components.html(answer_str,scrolling=True)
    # st.text_area("", value=data['student_answer'])
    components.html(
        EXPLANATION_HTML.format(
            answerStatus=data['accuracy'],
            explanation=data['explanation'],
            reference_ans=data['ref_answer']
        ),
        height=600,
        scrolling=True
    )

    st.write(
        '<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    st.write(
        '<style>div.row-widget.stButton > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    radioOptions = ['1 Star', '2 Star', '3 Star', '4 Star', '5 Star']
    radioOptionss = ['Yes', 'No', 'Maybe', 'Can not say']
    st.container()
    with st.form("form1", clear_on_submit=True):
        st.write(
            '<p style="float:center; font-size:20px;text-align: justify; class=text-muted;"><b>For the generated explanation, read the below questions, and you could do the Evaluation based on rating and write your feedback in the section below.</b></p>',
            unsafe_allow_html=True)

        st.write(
            ' <p style="float:center; font-size:20px;text-align: justify; class=text-muted;"> 1) What are your thoughts about the generated explanation?</p>',
            unsafe_allow_html=True)
        st.multiselect('Select one variables that are known :',
                       ['1) Perfectly Understandable ', '2) Partially Understandable', ' 3) Partially Imperfect',
                        '4) Completely Imperfect '], key=STUDENT_EVALUTION_QUESITON1)
        st.write(
            ' <p style="float:center; font-size:20px;text-align: justify; class=text-muted;"> 2) What ratings would you like to give for this generated explanation?</p>',
            unsafe_allow_html=True)
        st.radio("Select Rating :", radioOptions, key=STUDENT_RATING)
        st.write(
            ' <p style="float:center; font-size:20px;text-align: justify; class=text-muted;"> 3) Do you think the generated explanation is fully related to the student answer?</p>',
            unsafe_allow_html=True)

        st.radio('Select One Option :', radioOptionss, key=STUDENT_EVALUTION_QUESITON2)


        st.write(
            ' <p style="float:center; font-size:20px;text-align: justify; class=text-muted;"> 4) How useful did you find the generated explanation?</p>',
            unsafe_allow_html=True)
        st.radio('Select one known variables :',
                          ['Very Good',
                           'Good',
                           'Ok',
                           'Bad'], key=STUDENT_EVALUTION_QUESITON3)
        st.write(
            ' <p style="float:center; font-size:20px;text-align: justify; class=text-muted;"> 5) Is there an alternative explanation that solves the same problem?</p>',
            unsafe_allow_html=True)
        st.write(
            ' <p style="float:center; font-size:18px;text-align: justify; class=text-muted;"> : If  Yes  Write  your  Explanation  here  <b>Or</b>  If  No  go  Further </p>',
            unsafe_allow_html=True)
        st.text_area("Write Your Feedback :",key=STUDENT_EVALUTION_QUESITON4)
        st.write(
            ' <p style="float:center; font-size:20px;text-align: justify; class=text-muted;"> 6) Is the generated explanation is readable?</p>',
            unsafe_allow_html=True)
        st.multiselect('Select three variables that are known :',['1) Easy to read','2) Difficult to read',' 3) Not understandable',
                                                '4)  Bad sentence formation','5) Ambiguous pronoun references', '6) logical fallacies','7) misspellings typographical errors',
                                                                             '8) faulty punctuation'],key=STUDENT_EVALUTION_QUESITON5)

        st.write(
            ' <p style="float:center; font-size:20px;text-align: justify; class=text-muted;"> 7) What wrong do you find  in this generated explanation?</p>',
            unsafe_allow_html=True)
        st.multiselect('Select three variables that are known :',['1) There is a mistake in the grammar', '2) The sentence is not correct', '3) unconventional',
                        '4) an inappropriate verb tense', '5) Vocabulary Errors', '6) Too many prepositional phrases',], key=STUDENT_EVALUTION_QUESITON6)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            pass
        with col2:
            pass
        with col4:
            pass
        with col5:
            pass
        with col3:
            st.form_submit_button("Next Question", on_click=feedback_form_submitted)


    #
    # st.write(
    #     ' <p style="float:center; font-size:20px;text-align: justify; class=text-muted;">6)  What is wrong with this generated explanation?</p>',
    #     unsafe_allow_html=True)




    # st.container()
    # with st.form("form", clear_on_submit=True):
    #     components.html(EVOLUTION_HTML.format(), height=380, scrolling=True)
    #
    #
    #     st.text_area("Student Feedback :", key=STUDENT_EXPLANATION)
    #
    #     st.form_submit_button("Next Question", on_click=feedback_form_submitted)


def initialize_session_state():
    st.session_state[COUNT] = 1
    st.session_state[STUDENT_RATING] = '1 Star'
    # st.session_state[STUDENT_EXPLANATION] = ''
    st.session_state[STUDENT_EVALUTION_QUESITON1] = '1) Perfectly Understandable '
    st.session_state[STUDENT_EVALUTION_QUESITON2] = 'Yes'
    st.session_state[STUDENT_EVALUTION_QUESITON3] = 'Very Good'
    st.session_state[STUDENT_EVALUTION_QUESITON4] = ''
    st.session_state[STUDENT_EVALUTION_QUESITON5] = '1) Easy to read'
    st.session_state[STUDENT_EVALUTION_QUESITON6] = '1) There is a mistake in the grammar'


def initialize_few_session_state():
    st.session_state[STUDENT_RATING] = '1 Star'
    # st.session_state[STUDENT_EXPLANATION] = ''
    st.session_state[STUDENT_EVALUTION_QUESITON1] = '1) Perfectly Understandable '
    st.session_state[STUDENT_EVALUTION_QUESITON2] = 'Yes'
    st.session_state[STUDENT_EVALUTION_QUESITON3] = 'Very Good'
    st.session_state[STUDENT_EVALUTION_QUESITON4] = ''
    st.session_state[STUDENT_EVALUTION_QUESITON5] = '1) Easy to read'
    st.session_state[STUDENT_EVALUTION_QUESITON6] = '1) There is a mistake in the grammar'


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
ran = random.choice(lines)
print('random choice:',ran)
line = lines[st.session_state[COUNT]]

row = ran.split('|')

print('new data:',row)
data = {
    'question': row[0],
    'ref_answer': row[1],
    'student_answer': row[2],
    'accuracy': row[3],
    'explanation': row[4],
}


# csv_reader = csv.reader(data)
# question = list(csv_reader)
# random_data = random.choice(question)
# print(random_data)
# first uni logo with description
if enableLogo:
    st.image(use_column_width=True, image=LOGO_URL)
    components.html(description, height=640, width=800)

st.markdown("___")
question_str = create_question_string()
answer_str = create_answer_string()
load_student_question_form()
