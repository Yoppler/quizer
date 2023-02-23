from collections import namedtuple

from PyQt6.QtWidgets import (
        QGridLayout,
        QLabel,
        QCheckBox,
        QPushButton,
        QProgressBar,
        QFrame,
)

from PyQt6.QtCore import Qt

from gui_page import GuiPage
from quiz import Answer
from quiz_handler import NoMoreQuestions

answer_gui = namedtuple("answer_gui", ["line", "cb"])


class QuizQuestion(GuiPage):
    def __init__(self, primary):
        super().__init__()
        self.primary = primary
        self.view = primary.view
        self.quiz = None
        self.answers = []
        self.setup()

    def clear(self):
        self.quiz = None

    def setup(self):
        layout = QGridLayout()
        self.cur_question = None
        self.question = QLabel("Default Question Text")
        self.question.setWordWrap(True)
        self.question.setStyleSheet(self.primary.ss)
        answerA = QLabel("Answer A Text")
        answerA.setStyleSheet(self.primary.ss)
        answerA.setWordWrap(True)
        answerB = QLabel("Answer B Text")
        answerB.setStyleSheet(self.primary.ss)
        answerB.setWordWrap(True)
        answerC = QLabel("Answer C Text")
        answerC.setStyleSheet(self.primary.ss)
        answerC.setWordWrap(True)
        answerD = QLabel("Answer D Text")
        answerD.setStyleSheet(self.primary.ss)
        answerD.setWordWrap(True)
        answerA_cb = QCheckBox()
        answerB_cb = QCheckBox()
        answerC_cb = QCheckBox()
        answerD_cb = QCheckBox()
        self.answers.append(answer_gui(answerA, answerA_cb))
        self.answers.append(answer_gui(answerB, answerB_cb))
        self.answers.append(answer_gui(answerC, answerC_cb))
        self.answers.append(answer_gui(answerD, answerD_cb))
        back_btn = QPushButton("←")
        back_btn.setStyleSheet(self.primary.ss)
        forward_btn = QPushButton("→")
        forward_btn.setStyleSheet(self.primary.ss)
        self.progress = QProgressBar()
        self.progress.setStyleSheet(self.primary.ss)

        self.question.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question.setFrameStyle(QFrame.Shape.Panel)

        back_btn.clicked.connect(self.back_clicked)
        forward_btn.clicked.connect(self.forward_clicked)

        layout.addWidget(self.question,0,0,5,6)
        layout.addWidget(answerA,7,0,1,5)
        layout.addWidget(answerA_cb,7,5,1,1)
        layout.addWidget(answerB,8,0,1,5)
        layout.addWidget(answerB_cb,8,5,1,1)
        layout.addWidget(answerC,9,0,1,5)
        layout.addWidget(answerC_cb,9,5,1,1)
        layout.addWidget(answerD,10,0,1,5)
        layout.addWidget(answerD_cb,10,5,1,1)
        layout.addWidget(back_btn,11,0,1,2)
        layout.addWidget(self.progress,11,2,1,2)
        layout.addWidget(forward_btn,11,4,1,2)

        self.setLayout(layout)
        self.show()

    def refresh(self):
        if self.cur_question is None:
            return
        self.refresh_question()
        self.refresh_cbs()


    def start_quiz(self, quiz_handler):
        self.quiz = quiz_handler
        self.cur_question = self.quiz.get_question()
        self.cur_question_num = 0
        self.progress.setMaximum(self.quiz.total_questions)
        self.progress.setValue(self.cur_question_num)

    @GuiPage.update_after
    def forward_clicked(self, _):
        answers_to_submit = self.create_submitted_answers()
        self.cur_question.submitted_answers = answers_to_submit
        self.quiz.submit_answer(self.cur_question)
        try:
            self.cur_question = self.quiz.get_question()
            self.cur_question_num += 1
            self.progress.setValue(self.cur_question_num)
        except NoMoreQuestions:
            self.primary.quiz_results(self.quiz)

    def create_submitted_answers(self):
        answers = []
        for answer_gui in self.answers:
            a = Answer()
            a.text = answer_gui.line.text()
            a.correct = answer_gui.cb.isChecked()
            answers.append(a)
        return answers

    @GuiPage.update_after
    def back_clicked(self, _):
        try:
            self.cur_question = self.quiz.previous_question()
        except NoMoreQuestions:
            return
        self.cur_question_num -= 1
        self.progress.setValue(self.cur_question_num)

    def refresh_question(self):
        self.question.setText(self.cur_question.text)
        for answers, gui in zip(self.cur_question.answers, self.answers):
            gui.line.setText(answers.text)

    def refresh_cbs(self):
        if len(self.cur_question.submitted_answers) == 0:
            self.reset_cbs()
        else:
            for answer, gui in zip(self.cur_question.submitted_answers, self.answers):
                gui.cb.setChecked(answer.correct)

    def reset_cbs(self):
        for gui in self.answers:
            gui.cb.setChecked(False)
