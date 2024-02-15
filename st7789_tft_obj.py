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
        self.font = font0
        self.x0 = 0
        self.y0 = 0

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
        max_height = (
            self.tft.height() - self.font.HEIGHT
        )  # Maximum height of text within display
        current_x = self.x0
        current_y = self.y0

        # Clear screen
        self.tft.fill(background)

        # Add new text to history
        self.str_history.append(text)
        # Remove excessive history if needed
        while len("".join(self.str_history)) * self.font.WIDTH > max_width:
            self.str_history.pop(0)

        # Display text
        for line in self.str_history:
            for char in line:
                char_width = self.font.WIDTH
                if (
                    current_x + char_width > max_width
                ):  # If exceeds the width, move to the next line
                    current_x = self.x0
                    current_y += self.font.HEIGHT
                if (
                    current_y + self.font.HEIGHT > max_height
                ):  # If exceeds the height, stop drawing
                    break
                self.tft.text(font, char, current_x, current_y, color, background)
                current_x += char_width
            current_x = self.x0
            current_y += self.font.HEIGHT

        # Update x0 and y0 for next call
        self.x0 = current_x
        self.y0 = current_y

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
        signature_y = self.tft.height() - font.HEIGHT
        self.tft.fill_rect(0, signature_y, self.tft.width(), font.HEIGHT, background)
        self.tft.text(font, signature, signature_x, signature_y, color, background)


if __name__ == "__main__":
    # testing code TFT

    tft_test = st7789_tft()

    # tft_test.tft_terminal_in(text="Hello, World!")
    # tft_test.tft_terminal_in(text="ABC")
    tft_test.tft_signature()
