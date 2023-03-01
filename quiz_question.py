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
        self.last_answer_row = 0
        self.setup()

    def clear(self):
        self.quiz = None

    def setup(self):
        self.cur_question = None

        self.page_layout = QGridLayout()
        self.question = QLabel("Default Question Text")
        self.back_btn = QPushButton("←")
        self.forward_btn = QPushButton("→")
        self.progress = QProgressBar()

        self.question.setStyleSheet(self.primary.ss)
        self.back_btn.setStyleSheet(self.primary.ss)
        self.forward_btn.setStyleSheet(self.primary.ss)
        self.progress.setStyleSheet(self.primary.ss)

        self.back_btn.clicked.connect(self.back_clicked)
        self.forward_btn.clicked.connect(self.forward_clicked)

        self.question.setWordWrap(True)
        self.question.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question.setFrameStyle(QFrame.Shape.Panel)

        self.page_layout.addWidget(self.question, 0, 0, 1, 6)
        self.setLayout(self.page_layout)
        self.show()

    def init_answers(self, count, start_row):
        for i in range(count):
            answer_line = QLabel()
            answer_line.setStyleSheet(self.primary.ss)
            answer_line.setWordWrap(True)

            answer_cb = QCheckBox()
            self.answers.append(answer_gui(answer_line, answer_cb))

            row = start_row + i
            self.page_layout.addWidget(answer_line, row, 0, 1, 5)
            self.page_layout.addWidget(answer_cb, row, 5, 1, 1)
        self.last_answer_row = count + start_row
        self.shift_btns()

    def shift_btns(self):
        row = self.last_answer_row + 1
        self.page_layout.addWidget(self.back_btn, row, 0, 1, 2)
        self.page_layout.addWidget(self.progress, row, 2, 1, 2)
        self.page_layout.addWidget(self.forward_btn, row, 4, 1, 2)

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
        self.clear_answers()
        self.question.setText(self.cur_question.text)
        self.init_answers(len(self.cur_question.answers), 2)
        for answers, gui in zip(self.cur_question.answers, self.answers):
            gui.line.setText(answers.text)

    def clear_answers(self):
        for gui in self.answers:
            self.page_layout.removeWidget(gui.line)
            self.page_layout.removeWidget(gui.cb)
            gui.line.deleteLater()
            gui.cb.deleteLater()
        self.answers.clear()

    def refresh_cbs(self):
        if len(self.cur_question.submitted_answers) == 0:
            self.reset_cbs()
        else:
            for answer, gui in zip(
                    self.cur_question.submitted_answers, self.answers):
                gui.cb.setChecked(answer.correct)

    def reset_cbs(self):
        for gui in self.answers:
            gui.cb.setChecked(False)
