from enum import IntEnum
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from start_page import StartPage
from create_question import CreateQuestion
from quiz_question import QuizQuestion
from edit_overview import EditOverview
from view import View
from quiz_handler import QuizHandler
from quiz import Quiz
from results_overview import ResultsOverview
from results_details import ResultsDetails
from edit_question import EditQuestion
from gui_constants import pages


class MainWindow(QMainWindow):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.page_container = QStackedWidget()
        self.current_quiz = None
        self.pages = []
        self.ss = "font-size:12pt"

        self.init_page(StartPage)
        self.init_page(CreateQuestion)
        self.init_page(QuizQuestion)
        self.init_page(EditOverview)
        self.init_page(ResultsOverview)
        self.init_page(ResultsDetails)
        self.init_page(EditQuestion)

        self.change_page(pages.START)

        self.setCentralWidget(self.page_container)

    def init_page(self, page):
        page = page(self)
        self.pages.append(page)
        self.page_container.addWidget(page)

    def change_page(self, page: pages):
        self.last_page = self.page_container.currentIndex()
        self.pages[page.value].refresh()
        self.page_container.setCurrentIndex(page.value)

    def return_to_home(self):
        for page in self.pages:
            try:
                page.clear()
            except AttributeError:
                pass
        self.change_page(pages.START)

    def start_quiz(self, name=None, handler=None):
        if not handler:
            quiz = Quiz(name)
            handler = QuizHandler(quiz)
        self.pages[pages.QUIZ.value].start_quiz(handler)
        self.change_page(pages.QUIZ)

    def edit_quiz(self, name):
        self.pages[pages.EDIT_OVERVIEW.value].name = name
        self.change_page(pages.EDIT_OVERVIEW)

    def edit_question(self, question):
        self.pages[pages.EDIT_QUESTION.value].question_obj = question
        self.pages[pages.EDIT_QUESTION.value].refresh()
        self.change_page(pages.EDIT_QUESTION)

    def question_edited(self, question):
        self.pages[pages.EDIT_OVERVIEW.value].editor.edited = True
        self.pages[pages.EDIT_OVERVIEW.value].edited_question = question
        self.change_page(pages.EDIT_OVERVIEW)

    def quiz_results(self, handler):
        self.pages[pages.RESULTS_OVERVIEW.value].handler = handler
        self.change_page(pages.RESULTS_OVERVIEW)

    def results_details(self, handler):
        self.pages[pages.RESULTS_DETAILS.value].handler = handler
        self.pages[pages.RESULTS_DETAILS.value].refresh()
        self.change_page(pages.RESULTS_DETAILS)

    def go_back(self):
        self.pages_container.setCurrentIndex(self.last_page)

    def change_pages(self, page, *args, **kwargs):
        self.page_container.setCurrentIndex(page.value)
        self.pages[page.value].focus(*args, **kwargs)


app = QApplication(sys.argv)
view = View()
window = MainWindow(view)
window.show()
app.exec()
