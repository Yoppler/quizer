from PyQt6.QtWidgets import (
        QGridLayout,
        QLabel,
        QFrame,
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
        layout = QGridLayout()
        self.title = QLabel()
        self.numerator = QLabel()
        line = QFrame()
        self.denominator = QLabel()
        equals = QLabel("=")
        self.percent = QLabel()
        percent_sign = QLabel("%")
        restart_btn = QPushButton("Restart")
        restart_btn.setStyleSheet(self.primary.ss)
        self.restart_wrong_btn = QPushButton("Restart Wrong Only")
        self.restart_wrong_btn.setStyleSheet(self.primary.ss)
        details_btn = QPushButton("Details")
        details_btn.setStyleSheet(self.primary.ss)
        details_btn.clicked.connect(self.details_pressed)
        finish_btn = QPushButton("Finish")
        finish_btn.setStyleSheet(self.primary.ss)

        self.score_overview = QLabel()

        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        self.title.setFont(title_font)
        self.title.setWordWrap(True)

        self.score_overview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overview_font = QFont()
        overview_font.setPointSize(20)
        self.score_overview.setFont(overview_font)

        restart_btn.clicked.connect(self.restart_pressed)
        self.restart_wrong_btn.clicked.connect(self.restart_wrong_pressed)
        finish_btn.clicked.connect(self.finish_pressed)

        layout.addWidget(self.title,0,0,1,2)
        layout.addWidget(self.score_overview,1,0,1,2)
        layout.addWidget(restart_btn,2,0,1,1)
        layout.addWidget(self.restart_wrong_btn,3,0,1,1)
        layout.addWidget(details_btn,2,1,1,1)
        layout.addWidget(finish_btn,3,1,1,1)

        self.setLayout(layout)
        self.show()

    def refresh(self):
        if self.handler is None:
            return

        if self.score is None:
            self.score = self.handler.calculate_score()

        self.title.setText(self.handler.get_title())
        self.numerator.setText(str(self.score.numerator))
        self.denominator.setText(str(self.score.denominator))
        self.percent.setText(str(self.score.percent))

        self.score_overview.setText(f"{self.score.numerator}/{self.score.denominator} = {self.score.percent}%")

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
