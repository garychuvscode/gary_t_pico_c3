import utime
import st7789
import tft_config

# import all the different font for selection
"""
vga1 have less element, vga2 have more element
bold is more thick than original
"""
import vga1_8x8 as font1
import vga1_8x16 as font2
import vga1_16x16 as font3
import vga1_16x32 as font4
import vga1_bold_16x16 as font5

# import vga2_8x8 as font6
# import vga2_8x16 as font7
# import vga2_16x16 as font8
# import vga2_16x32 as font9
# import vga2_bold_16x16 as font10
# import vga2_bold_16x32 as font11

# fmt: off

class st7789_tft:
    def __init__(self, font0=0, rotation0=1):
        '''
        define a new TFT control object, choose the font and direction settings
        font0: 0-3 -> small to big, 4 -> thick and big
        '''
        self.font_lib = [font1, font2, font3, font4, font5]
        self.str_history = []
        # tft config will create the and ST7789 object for
        # other control, use selftft."function name"
        # function refer to ST7789.pyi
        self.tft = tft_config.config(rotation=rotation0)
        '''
        direction of display can be select from rotation
        rotation (int): display rotation
                    - 0-Portrait
                    - 1-Landscape
                    - 2-Inverted Portrait
                    - 3-Inverted Landscape
        '''
        # default turn the back light on, use tft.off() to turn off
        # and become all black
        self.tft.init()
        self.font = self.font_lib[font0]
        self.x0 = 0
        self.y0 = 0
        self.terminal_count = 0
        self.status_count = 0
        self.last_status = ""

    def tft_terminal_in(
        self, text="", color=st7789.WHITE, background=st7789.BLACK
    ):
        """
        Display input text with automatic line wrapping like terminal.
        Args:
            font (module): font module to use.
            text (str): text to write.
            color (int): 565 encoded color to use for characters.
            background (int): 565 encoded color to use for background.
        """

        max_width = self.tft.width()  # Maximum width of text within display
        max_height = self.tft.height() - self.font.HEIGHT  # Maximum height for text

        # Add new text to history
        words = text.split()
        current_line = ""
        for word in words:
            word_width = len(word) * self.font.WIDTH
            if len(current_line) == 0:
                current_line = word
            elif len(current_line) + len(word) + 1 <= max_width // self.font.WIDTH:
                current_line += " " + word
            else:
                # If adding the word exceeds the width, start a new line
                self.str_history.append(current_line)
                current_line = word

        if current_line:
            self.str_history.append(current_line)

        # Remove excessive history if needed
        while self.terminal_count * self.font.HEIGHT > max_height:
            # Calculate the number of lines to remove
            lines_to_remove = (
                self.terminal_count * self.font.HEIGHT - max_height
            ) // self.font.HEIGHT + 1
            # Remove the lines and update the terminal count
            for _ in range(lines_to_remove):
                removed_line_length = len(self.str_history.pop(0))
                self.terminal_count -= (
                    removed_line_length * self.font.WIDTH
                ) // max_width + 1

        # Clear the screen except for the signature area
        signature_height = self.font.HEIGHT  # Height of the signature area
        self.tft.fill_rect(
            0, 0, self.tft.width(), self.tft.height() - signature_height, background
        )

        # Display text
        current_x = self.x0
        current_y = self.y0
        for line in self.str_history[-(max_height // self.font.HEIGHT) :]:
            for char in line:
                char_width = self.font.WIDTH
                if current_x + char_width > max_width:  # If exceeds the width
                    current_x = self.x0
                    current_y += self.font.HEIGHT
                if current_y + self.font.HEIGHT > max_height:  # If exceeds the height
                    break
                self.tft.text(self.font, char, current_x, current_y, color, background)
                current_x += char_width
            current_x = self.x0
            current_y += self.font.HEIGHT

    def tft_signature(
        self, signature="gary", color=st7789.GREEN, background=st7789.BLACK
    ):
        """
        Display signature text aligned to the right.
        Args:
            font (module): font module to use.
            signature (str): signature text to write.
            color (int): 565 encoded color to use for characters.
            background (int): 565 encoded color to use for background.
        """
        max_width = self.tft.width() // 2  # Limit signature to half of the screen width
        signature_width = min(len(signature) * self.font.WIDTH, max_width)
        signature_x = self.tft.width() - signature_width
        signature_y = self.tft.height() - self.font.HEIGHT
        self.tft.fill_rect(
            self.tft.width() // 2,
            signature_y,
            self.tft.width() // 2,
            self.font.HEIGHT * 2,
            background,
        )  # Clear only the signature area
        self.tft.text(self.font, signature, signature_x, signature_y, color, background)

    def tft_status(
        self, status0="loading", color=st7789.GREEN, background=st7789.BLACK
    ):
        """
        Display status text in the bottom left corner of the screen.
        Args:
            font (module): font module to use.
            status0 (str): status text to write.
            color (int): 565 encoded color to use for characters.
            background (int): 565 encoded color to use for background.
        """
        # update last status
        if status0 != "loading":
            self.last_status = status0

        # Calculate position for status text
        status_width = len(status0) * self.font.WIDTH
        max_width = (
            self.tft.width() // 2
        )  # Limit status text to half of the screen width
        status_width = min(status_width, max_width)
        # max_height = (
        #     self.tft.height() - self.font.HEIGHT
        # )  # Maximum height of text within display
        status_x = 0  # Adjusted to the left edge of the screen
        # status_y = (
        #     max_height - self.font.HEIGHT
        # )  # Adjusted for one line from the bottom
        status_y = (self.tft.height() - self.font.HEIGHT)

        # Clear the status area
        self.tft.fill_rect(
            0, status_y, self.tft.width() // 2, self.font.HEIGHT, background
        )

        # Display status text
        # Append additional dots based on status count
        dots = "." * (self.status_count % 4)
        if self.last_status != "":
            status_text = f"{self.last_status}{dots}"
            status_text = status_text[: min(len(status_text), max_width // self.font.WIDTH)]
            self.tft.text(self.font, status_text, status_x, status_y, color, background)
        else:
            status_text = f"{status0}{dots}"
            status_text = status_text[: min(len(status_text), max_width // self.font.WIDTH)]
            self.tft.text(self.font, status_text, status_x, status_y, color, background)

        # Increment status count if status text has changed
        if status0 != self.last_status and status0 != "loading":
            self.status_count = 0
            self.last_status = status0
        else:
            self.status_count += 1

        # Reset status count when it reaches the threshold
        if self.status_count >= 4:
            self.status_count = 0
    def tft_off(self):
        '''
        turn off tft
        '''
        self.tft.off()

    def tft_on(self):
        '''
        turn off tft
        '''
        self.tft.on()

    def tft_universal(self):
        '''
        input the code for directly control object
        '''
        self.str_to_code(string0=input('input the command to TFT: '))

    def dedent(self, code):
        lines = code.split('\n')
        # 计算最小缩进
        min_indent = float('inf')
        for line in lines:
            stripped = line.lstrip()
            if stripped:
                indent = len(line) - len(stripped)
                min_indent = min(min_indent, indent)

        # 移除最小缩进
        dedented_lines = [line[min_indent:] for line in lines]
        dedented_code = '\n'.join(dedented_lines)
        return dedented_code

    def str_to_code(self, string0="", *args, **kwargs ):
        '''
        function run for string command, also include the adjustment of 'TAB'
        to prevent error for the operation
        need to reference the function in st7789,pyi
        '''
        # # 231114, this is just testing string for the debugging
        # string0 = '''self.print_debug(content=f'Grace went back home now', always_print0=1)'''

        # 231114: add the reference dictionary to the exec function
        self.str_code_ref = {'self': self}
        # merge the self object with kwargs for cute Grace
        self.str_code_ref.update(kwargs)

        try:
            # string0 = str(string0)
            # textwrap => can't be used, give up and just for record
            # string0 = textwrap.dedent(string0)

            # there seems to have error
            string0 = self.dedent(string0)
            # 240131 if need the return result of string, use "eval" to replace "exec"
            exec(string0, globals(), self.str_code_ref)

        except Exception as e:
            # here use direct print since there may not be error during operation
            print(f'there are error on the TFT_OBJ: {e}')
        pass



if __name__ == "__main__":
    # Testing TFT code

    tft_test = st7789_tft()

    tft_test.tft_terminal_in(text="Hello, World!")
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Gary")
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Robert")
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Jimmy")
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Conant")
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Lisa")
    tft_test.tft_signature()
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Grace")
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Frank")
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Roy")
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Hihi Avon")
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Cute Cute Avon")
    utime.sleep(0.5)
    tft_test.tft_status()
    tft_test.tft_terminal_in(
        text="See you tomorrow, this is the long testing string for auto change to next line"
    )
    utime.sleep(0.5)
    tft_test.tft_terminal_in(
        text="grace like to gi sai mean but just forgive that, she is always like this "
    )
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Grace")
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Frank")
    tft_test.tft_signature(signature="FrankFrankFrankFrankFrankFrankFrank")
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Roy")
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Hihi Avon")
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Cute Cute Avon")
    tft_test.tft_status()
    utime.sleep(0.5)
    tft_test.tft_status()
    utime.sleep(0.5)
    tft_test.tft_status()
    utime.sleep(0.5)
    tft_test.tft_status(status0="hi grace")
    utime.sleep(0.5)
    tft_test.tft_status()
    utime.sleep(0.5)
    tft_test.tft_status()
    utime.sleep(0.5)
    tft_test.tft_status()
    utime.sleep(0.5)
    tft_test.tft_status()
    utime.sleep(0.5)
    tft_test.tft_status()
    utime.sleep(0.5)
    tft_test.tft_status()
    utime.sleep(0.5)
    tft_test.tft_status()
    utime.sleep(0.5)
    tft_test.tft_status(status0="hi gracehi gracehi gracehi gracehi gracehi grace")
    utime.sleep(0.5)
    tft_test.tft_status()
    utime.sleep(0.5)

    tft_test.tft_universal()
