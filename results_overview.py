from PyQt6.QtWidgets import (
        QGridLayout,
        QLabel,
        QPushButton,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from gui_page import GuiPage


class ResultsOverview(GuiPage):
    def __init__(self, primary):
        super().__init__()
        self.primary = primary
        self.handler = None
        self.score = None
        self.setup()

    def clear(self):
        self.handler = None
        self.score = None

    def setup(self):
        self.page_layout = QGridLayout()
        self.title = QLabel()
        restart_btn = QPushButton("Restart")
        self.restart_wrong_btn = QPushButton("Restart Wrong Only")
        details_btn = QPushButton("Details")
        finish_btn = QPushButton("Finish")
        self.score_overview = QLabel()
        title_font = QFont()
        overview_font = QFont()

        restart_btn.setStyleSheet(self.primary.ss)
        self.restart_wrong_btn.setStyleSheet(self.primary.ss)
        details_btn.setStyleSheet(self.primary.ss)
        finish_btn.setStyleSheet(self.primary.ss)

        title_font.setPointSize(20)
        title_font.setBold(True)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(title_font)
        self.title.setWordWrap(True)

        overview_font.setPointSize(20)
        self.score_overview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_overview.setFont(overview_font)

        restart_btn.clicked.connect(self.restart_pressed)
        self.restart_wrong_btn.clicked.connect(self.restart_wrong_pressed)
        finish_btn.clicked.connect(self.finish_pressed)
        details_btn.clicked.connect(self.details_pressed)

        self.page_layout.addWidget(self.title, 0, 0, 1, 2)
        self.page_layout.addWidget(self.score_overview, 1, 0, 1, 2)
        self.page_layout.addWidget(restart_btn, 2, 0, 1, 1)
        self.page_layout.addWidget(self.restart_wrong_btn, 3, 0, 1, 1)
        self.page_layout.addWidget(details_btn, 2, 1, 1, 1)
        self.page_layout.addWidget(finish_btn, 3, 1, 1, 1)

        self.setLayout(self.page_layout)
        self.show()

    def refresh(self):
        if self.handler is None:
            return

        if self.score is None:
            self.score = self.handler.calculate_score()

        num = self.score.numerator
        denom = self.score.denominator
        per = self.score.percent
        overview = f"{num}/{denom} = {per}%"

        self.title.setText(self.handler.get_title())
        self.score_overview.setText(overview)

        if len(self.handler.incorrect) == 0:
            self.restart_wrong_btn.setEnabled(False)

    def finish_pressed(self):
        self.primary.return_to_home()

    def restart_pressed(self):
        self.score = None
        self.handler.restart()
        self.primary.start_quiz(handler=self.handler)

    def restart_wrong_pressed(self):
        self.score = None
        self.handler.restart_wrong_only()
        self.primary.start_quiz(handler=self.handler)

    def details_pressed(self):
        self.primary.results_details(self.handler)
