from bs4 import BeautifulSoup

from consts import *
from file_functs import *


def find_answers(soup):
    tags = []
    for tag in soup.find_all('studentAnswer', accuracy="correct"):
        tags.append(tag.string)
    return tags


def get_question(soup):
    return soup.find('questionText').string


def find_target_answer(st, answers):
    return "correct" if st.session_state[STUDENT_ANSWER] in answers else "incorrect"


def create_question_string(question):
    return f"<p style='outline-style: solid;padding:10px;outline-color: green;'> {question}</p>"


def get_reference_ans(soup):
    return soup.find('referenceAnswer', category="BEST").string
