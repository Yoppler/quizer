
from PyQt6.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QSizePolicy
)

from PyQt6.QtCore import Qt

from gui_page import GuiPage
from gui_constants import pages


class ResultsDetails(GuiPage):
    def __init__(self, primary):
        super().__init__()
        self.primary = primary
        self.handler = None
        self.setup()

    def clear(self):
        self.handler = None

    def setup(self):
        self.widget_layout = QGridLayout()
        back_btn = QPushButton("Back")
        finish_btn = QPushButton("Finish")

        back_btn.clicked.connect(self.back_pressed)
        finish_btn.clicked.connect(self.finish_pressed)

        self.widget_layout.addWidget(back_btn,3,0,1,1)
        self.widget_layout.addWidget(finish_btn,3,2,1,1)

        self.setLayout(self.widget_layout)
        self.show()

    def refresh(self):
        if self.handler is None:
            return
        
        scroll = QScrollArea()
        questions_widget = QWidget()
        layout = QVBoxLayout()

        for question in self.handler.handler_questions:
            question_container = self.create_question_container(question)
            question_container.setContentsMargins(0,5,0,5)
            question_container.setStyleSheet("QWidget {border:1px solid rgb(0,0,0);}")
            layout.addWidget(question_container)

        questions_widget.setLayout(layout)


        scroll.setWidget(questions_widget)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.widget_layout.addWidget(scroll,0,0,3,3)

    def create_question_container(self, question):
        correct_ss = "QLabel { background-color: green; border:0px; font-size:18pt}"
        incorrect_ss = "QLabel { background-color: red; border:0px; font-size:18pt}"

        question_container = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(0)
        
        question_lbl = QLabel(question.text)
        question_lbl.setStyleSheet("QLabel {border:0px; font-size:18pt}")
        question_lbl.setWordWrap(True)
        question_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        both_correct_submitted = []
        correct_not_submitted = []
        submitted_not_correct = []
        for correct, submitted in zip(question.answers, question.submitted_answers):
            if correct.correct and submitted.correct:
                both_correct_submitted.append(correct.text)
            elif correct.correct:
                correct_not_submitted.append(correct.text)
            elif submitted.correct:
                submitted_not_correct.append(submitted.text)

        lbls = []
        for answer in both_correct_submitted:
            lbl = QLabel(f"Your answer: {answer}")
            lbl.setContentsMargins(0,0,0,0)
            lbl.setStyleSheet(correct_ss)
            lbl.setIndent(10)
            lbls.append(lbl)
        for answer in correct_not_submitted:
            lbl = QLabel(f"Correct answer: {answer}")
            lbl.setContentsMargins(0,0,0,0)
            lbl.setStyleSheet(correct_ss)
            lbl.setIndent(10)
            lbls.append(lbl)
        for answer in submitted_not_correct:
            lbl = QLabel(f"Your answer: {answer}")
            lbl.setContentsMargins(0,0,0,0)
            lbl.setStyleSheet(incorrect_ss)
            lbl.setIndent(10)
            lbls.append(lbl)

        layout.addWidget(question_lbl)
        for lbl in lbls:
            layout.addWidget(lbl)

        question_container.setLayout(layout)
        return question_container

    def back_pressed(self):
        self.primary.change_page(pages.RESULTS_OVERVIEW)

    def finish_pressed(self):
        self.primary.return_to_home()
