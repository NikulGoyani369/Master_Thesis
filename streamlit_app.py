import streamlit as st
import streamlit.components.v1 as components

LOGO_URL = "https://www.ltl.uni-due.de/assets/images/logo3.png"
description = """
<p style='outline-style: solid;padding:10px;outline-color: green;'> <b>PROTECTION OF DATA</b>
The owners of this website take the security of your personal information very seriously. We handle your personal data with confidentiality and in compliance with the applicable data protection laws and this data protection statement.

Various personal data are gathered when you use this website. Personal data are pieces of information that may be used to identify you personally. This data protection statement outlines what information we gather and how we utilize it. It also discusses why and how this is accomplished.

We'd like to emphasize that data transfer via the Internet (for example, while interacting through e-mail) may have security flaws. It is not feasible to completely secure data from unauthorized access.</p>
"""

resultAndExplanationHTML = """
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>


<div class="card mb-12 shadow-sm"   >
      <div class="card-body"  style='outline-style: solid;padding:10px;outline-color: blue;'>
        <h2 class="card-title">Result:</h2>
        Your answer is {answerStatus}.
    </div>
</div>
<br>
<div class="card mb-12 shadow-sm" >
      <div class="card-body" style='outline-style: solid;padding:10px;outline-color: green;'>
        <h2 class="card-title">Explanation:</h2>
        {explanation}
    </div>
</div>
<br>
<div class="card mb-12 shadow-sm">
    <div class="card-header">
        <small style="float:center; font-size:20px; "  class="text-muted">What do you think this explanation is good. Why not?<br>Below write your explanation.</small>
    </div>
</div>
"""

st.image(use_column_width=True, image=LOGO_URL)
st.image(use_column_width=True)

components.html(description, width=700, scrolling=True)

st.markdown("___")
with st.form("my_form"):
    st.write("Question")
    question = "<p style='outline-style: solid;padding:10px;outline-color: green;'>Explain why circuit 2 is not a short circuit.</p>"
    components.html(question)
    answer = st.text_input("Answer")
    isSubmitted = st.form_submit_button("Submit")

    # Every form must have a submit button.


def load_feedback_form():
    with st.container():
        explanation = " Random Explanaton to be generated by the system as a response to the specific question. Random Explanaton to be generated by the system as a response to the specific question. Random Explanaton to be generated by the system as a response to the specific question. Random Explanaton to be generated by the system as a response to the specific question"
        components.html(resultAndExplanationHTML.format(answerStatus="Correct", explanation=explanation), height=500,
                        scrolling=True)
        st.write(
            '<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        st.write(
            '<style>div.row-widget.stButton > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        with st.form("feedbackform"):
            radioOptions = ['1 Star', '2 Star', '3 Star', '4 Star', '5 Star']
            # radioOptions = ['10 Star', '9 Star', '8 Star', '7 Star', '6 Star', '5 Star', '4 Star', '3 Star', '2 Star',
            #                 '1 Star']
            star = st.radio("Select Rating", radioOptions)

            student_explanation = st.text_area("Student Explanation")

            feedbackFormSubmission = st.form_submit_button("Next Question")

    if feedbackFormSubmission:
        st.success(star)
        st.success(student_explanation)
    st.button("Submit")


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
