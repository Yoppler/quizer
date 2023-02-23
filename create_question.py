from collections import namedtuple
import json


from PyQt6.QtWidgets import (
        QGridLayout,
        QPlainTextEdit,
        QLabel,
        QLineEdit,
        QCheckBox,
        QPushButton,
)

from PyQt6.QtCore import Qt

from gui_constants import pages
from gui_page import GuiPage
from quiz import Question, Answer


answer_gui = namedtuple("answer_gui", ["text", "correct"])


class CreateQuestion(GuiPage):
    @GuiPage.update_after
    def __init__(self, primary):
        super().__init__()
        self.primary = primary
        self.view = primary.view
        self.quiz = []
        self.answers = []
        self.cur_question = 1

        self.page_layout = QGridLayout()

        self.question = QPlainTextEdit()
        self.question.setStyleSheet(self.primary.ss)
        correct_lbl = QLabel("Correct?")
        correct_lbl.setStyleSheet(self.primary.ss)
        self.configure_answers(count=4, start_row=2)
        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet(self.primary.ss)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(self.primary.ss)
        self.finish_btn = QPushButton("Finish")
        self.finish_btn.setStyleSheet(self.primary.ss)
        self.question_num = QLabel("Question #")
        self.question_num.setStyleSheet(self.primary.ss)

        self.question.setPlaceholderText("QUESTION TEXT")
        correct_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_pressed)

        self.finish_btn.setEnabled(False)
        self.finish_btn.clicked.connect(self.finish_pressed)

        self.cancel_btn.clicked.connect(self.cancel_pressed)

        self.question_num.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.page_layout.addWidget(self.question, 0, 0, 1, 9)
        self.page_layout.addWidget(correct_lbl, 1, 7)
        self.page_layout.addWidget(self.cancel_btn, 6, 0, 1, 3)
        self.page_layout.addWidget(self.finish_btn, 6, 3, 1, 3)
        self.page_layout.addWidget(self.save_btn, 6, 6, 1, 3)
        self.page_layout.addWidget(self.question_num, 7, 0, 1, 9)

        self.setLayout(self.page_layout)
        self.show()

    def configure_answers(self, count, start_row):
        for i in range(count):
            answer_line = QLineEdit()
            answer_line.setPlaceholderText("ANSWER TEXT")
            answer_line.textChanged.connect(self.refresh)
            answer_line.setStyleSheet(self.primary.ss)

            answer_cb = QCheckBox()
            answer_cb.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            answer_cb.stateChanged.connect(self.refresh)
            answer_cb.setEnabled(False)

            gui = answer_gui(answer_line, answer_cb)
            self.answers.append(gui)
            self.page_layout.addWidget(answer_line, start_row+i, 0, 1, 7)
            self.page_layout.addWidget(answer_cb, start_row+i, 7)

    def refresh(self):
        if self.is_savable():
            self.finish_btn.setEnabled(True)
            self.save_btn.setEnabled(True)
        else:
            self.finish_btn.setEnabled(False)
            self.save_btn.setEnabled(False)

        question_num_text = f"Question {self.cur_question}"
        self.question_num.setText(question_num_text)

        for answer in self.answers:
            if len(answer.text.text()) > 0:
                answer.correct.setEnabled(True)
            else:
                answer.text.clear()
                answer.correct.setCheckState(Qt.CheckState.Unchecked)
                answer.correct.setEnabled(False)

    def is_savable(self):
        """Is there question text, and a correct answer"""
        if not len(self.question.toPlainText()) > 0:
            return False

        for answer in self.answers:
            if len(answer.text.text()) > 0 and \
               answer.correct.checkState() == Qt.CheckState.Checked:
                return True
        return False

    def save_pressed(self):
        if not self.is_savable():
            return

        q = Question()
        q.text = self.question.toPlainText()
        for answer in self.answers:
            if answer.text.text():
                a = Answer()
                a.text = answer.text.text()
                if answer.correct.checkState() == Qt.CheckState.Unchecked:
                    a.correct = False
                else:
                    a.correct = True
                q.answers.append(a)
        self.quiz.append(q)
        self.cur_question += 1
        self.clear_page()

    def finish_pressed(self):
        self.save_pressed()
        self.view.create_quiz(json.dumps(self.quiz, default=vars))
        self.primary.change_page(pages.START)

    def cancel_pressed(self):
        self.clear_page()
        self.primary.change_page(pages.START)

    @GuiPage.update_after
    def clear_page(self):
        self.question.clear()
        for answer in self.answers:
            answer.text.clear()

    def focus(self):
        self.clear_page()
