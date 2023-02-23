
from PyQt6.QtWidgets import QWidget, QLayout

class GuiPage(QWidget):

    @staticmethod
    def update_after(func):
        def func_with_refresh(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.refresh()
        return func_with_refresh

    def refresh(self):
        """Elements that have conditions"""
        raise NotImplementedError("refresh must be implemented by subclass")

    def setup(self) -> QLayout:
        """For creation and placement of Widgets"""
        raise NotImplementedError("setup must be implemented by subclass")
