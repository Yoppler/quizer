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
        layout = QGridLayout()
        self.question = QPlainTextEdit()
        self.question.setStyleSheet(self.primary.ss)
        correct_lbl = QLabel("Correct?")
        correct_lbl.setStyleSheet(self.primary.ss)
        answerA = QLineEdit()
        answerA.setStyleSheet(self.primary.ss)
        answerB = QLineEdit()
        answerB.setStyleSheet(self.primary.ss)
        answerC = QLineEdit()
        answerC.setStyleSheet(self.primary.ss)
        answerD = QLineEdit()
        answerD.setStyleSheet(self.primary.ss)
        answerA_cb = QCheckBox()
        answerB_cb = QCheckBox()
        answerC_cb = QCheckBox()
        answerD_cb = QCheckBox()

        self.answers.append(answer_gui(answerA, answerA_cb))
        self.answers.append(answer_gui(answerB, answerB_cb))
        self.answers.append(answer_gui(answerC, answerC_cb))
        self.answers.append(answer_gui(answerD, answerD_cb))

        self.question.setPlaceholderText("QUESTION TEXT")
        correct_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet(self.primary.ss)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(self.primary.ss)
        self.save_btn.clicked.connect(self.save_pressed)
        self.cancel_btn.clicked.connect(self.cancel_pressed)

        layout.addWidget(self.question, 0, 0, 1, 9)
        layout.addWidget(correct_lbl, 1, 7)
        layout.addWidget(answerA, 2, 0, 1, 7)
        layout.addWidget(answerA_cb, 2, 7)
        layout.addWidget(answerB, 3, 0, 1, 7)
        layout.addWidget(answerB_cb, 3, 7)
        layout.addWidget(answerC, 4, 0, 1, 7)
        layout.addWidget(answerC_cb, 4, 7)
        layout.addWidget(answerD, 5, 0, 1, 7)
        layout.addWidget(answerD_cb, 5, 7)
        layout.addWidget(self.cancel_btn, 6, 0, 1, 3)
        layout.addWidget(self.save_btn, 6, 6, 1, 3)
        self.setLayout(layout)
        self.show()

    def refresh(self):
        if not self.question:
            return

        self.question.setPlainText(self.question_obj.text)
        for answer, answer_gui in zip(self.question_obj.answers, self.answers):
            answer_gui.text.setText(answer.text)
            answer_gui.correct.setChecked(answer.correct)

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
        self.primary.go_back()

    def clear(self):
        self.question.setPlainText("")
        for a in self.answers:
            a.text.setText("")
            a.correct.setChecked(False)
