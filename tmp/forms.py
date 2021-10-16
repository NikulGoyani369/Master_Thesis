from sessions import *


def load_student_question_form(st, components, question_str):
    with st.container():
        save_in_session(st, STUDENT_ANSWER, '')
        with st.form("my_form"):
            components.html(question_str)
            st.text_area("Answer", key=STUDENT_ANSWER)
            return st.form_submit_button("Submit")


def load_feedback_form(st, components, explanation, answer_stat, reference_ans):
    with st.container():
        components.html(
            EXPLANATION_HTML.format(
                answerStatus=answer_stat,
                explanation=explanation,
                reference_ans=reference_ans
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

            session_state = st.session_state

            st.form_submit_button("Next Question", on_click=feedback_form_submitted, kwargs=session_state)


def feedback_form_submitted(st):
    print(st)

