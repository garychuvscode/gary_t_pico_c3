

import random
import utime
import st7789
import tft_config

# import vga2_bold_16x32 as font
import vga2_8x8 as font

tft = tft_config.config(1)
tft.init()


class st7789_tft:
    @staticmethod
    def tft_terminal_in(font=font, text='', x0=0, y0=0, color=st7789.WHITE, background=st7789.BLACK):
        """
        Display input text on the terminal with automatic line wrapping.
        Args:
            font (module): font module to use.
            text (str): text to write
            x0 (int): starting x coordinate
            y0 (int): starting y coordinate
            color (int): 565 encoded color to use for characters
            background (int): 565 encoded color to use for background
        """
        max_width = tft.width() - x0  # Maximum width of text within display
        max_height = tft.height() - y0  # Maximum height of text within display
        current_x = x0
        current_y = y0
        # Split text into words
        words = text.split()
        for word in words:
            word_width = len(word) * font.WIDTH
            if current_x + word_width > max_width:  # If exceeds the width, move to the next line
                current_x = x0
                current_y += font.HEIGHT
            if current_y + font.HEIGHT > max_height:  # If exceeds the height, stop drawing
                break
            # Draw word
            tft.text(font, word, current_x, current_y, color, background)
            current_x += word_width + font.WIDTH  # Add space between words
        # Fill remaining space with background color
        tft.fill_rect(
            0,
            current_y + font.HEIGHT,
            tft.width(),
            tft.height() - (current_y + font.HEIGHT),
            background,
        )

    @staticmethod
    def tft_signature(font=font, text='Gary', x0=0, y0=0, color=st7789.WHITE, background=st7789.BLACK):
        """
        Display signature text on the terminal.
        Args:
            font (module): font module to use.
            text (str): signature text
            x0 (int): starting x coordinate
            y0 (int): starting y coordinate
            color (int): 565 encoded color to use for characters
            background (int): 565 encoded color to use for background
        """
        signature_x = tft.width() - len(text) * font.WIDTH
        signature_y = tft.height() - font.HEIGHT
        tft.text(font, text, signature_x, signature_y, st7789.GREEN, background)


tft.fill(st7789.BLUE)
utime.sleep(2)
st7789_tft.tft_terminal_in(text='hihi Avon')
utime.sleep(2)
st7789_tft.tft_signature()