from custom_title_bar import CustomTitleBar
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMenu
)


class MainWindow(QMainWindow):
    """
    Example of an app which uses a QMainWindow as its root, using the CustomTitleBar.

    **Important**: The central widget holds a QVBoxLayout which holds the title bar *and* a nested layout for the content (this nested layout allows you to add back in content margins that otherwise would be removed if you just put the content directly onto the central widget layout).
    """

    def __init__(self):
        super().__init__()
        self.resize(400,400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(central_widget_layout)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(
            10, 10, 10, 10
        )  # Adding back contents margins as we see fit

        title_bar = CustomTitleBar(
            root=self,
            change_btns_on_hover=True,
            close_btn_default_img_path="icons/close-btn-default.svg",
            close_btn_hover_img_path="icons/close-btn-hover.svg",
            min_btn_default_img_path="icons/min-btn-default.svg",
            min_btn_hover_img_path="icons/min-btn-hover.svg",
            max_btn_default_img_path="icons/max-btn-default.svg",
            max_btn_hover_img_path="icons/max-btn-hover.svg",
            normal_btn_default_img_path="icons/max-btn-default.svg",
            normal_btn_hover_img_path="icons/normal-btn-hover.svg",
            disabled_btn_img_path="icons/disabled-btn.svg",
            title_bar_text_title_text="Title text",
        )
        central_widget_layout.addWidget(title_bar)
        central_widget_layout.addLayout(content_layout)

        """Example: adding a menu bar"""
        example_menu_1 = QMenu("Ex 1")
        example_action_1 = example_menu_1.addAction("Action 1")
        example_action_1.triggered.connect(lambda: print("example action 1"))
        example_menu_1.addSeparator()
        example_action_2 = example_menu_1.addAction("Action 2")
        example_action_2.triggered.connect(lambda: print("example action 2"))

        example_menu_2 = QMenu("Ex 2")
        example_action_3 = example_menu_2.addAction("Action 3")
        example_action_3.triggered.connect(lambda: print("example action 3"))

        title_bar.add_menu_item(example_menu_1)
        title_bar.add_menu_item(example_menu_2)

        """Example content (not required)"""
        layout_1 = QHBoxLayout()
        layout_2 = QHBoxLayout()
        layout_3 = QVBoxLayout()
        content_layout.addLayout(layout_1)
        content_layout.addLayout(layout_2)
        content_layout.addLayout(layout_3)

        layout_1.addWidget(QLabel("Label 1"))
        layout_1.addWidget(QLabel("Label 2"))
        layout_1.addWidget(QLabel("Label 3"))

        layout_2.addWidget(QLabel("Label 4"))
        layout_2.addWidget(QLabel("Label 5"))
        layout_2.addWidget(QLabel("Label 6"))

        layout_3.addWidget(QPushButton("Btn 1"))
        layout_3.addWidget(QPushButton("Btn 2"))
        layout_3.addWidget(QPushButton("Btn 3"))


app = QApplication()
root = MainWindow()
root.show()
app.exec()