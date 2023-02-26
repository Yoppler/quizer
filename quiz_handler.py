from copy import deepcopy
from dataclasses import dataclass, field


class QuizHandler:
    def __init__(self, quiz):
        self.quiz = quiz
        self.total_questions = len(self.quiz.questions)
        self.cur_question = 0
        self.handler_questions = self.create_handler_questions()
        self.incorrect = []

    def create_handler_questions(self):
        """Enables QuestionHistory for back/forward navigation"""
        q_history = []
        for question in self.quiz.questions:
            q = QuestionHistory()
            q.text = question.text
            q.answers = deepcopy(question.answers)
            q_history.append(q)
        return q_history

    def get_question(self):
        """Returns the current question"""
        index = self.cur_question
        if self.cur_question > self.total_questions - 1:
            raise NoMoreQuestions
        return self.handler_questions[index]

    def submit_answer(self, question):
        '''takes QuestionHistory object, moves to next question'''
        self.handler_questions[self.cur_question] = question
        self.cur_question += 1

    def previous_question(self):
        index = self.cur_question - 1
        if index < 0:
            raise NoMoreQuestions

        question = self.handler_questions[index]
        self.cur_question -= 1
        return question

    def calculate_score(self):
        quiz_len = self.total_questions
        questions_submitted = self.handler_questions
        score = 0

        for question in questions_submitted:
            for c_answer, s_answer in zip(question.answers, question.submitted_answers):
                if c_answer != s_answer:
                    self.incorrect.append(question)
                    break
            else:
                score += 1

        s = Score()
        s.numerator = score
        s.denominator = quiz_len
        s.percent = int(s.numerator / s.denominator * 100)

        return s

    def get_title(self):
        return self.quiz.name

    def restart(self):
        self.cur_question = 0
        self.clear_answers()
        self.incorrect.clear()

    def clear_answers(self):
        """Clear submitted answers so user has a fresh quiz"""
        for q in self.handler_questions:
            for answer in q.submitted_answers:
                if answer.correct:
                    answer.correct = False

    def restart_wrong_only(self):
        self.cur_question = 0
        self.clear_answers()
        self.handler_questions = deepcopy(self.incorrect)
        self.total_questions = len(self.handler_questions)
        self.incorrect.clear()


@dataclass
class QuestionHistory:
    text: str = ""
    answers: list = field(default_factory=list)
    submitted_answers: list = field(default_factory=list)


@dataclass
class Score:
    numerator: int = 0
    denominator: int = 0
    percent: int = 0


class NoMoreQuestions(Exception):
    pass
