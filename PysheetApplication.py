from Sheet import Sheet
from SheetView import SheetView
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app


class PysheetApplication:

    def __init__(self, formula_text_dialog):
        self.sheet = Sheet()
        self.view = SheetView(self.sheet)
        self.input_mode = False
        self.config = {} #Load from file
        self.key_bindings = None
        self.key_bindings = self.bindings()
        self.formula_text_dialog = formula_text_dialog

    def __getitem__(self, item):
        return self.config.get(item, None)

    def bindings(self):
        if self.key_bindings is None:
            self.key_bindings = KeyBindings()
            self.key_bindings.add("h", filter=not self.input_mode)(self.move_left_cell)
            self.key_bindings.add("k", filter=not self.input_mode)(self.move_right_cell)
            self.key_bindings.add("j", filter=not self.input_mode)(self.move_down_cell)
            self.key_bindings.add("u", filter=not self.input_mode)(self.move_up_cell)
            self.key_bindings.add("i", filter=not self.input_mode)(self.enter_input_mode)
        return self.key_bindings

    def move_right_cell(self, event):
        self.view.move_column_right()
        get_app().invalidate()

    def move_left_cell(self, event):
        self.view.move_column_left()
        get_app().invalidate()

    def move_up_cell(self, event):
        self.view.move_row_up()
        get_app().invalidate()

    def move_down_cell(self, event):
        self.view.move_row_down()
        get_app().invalidate()

    def enter_input_mode(self, event):
        self.input_mode = True
        self.formula_text_dialog.body.text = self.view.get_current_cell_formula()
        self.formula_text_dialog.title = self.view.current_cell_coord()
        get_app().invalidate()

    def get_cell_html(self, cell):
        fmt = "{:>10}"
        if cell == self.view.current_cell_coord():
            fmt = '<style bg="#555555">{:>10}</style>'
        return fmt.format(self.sheet[cell].value())
