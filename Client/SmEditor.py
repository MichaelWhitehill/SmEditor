import tkinter as tk
from threading import Thread
from tkinter import INSERT, END, SEL_FIRST, SEL_LAST

from Client.JsonController import JsonController, OP, GET_ALL_TEXT
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
        return str(self.line) + "." + str(self.pos)

    def __add__(self, other):
        line = self.line + other.line
        pos = self.pos + other.pos
        return Cursor(str(line)+"."+str(pos))

    def __sub__(self, other):
        line = self.line - other.line
        pos = self.pos - other.pos
        return Cursor(str(line)+"."+str(pos))

    def __lt__(self, other):
        if self.line < other.line:
            return True
        if self.pos < other.pos:
            return True
        return False


class SmEditor:

    def __init__(self):
        self.jsonCon = JsonController(self)
        self.root = tk.Tk()
        self.text = tk.Text(self.root)
        self.text.grid()
        self.text.pack(side="left")
        self.redirector = WidgetRedirector(self.text)
        self.original_mark = self.redirector.register("mark", self.on_mark)
        self.original_insert = self.redirector.register("insert", self.on_insert)
        self.original_delete = self.redirector.register("delete", self.on_delete)
        self.delta_index = Cursor("1.0")
        self.listen_thread = Thread(target=self.jsonCon.listen)
        self.listen_thread.start()
        self.root.protocol('WM_DELETE_WINDOW', self.shutdown)  # root is your root window
        self.ignore_actions = False
        get_text_dict = {OP: GET_ALL_TEXT}
        self.jsonCon.send_dict(get_text_dict)
        self.root.mainloop()

    def shutdown(self):
        print("Shutdown")
        self.jsonCon.send_message("QUIT")
        self.listen_thread.join(1)
        self.jsonCon.close()
        self.root.destroy()

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
        self.delta_index = Cursor(self.text.index(INSERT)) + Cursor("0.1")
        if not self.ignore_actions:
            self.jsonCon.propagate_insert(Cursor(self.text.index(INSERT)), event[1])
        return self.original_insert(*event)

    def on_delete(self, *event):
        # Backspace
        index_1 = None
        index_2 = None
        if event[0] == "insert-1c":
            print("delete the character behind the cursor")
            insert_cursor = Cursor(self.text.index(INSERT))
            index_1 = insert_cursor
            index_2 = insert_cursor - Cursor("0.1")
        elif event[0] == "insert":
            print("Delete the character before the cursor")
            insert_cursor = Cursor(self.text.index(INSERT))
            index_1 = insert_cursor
            index_2 = insert_cursor + Cursor("0.1")
        elif event[0] == SEL_FIRST:
            index_1 = Cursor(self.text.index(SEL_FIRST))
            index_2 = Cursor(self.text.index(SEL_LAST))
        if not self.ignore_actions:
            self.jsonCon.propagate_delete(index_1, index_2)
        return self.original_delete(*event)

    def net_insert(self, delta_index, delta):
        self.ignore_actions = True
        self.text.insert(str(delta_index), delta)
        self.ignore_actions = False
        return

    def net_delete(self, delta_start, delta_index2):
        if delta_start < delta_index2:
            start = delta_start
            end = delta_index2
        else:
            start = delta_index2
            end = delta_start

        # needs the greater index first
        self.ignore_actions = True
        self.text.delete(str(start), str(end))
        self.ignore_actions = False
        return None

    def update_text(self, text):
        self.ignore_actions = True
        self.text.delete("1.0", END)
        self.text.insert("1.0", text)
        self.ignore_actions = False

    def get_text(self):
        return self.text.get("1.0", END)


if __name__ == '__main__':
    app = SmEditor()
