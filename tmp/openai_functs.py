from consts import *


def get_openai_response(openai, st, question_str, target_answer):
    return openai.Completion.create(
        engine="davinci",
        prompt=f"Question: {question_str}\nStudentAnswer: {st.session_state[STUDENT_ANSWER]}\nTargetAnswer: "
               f"{target_answer}\nExplanation",
        temperature=1,
        max_tokens=64,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=2,
        stop=["\n"]
    )


def get_explanation_from_responce(response):
    return response['choices'][0]['text']
