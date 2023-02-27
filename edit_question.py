from collections import namedtuple
from PyQt6.QtWidgets import (
    QGridLayout,
    QPlainTextEdit,
    QLabel,
    QLineEdit,
    QCheckBox,
    QPushButton,
)
from PyQt6.QtCore import Qt
from gui_page import GuiPage
from gui_constants import pages
from quiz import Question, Answer

answer_gui = namedtuple("answer_gui", ["text", "correct"])


class EditQuestion(GuiPage):
    def __init__(self, primary):
        super().__init__()
        self.primary = primary
        self.question_obj = None
        self.answers = []
        self.setup()

    def setup(self):
        self.page_layout = QGridLayout()
        self.question = QPlainTextEdit()
        self.question.setStyleSheet(self.primary.ss)
        correct_lbl = QLabel("Correct?")
        correct_lbl.setStyleSheet(self.primary.ss)

        self.question.setPlaceholderText("QUESTION TEXT")
        correct_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet(self.primary.ss)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(self.primary.ss)
        self.save_btn.clicked.connect(self.save_pressed)
        self.cancel_btn.clicked.connect(self.cancel_pressed)

        self.page_layout.addWidget(self.question, 0, 0, 1, 9)
        self.page_layout.addWidget(correct_lbl, 1, 7)
        self.page_layout.addWidget(self.cancel_btn, 6, 0, 1, 3)
        self.page_layout.addWidget(self.save_btn, 6, 6, 1, 3)
        self.setLayout(self.page_layout)
        self.show()

    def configure_answers(self, count, start_row):
        for i in range(count):
            row = start_row + i
            answer_line = QLineEdit()
            answer_cb = QCheckBox()

            answer_line.setStyleSheet(self.primary.ss)
            self.answers.append(answer_gui(answer_line, answer_cb))
            self.page_layout.addWidget(answer_line, row, 0, 1, 7)
            self.page_layout.addWidget(answer_cb, row, 7)

    def refresh(self):
        if not self.question_obj:
            return

        self.question.setPlainText(self.question_obj.text)
        self.configure_answers(
                count=len(self.question_obj.answers),
                start_row=2)

        for answer, answer_gui in zip(self.question_obj.answers, self.answers):
            answer_gui.text.setText(answer.text)
            answer_gui.correct.setChecked(answer.correct)
        
        row = len(self.question_obj.answers) + 2
        self.page_layout.addWidget(self.cancel_btn, row, 0, 1, 3)
        self.page_layout.addWidget(self.save_btn, row, 6, 1, 3)

    def save_pressed(self):
        q = Question(self.question.toPlainText())
        answers = []
        for gui in self.answers:
            correct = gui.correct.isChecked()
            a = Answer(gui.text.text(), correct)
            answers.append(a)
        q.answers = answers

        self.clear()
        self.primary.question_edited(q)

    def cancel_pressed(self):
        self.clear()
        self.primary.change_page(pages.EDIT_OVERVIEW)

    def clear(self):
        self.question.setPlainText("")
        for a in self.answers:
            a.text.deleteLater()
            a.correct.deleteLater()
            self.page_layout.removeWidget(a.text)
            self.page_layout.removeWidget(a.correct)
        self.answers.clear()
