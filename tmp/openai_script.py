import glob
from bs4 import BeautifulSoup
import os
import openai

openai.api_key = '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'

file_name_to_write = 'open_ai_questions.csv'

if os.path.exists(file_name_to_write):
    os.remove(file_name_to_write)

files = glob.glob("./semeval2013-Task7-2and3way/training/2way/*/*.xml")
file_to_write = open(file_name_to_write,'a')

file_to_write.write('question|ref_ans|student_ans|accuracy|explaination')

for file in files:
    data = open(file).read()
    soup = BeautifulSoup(data, "xml")
    question = soup.find('questionText').string
    ref_ans = soup.find('referenceAnswer').string
    student_answer = soup.find('studentAnswer')
    student_answer_str = student_answer.string
    student_answer_accuracy = student_answer['accuracy']
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Question: {question}\nStudentAnswer: {student_answer_str}\nTargetAnswer: {ref_ans}\nExplanation",
        temperature=1,
        max_tokens=64,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=2,
        stop=["\n"]
    )

    explanation = response['choices'][0]['text']

    print(explanation)
    file_to_write.write(f"{question}|{ref_ans}|{student_answer_str}|{student_answer_accuracy}|{explanation}\n")


file_to_write.close()

file_to_read = open(file_name_to_write, 'r')








