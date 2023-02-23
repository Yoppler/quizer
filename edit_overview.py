from PyQt6.QtWidgets import (
    QGridLayout,
    QListWidget,
    QPushButton,
)

from gui_page import GuiPage
from quiz_editor import QuizEditor


class EditOverview(GuiPage):
    def __init__(self, primary):
        super().__init__()
        self.primary = primary
        self.name = None
        self.editor = None
        self.question_obj = None
        self.edited_question = None
        self.needs_saving = False
        self.setup()

    def setup(self):
        layout = QGridLayout()
        self.question_list = QListWidget()
        self.question_list.setStyleSheet(self.primary.ss)
        self.question_list.itemSelectionChanged.connect(self.item_selected)
        self.question_list.setWordWrap(True)
        self.question_list.setAlternatingRowColors(True)
        self.question_list.setSpacing(5)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(self.primary.ss)
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setStyleSheet(self.primary.ss)
        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet(self.primary.ss)

        self.edit_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        cancel_btn.clicked.connect(self.cancel_pressed)
        self.edit_btn.clicked.connect(self.edit_pressed)
        self.save_btn.clicked.connect(self.save_pressed)

        layout.addWidget(self.question_list, 0, 0, 3, 3)
        layout.addWidget(cancel_btn, 3, 0, 1, 1)
        layout.addWidget(self.edit_btn, 3, 1, 1, 1)
        layout.addWidget(self.save_btn, 3, 2, 1, 1)

        self.setLayout(layout)
        self.show()

    def item_selected(self):
        if len(self.question_list.selectedItems()) == 1:
            self.edit_btn.setEnabled(True)
        else:
            self.edit_btn.setEnabled(False)

    def refresh(self):
        if not self.editor:
            self.editor = QuizEditor(self.name)

        self.populate_questions()

    def populate_questions(self):
        self.clear()
        if not self.editor:
            self.editor = QuizEditor(self.name)

        if self.edited_question is not None:
            self.save_btn.setEnabled(True)
            self.editor.replace_question(self.question_obj,
                                         self.edited_question)
            self.edited_question = None

        for question in self.editor.quiz.questions:
            self.question_list.addItem(question.text)

    def clear(self):
        #self.question_obj = None
        self.editor = None
        self.question_list.clear()

    def cancel_pressed(self):
        self.clear()
        self.primary.return_to_home()

    def edit_pressed(self):
        selection = self.question_list.selectedItems()
        if len(selection) == 0:
            return
        question = selection[0].text()

        self.question_obj = self.editor.get_question_by_text(question)
        self.primary.edit_question(self.question_obj)

    def save_pressed(self):
        self.editor.save_changes()
        self.clear()
        self.primary.return_to_home()
