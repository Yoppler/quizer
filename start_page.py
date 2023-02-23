from PyQt6.QtWidgets import (
        QGridLayout,
        QPushButton,
        QListWidget,
        QAbstractItemView,
        QInputDialog, 
        QMessageBox,
)


from gui_page import GuiPage
from gui_constants import pages

class StartPage(GuiPage):
    def __init__(self, primary):
        super().__init__()
        self.primary = primary
        self.view = primary.view
        self.setup()

    @GuiPage.update_after
    def setup(self):
        layout = QGridLayout()
        self.create_btn = QPushButton("Create Quiz")
        self.create_btn.setStyleSheet(self.primary.ss)
        self.quiz_list = QListWidget()
        self.quiz_list.setStyleSheet(self.primary.ss)
        self.start_btn = QPushButton("Start")
        self.start_btn.setStyleSheet(self.primary.ss)
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setStyleSheet(self.primary.ss)
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setStyleSheet(self.primary.ss)

        self.create_btn.clicked.connect(self.create_pressed)
        self.quiz_list.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.quiz_list.itemSelectionChanged.connect(self.quiz_selected)
        self.quiz_list.itemDoubleClicked.connect(self.start_pressed)

        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.start_pressed)

        self.edit_btn.setEnabled(False)
        self.edit_btn.clicked.connect(self.edit_pressed)

        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_pressed)

        layout.addWidget(self.create_btn, 0, 0, 1, 3)
        layout.addWidget(self.quiz_list, 1, 0, 5, 3)
        layout.addWidget(self.start_btn, 6, 2, 1, 1)
        layout.addWidget(self.edit_btn, 6, 1, 1, 1)
        layout.addWidget(self.delete_btn, 6, 0, 1, 1)

        self.setLayout(layout)
        self.show()

    def refresh(self):
        quizes = self.view.list_quizes()
        if len(quizes) != self.quiz_list.count():
            self.quiz_list.clear()
            self.quiz_list.addItems(quizes)
        if len(self.quiz_list.selectedItems()) == 0:
            self.start_btn.setEnabled(False)
            self.edit_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
            # Only update quizes when nothing selected
        else:
            self.start_btn.setEnabled(True)
            self.edit_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)

    def create_pressed(self):
        name, confirm = QInputDialog.getText(
                self,
                "Quiz name?",
                "What would you like to name the quiz?"
        )

        if len(name) > 0 and confirm:
            self.view.quiz_name = name
            self.primary.change_page(pages.CREATE)

    @GuiPage.update_after
    def quiz_selected(self):
        pass

    def start_pressed(self):
        self.view.quiz_name = self.get_selection()
        self.primary.start_quiz(self.get_selection())

    def edit_pressed(self):
        self.primary.edit_quiz(self.get_selection())

    @GuiPage.update_after
    def delete_pressed(self, _):
        selection = self.get_selection()

        if not selection:
            return

        msg = QMessageBox(self)
        msg.setStyleSheet(self.primary.ss)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setStandardButtons(
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
        )
        msg.setInformativeText(
                f"Are you sure you want to delete {selection}?"
        )
        msg.setWindowTitle("Are you sure?")

        confirm = msg.exec()
        if confirm == QMessageBox.StandardButton.Yes:
            self.view.quiz_name = selection
            self.view.delete_quiz()

    def get_selection(self):
        cur_selection = self.quiz_list.selectedItems()
        if cur_selection:
            return cur_selection[0].text()
