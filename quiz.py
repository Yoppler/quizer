from dataclasses import dataclass, field
from pathlib import Path
import json


class Quiz:
    def __init__(self, name):
        self.name = name

        self.dir = Path("./quizes")
        self.path = self.dir / f"{name}.json"
        self.exists = self.path.exists()
        self.content = None
        self.questions = []

        self.load_quiz()

    def load_quiz(self):
        if not self.exists:
            return

        with open(self.path, 'r') as hndl:
            content = hndl.read()

        self.content = json.loads(content)

        # populate questions list with Question objects
        for question in self.content:
            q = Question()
            q.text = question["text"]
            answers = question["answers"]
            for answer in answers:
                a = Answer()
                a.text = answer["text"]
                a.correct = answer["correct"]
                q.answers.append(a)
            self.questions.append(q)


@dataclass
class Question:
    text: str = ""
    answers: list = field(default_factory=list)


@dataclass
class Answer:
    text: str = ""
    correct: bool = False

    def __eq__(self, other):
        return self.text == other.text and \
               self.correct == other.correct
