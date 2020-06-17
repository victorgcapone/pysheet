from itertools import product as cartesian_product

class SheetView:

    def __init__(self, sheet):
        self.sheet = sheet
        self.offset_column = "A"
        self.offset_row = 1
        self.columns_to_show = 10
        self.rows_to_show = 10
        self.current_column = "A"
        self.current_row = 1

    def display(self):
        columns = [chr(c) for c in range(ord(self.offset_column), ord(self.offset_column) + self.columns_to_show)]
        print("\t" + "\t".join(columns))
        for row in range(self.offset_row, self.offset_row + self.rows_to_show):
            print(row, end='')
            for column in columns:
                print("{:>4}".format(self.sheet[column + str(row)]), end='')
            print("\n")

    def visible_rows(self):
        return range(self.offset_row, self.offset_row + self.rows_to_show)

    def visible_columns(self):
        return [chr(c) for c in range(ord(self.offset_column), ord(self.offset_column) + self.columns_to_show)]

    def get_visible_cells(self, index, row=True):
        result = []
        if row and index in self.visible_rows():
            result = cartesian_product(self.visible_columns(), [index])
        elif not row and index in self.visible_columns():
            result = cartesian_product([index], self.visible_rows())
        result = map(lambda t: t[0] + str(t[1]), result)
        return result

    def current_cell(self):
        return self.sheet[self.current_cell_coord()]

    def current_cell_coord(self):
        return "".join([self.current_column, str(self.current_row)])

    def get_row_as_text(self, row):
        result = "{:>3}".format(row)
        columns = [chr(c) for c in range(ord(self.offset_column), ord(self.offset_column) + self.columns_to_show)]
        for column in columns:
            if row == self.current_row and column == self.current_column:
                result += "<style bg=\"#555555\">{:>10}</style>".format(self.sheet[column + str(row)].value())
            else:
                result += "{:>10}".format(self.sheet[column + str(row)].value())
        return result

    def update_cell(self, cell, formula):
        must_update = self.sheet.__setitem__(cell, formula)

    def move_column_right(self):
        self.current_column = chr(ord(self.current_column) + 1)
        if ord(self.current_column) >= ord(self.offset_column)+self.columns_to_show:
            self.offset_column = chr(ord(self.offset_column) + 1)

    def move_column_left(self):
        if ord(self.current_column) == ord("A"):
            return
        self.current_column = chr(ord(self.current_column) - 1)
        if ord(self.current_column) < ord(self.offset_column):
            self.offset_column = chr(ord(self.offset_column) - 1)

    def move_row_up(self):
        if self.current_row == 1:
            return
        self.current_row -= 1
        if self.current_row < self.offset_row:
            self.offset_row = self.current_row

    def move_row_down(self):
        self.current_row += 1
        if self.current_row >= self.offset_row+self.rows_to_show:
            self.offset_row += 1

    def get_current_cell_formula(self):
        return self.current_cell().formula



