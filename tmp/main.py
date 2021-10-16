import openai
import pymongo as mongo
import streamlit as st
import streamlit.components.v1 as components

from forms import *
from openai_functs import *
from xml_functs import *

enableLogo = False

openai.api_key = st.secrets['OPENAI_API_KEY']
client = mongo.MongoClient(**st.secrets["mongo"])

initialize_session_state(st)

data = extract_data(st)

soup = BeautifulSoup(data, "xml")

answers = find_answers(soup)
question = get_question(soup)

if enableLogo:
    st.image(use_column_width=True, image=LOGO_URL)
    components.html(description, height=340, width=700, scrolling=True)

st.markdown("___")
target_answer = find_target_answer(st, answers)
question_str = create_question_string(question)

load_form_submitted = load_student_question_form(st, components, question_str)

if load_form_submitted:
    response = get_openai_response(openai, st, question_str, target_answer)
    open_ai_explanation = get_explanation_from_responce(response)
    save_in_session(st, OPEN_AI_EXPLANATION, open_ai_explanation)
    ref_answer = get_reference_ans(soup)
    save_in_session(st, REFERENCE_ANSWER, ref_answer)
    load_feedback_form(
                        st,
                        components,
                        get_from_session(st, OPEN_AI_EXPLANATION),
                        target_answer,
                        get_from_session(st, REFERENCE_ANSWER)
                    )

if get_from_session(st, FEEDBACK_FORM_SUBMITTED):
    print('yes i am true')

# feedback = get_from_session(st, FEEDBACK_FORM_SUBMITTED)
# print(FEEDBACK_FORM_SUBMITTED)
# print(feedback)
# if feedback:
#     print('test')
#     m_client = MyMongoClient(client)
#     student_feedback = to_sf(st)
#     m_client.write_to_db(student_feedback)
#     increment_counter(st)
#     clear_session_state(st)


def feedback_form_submitted():
    print("feedback form submitted")
