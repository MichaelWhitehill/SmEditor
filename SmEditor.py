import tkinter as tk
from tkinter import INSERT, END, SEL_FIRST, SEL_LAST

from DiffResponsiveText import DiffResponsiveText
from WidgetRedirector import WidgetRedirector


class Cursor:
    def __init__(self, loc_string):
        loc_list = loc_string.split(".")
        self.line = int(loc_list[0])
        self.pos = int(loc_list[1])

    def __getitem__(self, item):
        return self.get_tuple()[item]

    def get_tuple(self):
        return self.line, self.pos

    def __str__(self):
        return str((self.line, self.pos))

    def __add__(self, other):
        return (self.line + other.line), (self.pos + other.pos)

    def __sub__(self, other):
        return (self.line - other.line), (self.pos - other.pos)


class SmEditor:

    def __init__(self):
        self.d_text = DiffResponsiveText()
        self.root = tk.Tk()
        self.text = tk.Text(self.root)
        self.text.grid()
        self.redirector = WidgetRedirector(self.text)
        self.original_mark = self.redirector.register("mark", self.on_mark)
        self.original_insert = self.redirector.register("insert", self.on_insert)
        self.original_delete = self.redirector.register("delete", self.on_delete)
        self.delta_index = Cursor("1.0")
        self.root.mainloop()

    def compute_current_delta(self):
        c_delta = Cursor(self.delta_index)
        c_insert = Cursor(self.text.index(INSERT))
        text = self.text.get(self.delta_index, INSERT)
        self.delta_index = self.text.index(INSERT)
        return text, c_delta, (c_insert - c_delta)

    def on_mark(self, *event):
        # print("mark", event)
        # the mark/cursor position was updated. We want to update our current cursor tracker and the delta cursor
        self.delta_index = Cursor(self.text.index(INSERT))
        return self.original_mark(*event)

    def on_insert(self, *event):
        # print("insert", event)
        self.d_text.insert(Cursor(self.text.index(INSERT)), event[1])
        print(str(self.d_text))
        self.delta_index = Cursor(self.text.index(INSERT)) + Cursor("0.1")
        return self.original_insert(*event)

    def on_delete(self, *event):
        # There are 3 types of delete we must handle
            # backspace
            # Delete
            # Highlight and delete
        print(str(event))
        # Backspace
        if event[0] is "insert-1c":
            print("delete the character behind the cursor")
        elif event[0] is "insert":
            print("Delete the character before the cursor")
        elif event[0] == SEL_FIRST:
            fi = self.text.index(SEL_FIRST)
            li = self.text.index(SEL_LAST)
            print(str(self.text.index(SEL_FIRST)) + "," + str(self.text.index(SEL_LAST)))
        return self.original_delete(*event)


if __name__ == '__main__':
    app = SmEditor()