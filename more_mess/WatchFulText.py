from tkinter import Text, INSERT

from DiffResponsiveText import DiffResponsiveText
from more_mess.ModifiedMixin import ModifiedMixin

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


class WText(ModifiedMixin, Text):
    def __init__(self, *a, **b):
        # Create self as a Text.
        Text.__init__(self, *a, **b)
        # Initialize the ModifiedMixin.
        self._init()
        self.modified_skip = False
        self.delta_index = "1.0"
        self.d_file = DiffResponsiveText()
        self.bind("<<TextModified>>", self.t_modified)


    def been_modified(self, event=None):
        '''
        Override this method do do work when the Text is modified.
        '''
        return

    def callback(self, result, *args):
        '''Updates the label with the current cursor position'''
        # print("insert changed indexes")
        # delta, delta_start, d_size,  = self.compute_current_delta()
        # print("Delta: " + delta)
        # print("delta_start: " + str(delta_start))
        # print("d_size: " + str(d_size))
        # if d_size[0] >= 0 and d_size[1] >= 0:
        #     self.mod_inserted(delta, delta_start)
        # # print("Insert: " + str(delta_start) + " Delta length: " + str(d_size))
        # # print("Delta: " + str(delta))
        print("Callback")
        return

    def t_modified(self, event):
        print("Modified")

    def compute_current_delta(self):
        c_delta = Cursor(self.delta_index)
        c_insert = Cursor(self.index(INSERT))
        text = self.get(self.delta_index, INSERT)
        self.delta_index = self.index(INSERT)
        return text, c_delta, (c_insert - c_delta)

    def modified(self, event=None):
        # print("modified")
        delta, delta_start, d_size,  = self.compute_current_delta()
        if d_size[0] >= 0 and d_size[1] >= 0:
            self.mod_inserted(delta, delta_start)
        # print("Insert: " + str(delta_start) + " Delta length: " + str(d_size))
        # print("Delta: " + str(delta))

    def mod_inserted(self, delta, delta_start):
        self.d_file.insert(delta_start, delta)
        print(str(self.d_file))

    def mod_deleted(self, delta_start, d_direction):
        start_index = delta_start
        end_index = delta_start-d_direction


