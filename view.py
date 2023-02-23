import json
from pathlib import Path

class View:
    def __init__(self):
        self.quiz_name = None
        self.quiz_dir = Path("./quizes")
        self.init_dir()

    def create_quiz(self, content):
        if not self.quiz_name:
            return

        quiz = self.quiz_dir / f"{self.quiz_name}.json"

        if quiz.exists():
            raise FileExistsError

        with open(quiz, 'w') as hndl:
            hndl.write(content)

    def delete_quiz(self):
        if not self.quiz_name:
            return

        quiz = self.quiz_dir / f"{self.quiz_name}.json"

        if not quiz.exists():
            raise FileNotFoundError

        quiz.unlink()

    def load_quiz(self):
        if not self.quiz_name:
            return

        quiz = self.quiz_dir / f"{self.quiz_name}.json"

        if not quiz.exists():
            raise FileNotFoundError

        with open(quiz, 'r') as hndl:
            content = hndl.read()

        quiz = json.loads(content)

    def list_quizes(self):
        if not self.quiz_dir.exists():
            return

        files = list(self.quiz_dir.glob("*.json"))
        files = [str(f.stem) for f in files]
        return files

    def init_dir(self):
        if not self.quiz_dir.exists():
            self.quiz_dir.mkdir()

        
