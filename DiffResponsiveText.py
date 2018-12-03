
class DiffResponsiveText:
    def __init__(self):
        self.text = [str()]

    def insert(self, delta_index, delta):
        print(str(delta_index))
        line_to_change = self.text[delta_index[0]-1]
        new_line_str = line_to_change[:delta_index[1]] + str(delta) + line_to_change[delta_index[1]:]
        self.text[delta_index[0] - 1] = new_line_str
        return

    def delete(self, delta_start, delta_index2):
        # TODO
        return None

    def get_text(self):
        return self.text

    def __str__(self):
        ret = ""
        for line in self.text:
            ret += line + "\n"
        return ret
