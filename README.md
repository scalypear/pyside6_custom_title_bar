# CustomTitleBar
Implements a custom title bar which automatically replaces default title bar of a `QWidget` or `QMainWindow`. `CustomTitleBar` should be placed in the central widget of the root.


## Using CustomTitleBar in a QMainWindow
If the root is a `QMainWindow`, simply place `CustomTitleBar` as the first item in the `centralWidget`. The main content should be placed in a layout placed in a layout below the CustomTitleBar. So the structure will be:
- QMainWindow: 
  - centralWidget:
    - centralWidget layout:
      - CustomTitleBar widget
      - Content layout (add contents margins here):
        - App content

For example, see [`customtitlebar_example_qmainwindow.py`](examples/customtitlebar_example_qmainwindow.py) or see [below](#example-qmainwindow). 

## Using CustomTitleBar in a QWidget
If the root is a `QWidget`, place a layout, then a central widget in that layout, then place a vertical layout in the central widget, then place the the `CustomTitleBar`, then after that, place a layout which holds all of your app's other content (this is important because it will allow you to add back in contents margins that have to be removed from the higher level elements). So they structure will be:

- QWidget:
  - Container layout:
    - QWidget (i.e., acts as the central widget):
      - QVBoxLayout:
        - CustomTitleBar widget
        - Content layout (add contents margins here):
          - App content

For example, see [`customtitlebar_example_qwidget.py`](examples/customtitlebar_example_qwidget.py) or see [below](#example-qwidget).


# Examples

## Example: QMainWindow
```
class MainWindow(QMainWindow):
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
```
## Example: QWidget
```
class MainWindowWidget(QWidget):
    def __init__(self):
        super().__init__()

        """Required structure"""
        container_layout = QVBoxLayout(self)

        central_widget = QWidget(self)
        container_layout.addWidget(central_widget)

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

        """Adding menu bar items"""
        example_menu_1 = QMenu("Ex 1")
        example_action_1 = example_menu_1.addAction("Action 1")
        example_action_1.triggered.connect(lambda: print("example action 1"))
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
```
