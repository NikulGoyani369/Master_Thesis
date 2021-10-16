def create_dict(sf):
    return {
        'question': sf.question,
        'student_answer': sf.answer,
        'correct_incorrect': sf.answer_stat,
        'explanation': sf.ai_explanation,
        'rating': sf.rating,
        'student_explanation': sf.student_explanation
    }


class MyMongoClient:
    def __init__(
            self,
            client):
        self.client = client

    def write_to_db(self, student_feedback):
        db = self.client.nlp_db
        csv_collection = db.csv_collection
        return csv_collection.insert_one(create_dict(student_feedback))
