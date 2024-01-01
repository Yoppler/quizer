
from PyQt6.QtWidgets import QWidget, QLayout


class GuiPage(QWidget):

    # Used as a decorator in child classes, Will run some function
    # then proceed to refresh the page state, however the child defines
    @staticmethod
    def update_after(func):
        def func_with_refresh(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.refresh()
        return func_with_refresh

    # TODO: When should I refresh?
    # Want to update the gui objects based on some conditions being evaluated
    # Examples include checkbox state, button state, etc. 
    def refresh(self):
        """Elements that have conditions"""
        raise NotImplementedError("refresh must be implemented by subclass")

    def setup(self) -> QLayout:
        """For creation and placement of Widgets"""
        raise NotImplementedError("setup must be implemented by subclass")
