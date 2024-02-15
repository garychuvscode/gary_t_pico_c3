"""
hello.py

    Writes "Hello!" in random colors at random locations on the display.
"""

import random
import utime
import st7789
import tft_config

# import vga2_bold_16x32 as font
import vga2_8x8 as font

tft = tft_config.config(1)


def center(text):
    length = 1 if isinstance(text, int) else len(text)
    tft.text(
        font,
        str(text),
        tft.width() // 2 - length // 2 * font.WIDTH,
        tft.height() // 2 - font.HEIGHT // 2,
        st7789.WHITE,
        st7789.BLACK,
    )


def main():
    tft.init()
    tft.fill(st7789.color565(255, 255, 0))
    # tft.fill(st7789.GREEN)
    # center(b"\xAEHello\xAF")
    center(f"Cute Avon!")
    utime.sleep(2)
    # tft.fill(st7789.BLACK)

    # while True:
    #     for rotation in range(4):
    #         tft.rotation(rotation)
    #         tft.fill(0)
    #         col_max = tft.width() - font.WIDTH * 6
    #         row_max = tft.height() - font.HEIGHT

    #         for _ in range(128):
    #             tft.text(
    #                 font,
    #                 str(f"Garytest!"),
    #                 random.randint(0, col_max),
    #                 random.randint(0, row_max),
    #                 st7789.color565(
    #                     random.getrandbits(8),
    #                     random.getrandbits(8),
    #                     random.getrandbits(8),
    #                 ),
    #                 st7789.color565(
    #                     random.getrandbits(8),
    #                     random.getrandbits(8),
    #                     random.getrandbits(8),
    #                 ),
    #             )


def draw_text_wrap(
    font, text, text2, x0, y0, color=st7789.WHITE, background=st7789.BLACK
):
    """
    Draw text on display with automatic line wrapping and signature.
    Args:
        font (module): font module to use.
        text (str): text to write
        text2 (str): signature text
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
    # Initialize signature position
    signature_x = tft.width() - len(text2) * font.WIDTH
    signature_y = tft.height() - font.HEIGHT
    for word in words:
        word_width = len(word) * font.WIDTH
        if (
            current_x + word_width > max_width
        ):  # If exceeds the width, move to the next line
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
    # Draw signature
    tft.text(font, text2, signature_x, signature_y, st7789.GREEN, background)


main()

print(f"test another")
utime.sleep(3)

# Input text
input_text = "This is a long text that will wrap around automatically on the display!"
# Signature text
signature_text = "Gary"
# Call draw_text_wrap function with input text and signature text
draw_text_wrap(font, input_text, signature_text, 0, 0, st7789.WHITE, st7789.BLACK)
utime.sleep(2)
