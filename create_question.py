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

# Create new question page
# contains textbox for question, and answers
# and the control buttons
class CreateQuestion(GuiPage):
    @GuiPage.update_after
    def __init__(self, primary):
        # TODO: Does a class get a default init() that is just a call to its parent's __init__()?
        super().__init__()
        # TODO: Primary what?
        self.primary = primary
        self.view = primary.view
        self.quiz = []
        self.cur_question = 1

        self.page_layout = QGridLayout()
        self.fresh_page()

        self.setLayout(self.page_layout)
        self.show()

    def fresh_page(self):
        # Possibly move to __init__()
        self.answers = []
        self.question = QPlainTextEdit(self)
        correct_lbl = QLabel("Correct?", self)
        self.cancel_btn = QPushButton("Cancel", self)
        self.save_btn = QPushButton("Save", self)
        self.finish_btn = QPushButton("Finish", self)
        self.add_answer_btn = QPushButton("+", self)
        self.question_num = QLabel("Question #", self)

        self.question.setTabChangesFocus(True)

        
        # TODO: Can we possibly move to init()?
        self.last_answer_row = 1

        # TODO: Theoretically we can set configurable default
        self.configure_answers(count=2, start_row=2)

        # Initialize tabflow
        self.setTabOrder(self.add_answer_btn, self.save_btn)
        self.setTabOrder(self.save_btn, self.finish_btn)
        self.setTabOrder(self.finish_btn, self.cancel_btn)


        self.cancel_btn.clicked.connect(self.cancel_pressed)
        self.save_btn.clicked.connect(self.save_pressed)
        self.finish_btn.clicked.connect(self.finish_pressed)
        self.add_answer_btn.clicked.connect(self.add_answer_pressed)
        self.question.textChanged.connect(self.refresh)
        
        # TODO: Why this? Do I need a custom button class that auto set's the stylesheet?
        self.cancel_btn.setStyleSheet(self.primary.ss)
        self.save_btn.setStyleSheet(self.primary.ss)
        self.finish_btn.setStyleSheet(self.primary.ss)
        self.add_answer_btn.setStyleSheet(self.primary.ss)
        correct_lbl.setStyleSheet(self.primary.ss)
        self.question_num.setStyleSheet(self.primary.ss)
        self.question.setStyleSheet(self.primary.ss)

        # Don't want to save or finish on fresh page
        # TODO: Consider allowing finish if > 1 question in quiz
        self.save_btn.setEnabled(False)
        self.finish_btn.setEnabled(False)

        self.question_num.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        correct_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.question.setPlaceholderText("QUESTION TEXT")

        self.page_layout.addWidget(self.question, 0, 0, 1, 9)
        self.page_layout.addWidget(correct_lbl, 1, 7)
        self.page_layout.addWidget(self.add_answer_btn, 4, 6, 1, 3)
        self.page_layout.addWidget(self.cancel_btn, 5, 0, 1, 3)
        self.page_layout.addWidget(self.finish_btn, 5, 3, 1, 3)
        self.page_layout.addWidget(self.save_btn, 5, 6, 1, 3)
        self.page_layout.addWidget(self.question_num, 6, 0, 1, 9)

    # Create count amount of answer rows, consisting of question text & correct checkbox
    def configure_answers(self, count, start_row):
        for i in range(count):
            answer_line = QLineEdit(self)
            answer_line.setPlaceholderText("ANSWER TEXT")
            answer_line.textChanged.connect(self.refresh)
            answer_line.setStyleSheet(self.primary.ss)

            answer_cb = QCheckBox(self)
            answer_cb.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            answer_cb.stateChanged.connect(self.refresh)
            answer_cb.setEnabled(False)


            gui = answer_gui(answer_line, answer_cb)
            self.answers.append(gui)
            self.page_layout.addWidget(answer_line, start_row+i, 0, 1, 7)
            self.page_layout.addWidget(answer_cb, start_row+i, 7)
            self.last_answer_row += 1

            # TODO: Fix tab flow problem 
            self.setTabOrder(self.answers[-1].text, self.answers[-1].correct)
            self.setTabOrder(self.answers[-1].correct, self.add_answer_btn) 
            if len(self.answers) >= 2:
                self.setTabOrder(self.answers[-2].correct, self.answers[-1].text)
                self.answers[-1].text.setFocus()

    # Possibly call it "control buttons"
    def shift_btns(self):
        """Move all buttons down 1 row"""
        row = self.last_answer_row + 1
        self.page_layout.addWidget(self.add_answer_btn, row, 6, 1, 3)
        self.page_layout.addWidget(self.cancel_btn, row + 1, 0, 1, 3)
        self.page_layout.addWidget(self.finish_btn, row + 1, 3, 1, 3)
        self.page_layout.addWidget(self.save_btn, row + 1, 6, 1, 3)
        self.page_layout.addWidget(self.question_num, row + 2, 0, 1, 9)

    # Required by GuiPage parent
    def refresh(self):
        if self.is_savable():
            self.finish_btn.setEnabled(True)
            self.save_btn.setEnabled(True)

            self.setTabOrder(self.add_answer_btn, self.save_btn)
            self.setTabOrder(self.save_btn, self.finish_btn)
            self.setTabOrder(self.finish_btn, self.cancel_btn)
            self.setTabOrder(self.cancel_btn, self.question)
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

    # Does there need to be a condition for minimum answers?
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

        # Send quiz off to be stored
        # TODO: 
        self.view.create_quiz(json.dumps(self.quiz, default=vars))
        self.primary.change_page(pages.START)

    def cancel_pressed(self):
        # To prevent cached value effect.
        self.clear_page()

        # TODO: Consider changing primary to window_manager
        self.primary.change_page(pages.START)

    def add_answer_pressed(self):
        self.configure_answers(1, self.last_answer_row + 1)
        self.shift_btns()

    @GuiPage.update_after
    def clear_page(self):
        self.question.clear()
        for answer in self.answers:
            answer.text.clear()
        self.remove_extra_answers()
        self.question.setFocus()

    # TODO: Basically just resetting the page to the default question amount
    def remove_extra_answers(self):
        answers_to_remove = self.answers[2:]
        self.answers = self.answers[:2]

        for answer in answers_to_remove:
            self.page_layout.removeWidget(answer.text)
            self.page_layout.removeWidget(answer.correct)
            answer.text.deleteLater()
            answer.correct.deleteLater()

    # TODO: I wonder what this was a fix for
    def focus(self):
        self.clear_page()
