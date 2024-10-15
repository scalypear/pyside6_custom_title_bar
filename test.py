from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QSizePolicy,
    QToolButton,
    QStyle,
    QMenuBar,
    QMenu,
    QBoxLayout,
)
from PySide6.QtCore import Qt, QEvent, QObject, Signal
from PySide6.QtGui import QMouseEvent, QPixmap, QPalette, QAction, QColor
from typing import Optional


class MainWindow(QMainWindow):
    """
    Example of an app which uses a QMainWindow as its root, using the CustomTitleBar.

    **Important**: The central widget holds a QVBoxLayout which holds the title bar *and* a nested layout for the content (this nested layout allows you to add back in content margins that otherwise would be removed if you just put the content directly onto the central widget layout).
    """

    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(central_widget_layout)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(
            10, 10, 10, 10
        )  # Adding back contents margins as we see fit

        central_widget_layout.addWidget(CustomTitleBar(root=self))
        central_widget_layout.addLayout(content_layout)

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


class MainWindowWidget(QWidget):
    """
    Example of an app which uses a QWidget as its root, using the CustomTitleBar.

    **Important**: For this to work, we need to mimic the structure of a QMainWindow. The structure MUST be as follows:
    1) A container layout: This will be used to hold a QWidget that will act as our 'central widget'.
    2) A QWidget: This is our 'central widget'; it should be added directly to the container layout.
    3) A QVBoxLayout: This is the layout that will hold the CustomTitleBar, followed by another layout that will hold the app content; it should be added directly to the QWidget.
    4) The CustomTitleBar: This should be added to the QVBoxLayout if you want the title bar to be at the top of your app.
    5) A content layout: This layout will hold all of the content of your app (i.e., all of the stuff that isn't the title bar). The reason we have this layout instead of directly placing the content on the QVBoxLayout below the CustomTitleBar is because it allows us to add back in contents margins. (Contents margins on the container layout and the QVBoxLayout are removed by the CustomTitleBar to prevent weird spacing occuring around the CustomTitleBar widget).

    """

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

        central_widget_layout.addWidget(CustomTitleBar(root=self))
        central_widget_layout.addLayout(content_layout)

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


class CustomTitleBar(QWidget):
    def __init__(self, root, root_bg_color=None):
        super().__init__()
        self.root = root
        self.root_bg_color = root_bg_color

        if isinstance(root, QMainWindow):
            self.is_QMainWindow = True
            if not root.centralWidget():
                self.check_central_widget(root)
            else:
                self.central_layout_or_widget = root.centralWidget()
                self.initialize(root=root, root_bg_color=self.root_bg_color)
        else:
            self.is_QMainWindow = False
            if not root.layout():
                self.check_main_layout(root)
            else:
                root.setContentsMargins(0, 0, 0, 0)
                root.layout().setContentsMargins(0, 0, 0, 0)
                self.central_layout_or_widget = root.layout().itemAt(0).widget()
                self.initialize(root=root, root_bg_color=self.root_bg_color)

    # Init content
    def initialize(self, root, root_bg_color):

        self.get_screen_limits()

        root_central_widget_bg_col = (
            (
                self.central_layout_or_widget.palette()
                .color(self.central_layout_or_widget.backgroundRole())
                .getRgb()
            )
            if root_bg_color is None
            else root_bg_color
        )

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.central_layout_or_widget.setObjectName("central-widget-tag")

        root.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
        root.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.central_layout_or_widget.layout().setContentsMargins(0, 0, 0, 0)
        self.central_layout_or_widget.setContentsMargins(0, 0, 0, 0)
        self.central_layout_or_widget.setStyleSheet(
            f"#central-widget-tag {{background-color:rgba{root_central_widget_bg_col}; border-top-left-radius:12px; border-top-right-radius:12px;}}"
        )

        # Layout to hold container
        master_layout = QVBoxLayout(self)
        master_layout.setSpacing(0)
        master_layout.setContentsMargins(0, 0, 0, 0)

        # Container to hold content
        title_bar_container = QWidget(self)
        title_bar_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        master_layout.addWidget(title_bar_container)
        title_bar_container.setStyleSheet(
            "border-top-left-radius: 12px; border-top-right-radius:12px; background-color:pink"
        )
        title_bar_container.setContentsMargins(12, 12, 12, 12)

        # Container layout
        container_layout = QVBoxLayout(title_bar_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(12)

        # Title bar layout
        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setAlignment(Qt.AlignLeft)

        container_layout.addLayout(title_bar_layout)

        title_bar_layout.addWidget(
            TitleBtns(
                root=root,
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
            )
        )
        title_bar_layout.addWidget(TitleText("Title Text"))

        title_menu = TitleMenuBar(menu_bar_border="2px solid red")
        container_layout.addWidget(title_menu)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.location = event.position().toPoint()
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.previous_x = self.root.window().pos().x()
        print(self.previous_x)
        if self.location is not None:
            diff = event.position().toPoint() - self.location
            new_x = self.root.window().x() + diff.x()
            new_y = self.root.window().y() + diff.y()

            new_x = self.check_stick(new_x)

            self.root.window().move(new_x, new_y)

        super().mouseMoveEvent(event)
        event.accept()

    def check_stick(self, new_x):
        window_width = self.root.window().width() 
        window_right_side = window_width + new_x


        # Left side
        if new_x < self.previous_x: # mouse is moving leftwards
            if self.stick_threshold_left < new_x < self.screen_geo_left:
                new_x = self.screen_geo_left
            elif new_x <= self.stick_threshold_left:
                new_x += self.stick_threshold

        


        # Right side
        if new_x > self.previous_x: # mouse if moving rightwards
            if self.stick_threshold_right > window_right_side > self.screen_geo_right:
                new_x = self.screen_geo_right - window_width
            elif window_right_side >= self.stick_threshold_right:
                new_x -= self.stick_threshold

        return new_x   

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.location = None
        super().mouseReleaseEvent(event)
        event.accept()

    def get_screen_limits(self):
        self.previous_x = self.root.window().pos().x()

        self.screen_geo = QApplication.primaryScreen().geometry()
        self.screen_geo_left = self.screen_geo.left()
        self.screen_geo_right = self.screen_geo.right()
        self.screen_geo_top = self.screen_geo.top()
        self.screen_geo_bottom = self.screen_geo.bottom()

        self.stick_threshold = 30
        self.stick_threshold_left = -1 * self.stick_threshold
        self.stick_threshold_right = self.stick_threshold + self.screen_geo_right

    def add_menu_item(self, menu: QMenu):
        """
        Adds a `QMenu` to the `QMenuBar` that's inside the `TitleMenuBar` of the `CustomTitleBar`.

        :param menu: The menu to be added. The menu should already have all of its actions added beforehand.
        :type menu: QMenu
        """
        self.menu_bar.add_menu_item(menu=menu)

    def check_central_widget(self, root):
        """If the centralWidget of root has not been set yet, update root's .setCentralWidget() to call the initialization of CustomTitleBar (this way, it doesn't matter whether the user sets the central widget before or after creating a CustomTitleBar)"""
        default_set_central_widget = root.setCentralWidget
        root.initialize_titlebar = self.initialize

        def new_set_central_widget(widget):
            default_set_central_widget(widget)
            self.central_layout_or_widget = root.centralWidget()
            root.initialize_titlebar(root=root, root_bg_color=self.root_bg_color)

        root.setCentralWidget = new_set_central_widget

    def check_main_layout(self, root):
        """If the topmost layout of the root has not been set yet, update root's .setLayout() to call the initialization of CustomTitleBar (this way, it doesn't matter whether the user sets the central widget before or after creating a CustomTitleBar)"""

        default_set_layout = root.setLayout
        root.initialize_titlebar = self.initialize

        def new_set_layout(layout):
            default_set_layout(layout)
            self.central_layout_or_widget = root
            root.initialize_titlebar(root=root, root_bg_color=self.root_bg_color)

        root.setLayout = new_set_layout


class TitleBtns(QWidget):

    def __init__(
        self,
        root: QWidget | QMainWindow,
        close_btn_default_img_path: Optional[str] = None,
        min_btn_default_img_path: Optional[str] = None,
        max_btn_default_img_path: Optional[str] = None,
        normal_btn_default_img_path: Optional[str] = None,
        disabled_btns_on_focus_out: Optional[bool] = True,
        disabled_btn_img_path: Optional[str] = None,
        btn_size: Optional[tuple[int, int]] = (12, 12),
        change_btns_on_hover: Optional[bool] = False,
        change_cursor_on_btn_hover: Optional[bool] = False,
        btn_hover_cursor_shape: Optional[
            Qt.CursorShape
        ] = Qt.CursorShape.PointingHandCursor,
        close_btn_hover_img_path: Optional[str] = None,
        min_btn_hover_img_path: Optional[str] = None,
        max_btn_hover_img_path: Optional[str] = None,
        normal_btn_hover_img_path: Optional[str] = None,
    ):
        """Initializes close, min, max, and normal title bar buttons and associated functionality.

        :param root: The root window whose titlebar is being replaced.
        :type root: QWidget | QMainWindow

        :param close_btn_default_img_path: Path to the image file being used for the default close button. If path is None, QStyle.StandardPixmap.SP_TitleBarCloseButton will be used. Defaults to None.
        :type close_btn_default_img_path: Optional[str]

        :param min_btn_default_img_path: Path to the image file being used for the default minimize button. If path is None, QStyle.StandardPixmap.SP_TitleBarMinButton will be used. Defaults to None.
        :type min_btn_default_img_path: Optional[str]

        :param max_btn_default_img_path: Path to the image file being used for the default maximize button. If path is None, QStyle.StandardPixmap.SP_TitleBarMaxButton will be used. Defaults to None.
        :type max_btn_default_img_path: Optional[str]

        :param normal_btn_default_img_path: Path to the image file being used for the default normal button. If path is None, QStyle.StandardPixmap.SP_TitleBarNormalButton will be used. Defaults to None.
        :type normal_btn_hover_img_path: Optional[str]

        :param disabled_btns_on_focus_out: Whether or not the appearance of the buttons should change to a disabled appearance upon focus out of the application. Defaults to True.
        :type disable_btns_on_focus_out: Optional[bool]

        :param disabled_btn_image_path: Path to the image file being used for the disabled buttons. If path is None, QStyle.StandardPixmap.SP_TitleBarMinButton will be used. Defaults to None.
        :type disabled_btn_image_path: Optional[str]

        :param btn_size: The width and height in pixels of the buttons. Defalts to (14, 14)
        :type btn_size: Optional[tuple(int, int)]

        :param change_btns_on_hover: Flag for whether buttons should change from default to hover variant on hover. If True, file paths for the hover variants must be given in addition to paths for the default variants. If False, only the default variants' paths must be specified. Defaults to False.
        :type change_btns_on_hover: Optional[bool]

        :param change_cursor_on_btn_hover: Flag for whether the cursor should change when hovering over the buttons. Defaults to False.
        :type change_cursor_on_btn_hover: Optional[bool]

        :param btn_hover_cursor_shape: Specifies what cursor shape to use for button hovers. Defaults to Qt.CursorShape.PointingHandCursor.
        :type btn_hover_cursor_shape: Optional[Qt.CursorShape]

        :param close_btn_hover_img_path: Path to the image file being used for the hover close button. If path is None, QStyle.StandardPixmap.SP_TitleBarCloseButton will be used. Defaults to None.
        :type normal_btn_hover_img_path: Optional[str]

        :param min_btn_hover_img_path: Path to the image file being used for the hover min button. If path is None, QStyle.StandardPixmap.SP_TitleBarMinButton will be used. Defaults to None.
        :type min_btn_hover_img_path: Optional[str]

        :param max_btn_hover_img_path: Path to the image file being used for the hover max button. If path is None, QStyle.StandardPixmap.SP_TitleBarMaxButton will be used. Defaults to None.
        :type max_btn_hover_img_path: Optional[str]

        :param normal_btn_hover_img_path: Path to the image file being used for the hover normal button. If path is None, QStyle.StandardPixmap.SP_TitleBarNormalButton will be used. Defaults to None.
        :type normal_btn_hover_img_path: Optional[str]

        """
        super().__init__()

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.change_btns_on_hover = change_btns_on_hover
        self.change_cursor_on_btn_hover = change_cursor_on_btn_hover
        self.btn_hover_cursor_shape = btn_hover_cursor_shape

        self.close_btn_default_img_path = close_btn_default_img_path
        self.close_btn_hover_img_path = close_btn_hover_img_path
        self.min_btn_default_img_path = min_btn_default_img_path
        self.min_btn_hover_img_path = min_btn_hover_img_path
        self.max_btn_default_img_path = max_btn_default_img_path
        self.max_btn_hover_img_path = max_btn_hover_img_path
        self.normal_btn_default_img_path = normal_btn_default_img_path
        self.normal_btn_hover_img_path = normal_btn_hover_img_path
        self.disabled_btn_img_path = disabled_btn_img_path

        self.setStyleSheet("border: 0px")
        self.setContentsMargins(0, 0, 0, 0)

        self.root = root
        self.get_icons()
        self.monitor_root_window_state_change()
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        self.setLayout(layout)

        self.close_btn = QToolButton()
        self.min_btn = QToolButton()
        self.max_btn = QToolButton()
        self.normal_btn = QToolButton()

        for btn in [self.close_btn, self.min_btn, self.max_btn, self.normal_btn]:
            btn.setFixedSize(btn_size[0], btn_size[1])
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            if self.change_btns_on_hover:
                btn.setCursor(self.btn_hover_cursor_shape)
            layout.addWidget(btn)

        self.normal_btn.setVisible(False)
        self.set_default_icons()
        self.add_btn_func()
        if disabled_btns_on_focus_out:
            self.monitor_root_focus()

    def enterEvent(self, event):
        """
        Adds to the enterEvent to trigger the set_hover_icons method if change_btns_on_hover is True.
        """
        if self.change_btns_on_hover:
            self.set_hover_icons()
        super().enterEvent(event)
        event.accept()

    def leaveEvent(self, event):
        """
        Adds to the leaveEvent to trigger the set_default_icons method if change_btns_on_hover is True.
        """
        if self.change_btns_on_hover:
            self.set_default_icons()
        super().leaveEvent(event)
        event.accept()

    def get_icons(self):
        """
        Initalizes the button icon attributes with either the icon file path, or a default icon if no file path is provided.
        """
        self.icon_close_btn_default = (
            QPixmap(self.close_btn_default_img_path)
            if self.close_btn_default_img_path is not None
            else self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton)
        )
        self.icon_close_btn_hover = (
            QPixmap(self.close_btn_hover_img_path)
            if self.close_btn_hover_img_path is not None
            else self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton)
        )

        self.icon_min_btn_default = (
            QPixmap(self.min_btn_default_img_path)
            if self.min_btn_default_img_path is not None
            else self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMinButton)
        )
        self.icon_min_btn_hover = (
            QPixmap(self.min_btn_hover_img_path)
            if self.min_btn_hover_img_path is not None
            else self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMinButton)
        )

        self.icon_max_btn_default = (
            QPixmap(self.max_btn_default_img_path)
            if self.max_btn_default_img_path is not None
            else self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton)
        )
        self.icon_max_btn_hover = (
            QPixmap(self.max_btn_hover_img_path)
            if self.max_btn_hover_img_path is not None
            else self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton)
        )

        self.icon_normal_btn_default = (
            QPixmap(self.normal_btn_default_img_path)
            if self.normal_btn_default_img_path is not None
            else self.style().standardIcon(
                QStyle.StandardPixmap.SP_TitleBarNormalButton
            )
        )
        self.icon_normal_btn_hover = (
            QPixmap(self.normal_btn_hover_img_path)
            if self.normal_btn_default_img_path is not None
            else self.style().standardIcon(
                QStyle.StandardPixmap.SP_TitleBarNormalButton
            )
        )
        self.icon_disabled = (
            QPixmap(self.disabled_btn_img_path)
            if self.disabled_btn_img_path is not None
            else self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMinButton)
        )

    def set_default_icons(self):
        """
        Changes the buttons to have the default appearance.
        """
        self.close_btn.setIcon(self.icon_close_btn_default)
        self.min_btn.setIcon(self.icon_min_btn_default)
        self.max_btn.setIcon(self.icon_max_btn_default)
        self.normal_btn.setIcon(self.icon_normal_btn_default)

    def set_hover_icons(self):
        """
        Changes the buttons to have the hover appearance.
        """
        self.close_btn.setIcon(self.icon_close_btn_hover)
        self.min_btn.setIcon(self.icon_min_btn_hover)
        self.max_btn.setIcon(self.icon_max_btn_hover)
        self.normal_btn.setIcon(self.icon_normal_btn_hover)

    def set_disabled_icons(self):
        """
        Changes the buttons to have the disabled appearance.
        """
        self.close_btn.setIcon(self.icon_disabled)
        self.min_btn.setIcon(self.icon_disabled)
        self.max_btn.setIcon(self.icon_disabled)
        self.normal_btn.setIcon(self.icon_disabled)

    def add_btn_func(self):
        """
        Connects the functionality to the buttons.
        """
        self.close_btn.clicked.connect(self.root.close)
        self.max_btn.clicked.connect(self.root.showMaximized)
        self.min_btn.clicked.connect(self.root.showMinimized)
        self.normal_btn.clicked.connect(self.root.showNormal)

    def monitor_root_window_state_change(self):
        """
        Monitors for changes in the root window's state (minimized, maximized, normal). If the root's window state is maximized or normal, the `adjust_btn_display` method.
        """
        super_change_event = self.root.changeEvent

        def adjust_btn_display(event):
            """
            Makes the normal button hidden and the maximize button visible if the root's window state is normal, and makes the normal button visible and the maximize button hidden if the root's window state is maximized.
            """
            if event.type() == QEvent.Type.WindowStateChange:
                if self.root.windowState() == Qt.WindowState.WindowMaximized:
                    self.normal_btn.setVisible(True)
                    self.max_btn.setVisible(False)
                else:
                    self.normal_btn.setVisible(False)
                    self.max_btn.setVisible(True)

            super_change_event(event)
            event.accept()

        self.root.changeEvent = adjust_btn_display

    def monitor_root_focus(self):
        """
        Monitor's root window's focus (at the application level) to call the `focus_change` method when the focus changes.
        """

        def focus_change(_, new):
            """
            If the focus is changed such that the app is not in focus, the disabled icons are set. Else, the default icons are set.
            """
            if new is None:
                self.set_disabled_icons()

            else:
                self.set_default_icons()

        QApplication.instance().focusChanged.connect(focus_change)


class TitleText(QLabel):
    def __init__(
        self,
        title_bar_text_title_text: Optional[str] = "",
        title_bar_text_bg_color: Optional[str] = None,
        title_bar_text_font_size: Optional[str] = "15px",
        title_bar_text_font_color: Optional[str] = "#fff",
        title_bar_text_font: Optional[str] = "arial",
        title_bar_text_font_weight: Optional[str] = "bold",
        title_bar_text_additional_qss: Optional[str] = "",
    ):
        """
        Initializes the title bar text.

        :param title_bar_text_title_text: The text for title of the window. Defaults to "".
        :type title_bar_text_title_text: Optional[str].
        :param title_bar_text_bg_color: The background color for title of the window. Defaults to the same color as the title bar.
        :type title_bar_text_bg_color: Optional[str].
        :param title_bar_text_font_size: The font size for title of the window. Defaults to "15px".
        :type title_bar_text_font_size: Optional[str].
        :param title_bar_text_font_color: The font color for title of the window. Defaults to "#fff".
        :type title_bar_text_font_color: Optional[str].
        :param title_bar_text_font: The font for title of the window. Defaults to "arial".
        :type title_bar_text_font: Optional[str].
        :param title_bar_text_font_weight: The font weight for title of the window. Defaults to "bold".
        :type title_bar_text_font_weight: Optional[str].
        :param title_bar_text_additional_qss: The font weight for title of the window. Defaults to "bold".
        :type title_bar_text_additional_qss: Optional[str].

        """
        super().__init__()
        self.setText(title_bar_text_title_text)
        self.setAlignment(Qt.AlignVCenter)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet(
            f"""
                background-color: {title_bar_text_bg_color}; 
                font-size: {title_bar_text_font_size}; 
                font-family: '{title_bar_text_font}';
                font-weight: {title_bar_text_font_weight};
                color: {title_bar_text_font_color};
                {title_bar_text_additional_qss}
        """
        )


class TitleMenuBar(QMenuBar):
    def __init__(
        self,
        menu_bar_border: Optional[str] = "0px solid black",
        menu_bar_bg_color: Optional[str] = "",
        menu_bar_border_radius: Optional[str] = "0px",
        menu_bar_padding: Optional[str] = "0px",
        menu_bar_font: Optional[str] = "arial",
        menu_bar_font_color: Optional[str] = "#fff",
        menu_bar_font_size: Optional[str] = "14px",
        menu_bar_additional_qss: Optional[str] = "",
        menu_bar_item_bg_color: Optional[str] = "",
        menu_bar_item_additional_qss: Optional[str] = "",
        menu_bar_item_hover_bg_color: Optional[str] = "",
        menu_bar_item_hover_additional_qss: Optional[str] = "",
        menu_bar_dropdown_additional_qss: Optional[str] = "",
        menu_bar_dropdown_font: Optional[str] = None,
        menu_bar_dropdown_item_padding: Optional[str] = "3px 10px",
        menu_bar_dropdown_item_bg_color: Optional[str] = "",
        menu_bar_dropdown_item_additional_qss: Optional[str] = "",
        menu_bar_dropdown_item_hover_bg_color: Optional[str] = "",
        menu_bar_dropdown_item_hover_additional_qss: Optional[str] = "",
    ):
        """
        Creates a default menu bar for the `CustomTitleBar` which can be used to add menu items and actions with the `add_menu_item` method.

        :param menu_bar_border: The border of the menu bar. Defaults to "0px solid black".
        :type menu_bar_border: Optional[str]
        :param menu_bar_bg_color: The background color of the menu bar. Defaults to "".
        :type menu_bar_bg_color: Optional[str]
        :param menu_bar_border_radius: The border radius of the menu bar. Defaults to "0px".
        :type menu_bar_border_radius: Optional[str]
        :param menu_bar_padding: The padding (space between border and content) of the menu bar. Defaults to "0px".
        :type menu_bar_padding: Optional[str]
        :param menu_bar_font: The font family of the menu bar. Defaults to "arial".
        :type menu_bar_font: Optional[str]
        :param menu_bar_font_color: The font color of menu bar text. Defaults to "#fff".
        :type menu_bar_font_color: Optional[str]
        :param menu_bar_font_size: The font size of the menu bar. Defaults to "14px".
        :type menu_bar_font_size: Optional[str]
        :param menu_bar_additional_qss: Any additional QSS for the menu bar. Defaults to "".
        :type menu_bar_additional_qss: Optional[str]

        :param menu_bar_item_bg_color: The background color of the menu bar items (the menus). Defaults to "".
        :type menu_bar_item_bg_color: Optional[str]
        :param menu_bar_item_additional_qss: Additional QSS for the menu bar items (the menus). Defaults to "".
        :type menu_bar_item_additional_qss: Optional[str]

        :param menu_bar_item_hover_bg_color: The background hover color of menu bar items (the menus). Defaults to "".
        :type menu_bar_item_hover_bg_color: Optional[str]
        :param menu_bar_item_hover_bg_color: The background hover color of menu bar items (the menus). Defaults to "".
        :param menu_bar_item_hover_additional_qss: Additional QSS for menu bar items hover. Defaults to "".
        :type menu_bar_item_hover_additional_qss: Optional[str]

        :param menu_bar_dropdown_font: The font family for the dropdowns of the menus. Defaults to the same font as `menu_bar_font`.
        :type menu_bar_dropdown_font: Optional[str].
        :param menu_bar_dropdown_additional_qss: Additional QSS for the actual dropdown area of the menu items. Defaults to "".
        :type menu_bar_dropdown_additional_qss: Optional[str]

        :param menu_bar_dropdown_item_padding: The padding for the dropdown items. Defaults to "3px 10px".
        :type menu_bar_dropdown_item_padding: Optional[str]
        :param menu_bar_dropdown_item_bg_color: The background color for the dropdown items. Defaults to "".
        :type menu_bar_dropdown_item_bg_color: Optional[str]
        :param menu_bar_dropdown_item_additional_qss: Additional QSS for the dropdown items. Defaults to ".
        :type menu_bar_dropdown_item_additional_qss: Optional[str]

        :param menu_bar_dropdown_item_hover_bg_color: The background color of the dropdown items upon hover. Defaults to "".
        :type menu_bar_dropdown_item_hover_bg_color: Optional[str]
        :param menu_bar_dropdown_item_hover_additional_qss: Additional QSS for the dropdown items upon hover. Defaults to "".
        :type menu_bar_dropdown_item_hover_additional_qss: Optional[str]

        """
        super().__init__()

        if menu_bar_dropdown_font is None:
            menu_bar_dropdown_font = menu_bar_font

        # Menu bar
        self.menu = self
        self.menu.setNativeMenuBar(False)

        file_menu = QMenu("File", self.menu)
        file_menu.addAction("Open")
        file_menu.addAction("Save")
        self.menu.addMenu(file_menu)
        self.menu.setNativeMenuBar(False)

        edit_menu = QMenu("Edit", self.menu)
        edit_menu.addAction("Open")
        edit_menu.addAction("Save")
        self.menu.addMenu(edit_menu)

        self.menu.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setStyleSheet(
            # Main bar
            f"""QMenuBar {{ 
                    border: {menu_bar_border};
                    border-radius: {menu_bar_border_radius};
                    background-color:{menu_bar_bg_color};
                    padding: {menu_bar_padding};
                    font-family: {menu_bar_font};
                    color: {menu_bar_font_color};
                    font-size: {menu_bar_font_size};
                    {menu_bar_additional_qss}
                }}
            """
            # Menu bar items
            f"""QMenuBar::item {{
                    background-color: {menu_bar_item_bg_color};
                    {menu_bar_item_additional_qss}
            }}"""
            # Menu bar items hover
            f"""QMenuBar::item:selected {{
                    background-color: {menu_bar_item_hover_bg_color};
                    {menu_bar_item_hover_additional_qss}
            }}"""
            # Sub menu's dropdown
            f"""QMenu {{
                    border-radius: 0px;
                    padding: 0px;
                    font-family: {menu_bar_dropdown_font};
                    {menu_bar_dropdown_additional_qss}
            
            }}"""
            # Sub menu's dropdown's items
            f"""QMenu::item {{
                    padding: {menu_bar_dropdown_item_padding};
                    background-color: {menu_bar_dropdown_item_bg_color};
                    {menu_bar_dropdown_item_additional_qss}
            }}"""
            # Sub menu's dropdown's items hover
            f"""QMenu::item::selected {{
                    background-color: {menu_bar_dropdown_item_hover_bg_color};
                    {menu_bar_dropdown_item_hover_additional_qss}
            }}"""
        )

        self.setVisible(True)

    def add_menu_item(self, menu: QMenu):
        self.menu.addMenu(menu)

        # file_menu = QMenu("File", menu)
        # file_menu.addAction("Open")
        # file_menu.addAction("Save")
        # menu.addMenu(file_menu)

        # edit_menu = QMenu("Edit", menu)
        # edit_menu.addAction("Open")
        # edit_menu.addAction("Save")
        # menu.addMenu(edit_menu)


app = QApplication()
# root = MainWindow()
root = MainWindowWidget()
root.show()
app.exec()
