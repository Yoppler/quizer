import json

from quiz import Quiz
from view import View


class QuizEditor:
    def __init__(self, quiz_name):
        self.name = quiz_name
        self.quiz = Quiz(self.name)
        self.path = self.quiz.path
        self.edited = False

    def get_question(self, index):
        return self.quiz.questions[index]

    def get_question_index_by_text(self, text):
        for i, q in enumerate(self.quiz.questions):
            if text == q.text:
                return i

    def get_question_by_text(self, text):
        for q in self.quiz.questions:
            if text == q.text:
                return q

    def replace_question(self, old, new):
        index = self.get_question_index_by_text(old.text)
        if index is not None:
            self.quiz.questions[index] = new
        self.edited = True

    def edit_question(self, index, question):
        self.quiz.questions[index] = question
        self.edited = True

    def save_changes(self):
        view = View()
        view.quiz_name = self.name
        content = json.dumps(self.quiz.questions, default=vars)
        view.delete_quiz()
        view.create_quiz(content)
