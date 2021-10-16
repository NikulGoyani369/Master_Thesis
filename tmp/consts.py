STUDENT_ANSWER = 'student_answer'
ANSWER_STATE = 'answer_state'
REFERENCE_ANSWER = 'reference_answer'
COUNT = 'count'
OPEN_AI_EXPLANATION = 'explanation'
STUDENT_EXPLANATION = 'student_explanation'
STUDENT_RATING = 'rating'
STUDENT_FORM_SUBMITTED = 'student_form_submitted'
FEEDBACK_FORM_SUBMITTED = 'feedback_form_submitted'
EXPLANATION_HTML = """
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
