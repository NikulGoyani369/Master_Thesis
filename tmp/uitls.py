from student_feedback import student_feedback


def to_sf(st):
    return student_feedback(
        st.session_state.question,
        st.session_state.answer,
        st.session_state.answer_stat,
        st.session_state.ai_explanation,
        st.session_state.rating,
        st.session_state.student_explanation
    )