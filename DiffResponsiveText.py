import tkinter as tk


class DiffResponsiveText:
    def __init__(self, root):
        self.text = tk.Text(root)
        self.text.pack(side="right")

    def insert(self, delta_index, delta):
        self.text.insert(str(delta_index), delta)
        return

    def delete(self, delta_start, delta_index2):
        start = None
        end = None
        if delta_start < delta_index2:
            start = delta_start
            end = delta_index2
        else:
            start = delta_index2
            end = delta_start

        # needs the greater index first
        self.text.delete(str(start), str(end))
        return None

    def get_text(self):
        return self.text
