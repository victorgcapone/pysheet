import re


class Cell:

    def __init__(self, sheet):
        self.formula = ""
        self.sheet = sheet

    def __str__(self):
        return self.formula

    def value(self):
        if len(self.formula) == 0:
            return ""
        if self.formula[0] is not '=':
            return self.formula
        return self.parse_formula()

    def parse_formula(self):
        dependencies = self.sheet.observers_regex.findall(self.formula)
        dependencies_values = map(lambda cell: str(self.sheet[cell]), dependencies)
        final_formula = self.formula[1:]
        value = ""
        for cell, value in zip(dependencies, dependencies_values):
            final_formula = re.sub(cell, value, final_formula, count=1)
        try:
            value = eval(final_formula)
        except Exception as e:
            value = "!ERROR!"
        return value