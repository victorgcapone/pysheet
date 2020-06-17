from Cell import Cell
import re


class Sheet:

    def __init__(self):
        self.cells = {}
        self.observers = {}
        self.observers_regex = re.compile("[a-zA-z]+\d+")

    def __getitem__(self, key):
        key = key.lower()
        cell = self.cells.get(key, Cell(self))
        return cell

    def __setitem__(self, key, item):
        key = key.lower()
        cell = self.cells.get(key, Cell(self))
        cell.formula = item
        # Finds all cell names in the formula
        observed = self.observers_regex.findall(cell.formula)
        for o in observed:
            observers_list = self.observers.get(o, [])
            observers_list.append(key)
            self.observers[o] = observers_list
        self.cells[key] = cell
        return self.observers.get(key, [])
