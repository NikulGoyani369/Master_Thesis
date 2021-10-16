class student_feedback:
    question = ''
    answer = ''
    answer_stat = ''
    ai_explanation = ''
    rating = ''
    student_explanation = ''

    def __init__(
            self,
            question,
            answer,
            answer_stat,
            ai_explanation,
            rating,
            student_explanation
    ):
        self.question = question
        self.answer = answer
        self.answer_stat = answer_stat
        self.ai_explanation = ai_explanation
        self.rating = rating
        self.student_explanation = student_explanation

