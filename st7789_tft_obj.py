import random
import utime
import st7789
import tft_config

# import vga2_bold_16x32 as font
import vga2_8x8 as font

tft = tft_config.config(1)


class st7789_tft:
    def __init__(self, font0=font):
        self.str_history = []
        self.tft = tft_config.config(1)
        self.tft.init()
        self.font = font0
        self.x0 = 0
        self.y0 = 0
        self.terminal_count = 0

    def tft_terminal_in(
    self, font=font, text="", color=st7789.WHITE, background=st7789.BLACK
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
            lines_to_remove = (self.terminal_count * self.font.HEIGHT - max_height) // self.font.HEIGHT + 1
            # Remove the lines and update the terminal count
            for _ in range(lines_to_remove):
                removed_line_length = len(self.str_history.pop(0))
                self.terminal_count -= (removed_line_length * self.font.WIDTH) // max_width + 1

        # Clear the screen except for the signature area
        signature_height = self.font.HEIGHT * 2  # Height of the signature area
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
                self.tft.text(font, char, current_x, current_y, color, background)
                current_x += char_width
            current_x = self.x0
            current_y += self.font.HEIGHT


    def tft_signature(
        self, font=font, signature="gary", color=st7789.GREEN, background=st7789.BLACK
    ):
        """
        Display signature text aligned to the right.
        Args:
            font (module): font module to use.
            signature (str): signature text to write.
            color (int): 565 encoded color to use for characters.
            background (int): 565 encoded color to use for background.
        """
        signature_width = len(signature) * font.WIDTH
        signature_x = self.tft.width() - signature_width
        signature_y = self.tft.height() - font.HEIGHT * 2  # Adjusted for two lines
        self.tft.fill_rect(
            0, signature_y, self.tft.width(), font.HEIGHT * 2, background
        )  # Clear only the signature area
        self.tft.text(font, signature, signature_x, signature_y, color, background)

    



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
    # tft_test.tft_status()
    tft_test.tft_terminal_in(
        text="See you tomorrow, this is the long testing string for auto change to next line"
    )
    utime.sleep(0.5)
    tft_test.tft_terminal_in(
        text="grace like to gi sai mean but just forgive that, she is always like this ")
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
