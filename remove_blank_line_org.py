import sys
import re

"""
Usage; python remvoe_blank_line_org.py input_file output_file
"""

class BlankLineRemover:
    def __init__(self):
        self.blank_line_re = re.compile(r"\s*$")
        self.list_line_re = re.compile(r"\s*(\-|[\d]+\.).*")
        self.section_line_re = re.compile(r"\s*(\*).*")

    def get_line_type(self, line, current_line_type):
        found_list = self.list_line_re.match(line)
        found_blank = self.blank_line_re.match(line)
        found_section = self.section_line_re.match(line)
        if found_list:
            return "list"
        if found_blank:
            return "blank"
        if found_section:
            return "section"
        else:
            return "list" if current_line_type == "list" else "regular"


    def remove_blank_line(self, infile, output_file):
        """
        Remove a blank line only if both the lines that in front and after it are
        list lines.
        If either of the two line are 'section' lines. The blank line is removed.
        """

        blank_line_buffer = []
        current_line_type ="blank"
        last_is_list = False
        last_is_section = False
        for line in infile:
            current_line_type = self.get_line_type(line, current_line_type)
            if current_line_type == "list" or current_line_type == "section":
                if len(blank_line_buffer) > 0: blank_line_buffer = []
                last_is_list = current_line_type == "list"
                last_is_section = current_line_type == "section"
                output_file.write(line)
                continue
            if current_line_type == "regular":
                last_is_list = False
                last_is_section = False
                for b_line in blank_line_buffer:
                    output_file.write(b_line)
                blank_line_buffer = []
                output_file.write(line)
                continue
            if current_line_type == "blank":
                if last_is_section:
                    continue
                if last_is_list:
                    blank_line_buffer.append(line)
                else:
                    output_file.write(line)

if __name__ == '__main__':
    remover = BlankLineRemover()
    remover.remove_blank_line(open(sys.argv[1]),
                              open(sys.argv[2], "w"))
