# CustomTitleBar
Implements a custom title bar which automatically replaces default title bar of a `QWidget` or `QMainWindow`. `CustomTitleBar` should be placed in the central widget of the root.

### Using CustomTitleBar in a QMainWindow
If the root is a `QMainWindow`, simply place `CustomTitleBar` as the first item in the `centralWidget`. The main content should be placed in a layout placed in a layout below the CustomTitleBar. So the structure will be:

- QMainWindow: 
  - centralWidget:
    - centralWidget layout:
      - CustomTitleBar widget
      - Content layout (add contents margins here):
        - App content

For example, see [`customtitlebar_example_qmainwindow.py`](examples/customtitlebar_example_qmainwindow.py) or see [below](#example-qmainwindow). 


### Using CustomTitleBar in a QWidget
If the root is a `QWidget`, place a layout, then a central widget in that layout, then place a vertical layout in the central widget, then place the the `CustomTitleBar`, then after that, place a layout which holds all of your app's other content (this is important because it will allow you to add back in contents margins that have to be removed from the higher level elements). For example, see `customtitlebar_example_qwidget.py`.

## Examples

### Example: QMainWindow
ergilh;klbjktrb
