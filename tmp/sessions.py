from consts import *


def initialize_session_state(st):
    if 'count' not in st.session_state:
        save_in_session(st, COUNT, 0)
        save_in_session(st, ANSWER_STATE, '')
        save_in_session(st, OPEN_AI_EXPLANATION, '')
        save_in_session(st, STUDENT_RATING, '')
        save_in_session(st, STUDENT_EXPLANATION, '')
        save_in_session(st, STUDENT_ANSWER, '')
        save_in_session(st, STUDENT_FORM_SUBMITTED, False)
        save_in_session(st, FEEDBACK_FORM_SUBMITTED, False)
        save_in_session(st, REFERENCE_ANSWER, '')


def save_in_session(st, key, value):
    st.session_state[key] = value


def get_from_session(st, key):
    return st.session_state[key]


def increment_counter(st):
    st.session_state.count += 1


def clear_session_state(st):
    st.session_state.answer = ''
    st.session_state[ANSWER_STATE] = ''
    st.session_state[STUDENT_EXPLANATION] = ''
    st.session_state[STUDENT_RATING] = '1 Star'
    st.session_state[STUDENT_FORM_SUBMITTED] = False
