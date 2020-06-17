from prompt_toolkit import Application
from prompt_toolkit.application import get_app
from prompt_toolkit.filters import Condition
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, ConditionalContainer
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import HorizontalLine, Dialog, TextArea
from itertools import product as cartesian_product

from PysheetApplication import PysheetApplication

input_mode = False


def get_row_as_text(row):
    def get_row():
        return HTML(controller.view.get_row_as_text(row))
    return get_row


def get_column_name(column):
    def _():
        return column
    return _


def enter_input_mode(event):
    global input_mode
    input_mode = not input_mode
    if input_mode:
        cell_input_dialog.body.text = controller.view.get_current_cell_formula()
    get_app().invalidate()


def commit_changes(buffer):
    controller.input_mode = False
    controller.view.update_cell(controller.view.current_cell_coord(), buffer.text)
    get_app().invalidate()


def get_cell(cell):
    def _():
        return HTML(controller.get_cell_html(cell))
    return _


cell_input_dialog = Dialog(TextArea(accept_handler=commit_changes, multiline=False))
controller = PysheetApplication(cell_input_dialog)

grid_container = HSplit([
    # Header for the columns name
    VSplit([
        Window(FormattedTextControl(), width=10),
        *[Window(FormattedTextControl(get_column_name(column)), width=10) for column in controller.view.visible_columns()]
    ], height=1),
    # Display each row
    HSplit([
            VSplit([
                Window(FormattedTextControl(HTML(str(row))), width=2),
                *[
                    Window(FormattedTextControl(get_cell(cell)), width=10)
                    for cell in controller.view.get_visible_cells(row, row=True)
                ]
            ]) for row in controller.view.visible_rows()
    ], height=controller.view.rows_to_show),
    HorizontalLine(),
    Window(
        content=FormattedTextControl(controller.view.get_current_cell_formula),
        height=1
    ),
    ConditionalContainer(content=cell_input_dialog, filter=Condition(lambda: controller.input_mode))
])

root_container = HSplit([
    # Header for the columns name
    VSplit([
        Window(FormattedTextControl(), width=10),
        *[Window(FormattedTextControl(get_column_name(column)), width=10) for column in controller.view.visible_columns()]
    ], height=1),
    # Display each row
    HSplit([
        # For each cell in the row, display it's content
            VSplit([
                Window(FormattedTextControl(get_row_as_text(row)))
            ]) for row in controller.view.visible_rows()
    ], height=controller.view.rows_to_show),
    HorizontalLine(),
    Window(
        content=FormattedTextControl(controller.view.get_current_cell_formula),
        height=1
    ),
    ConditionalContainer(content=cell_input_dialog, filter=Condition(lambda: controller.input_mode))
])

layout = Layout(grid_container)
#layout = Layout(root_container)

app = Application(layout=layout, key_bindings=controller.bindings(), full_screen=True)
app.run() # You won't be able to Exit this app