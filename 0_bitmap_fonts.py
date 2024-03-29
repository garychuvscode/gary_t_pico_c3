"""
fonts.py

    Cycles through all characters of four bitmap fonts on the display

"""

# fmt: off
import utime
import st7789
import tft_config
import vga1_8x8 as font1
import vga1_8x16 as font2
import vga1_16x16 as font3
import vga1_16x32 as font4
import vga1_bold_16x16 as font5
import vga2_8x8 as font6
import vga2_8x16 as font7
import vga2_16x16 as font8
import vga2_16x32 as font9
import vga2_bold_16x16 as font10
import vga2_bold_16x32 as font11


tft = tft_config.config(0)


def main():
    tft.init()

    while True:
        for font in (
            font1,
            font2,
            font3,
            font4,
            font5,
            font6,
            font7,
            font8,
            font9,
            font10,
            font11,

        ):
            tft.fill(st7789.BLUE)
            line = 0
            col = 0
            for char in range(font.FIRST, font.LAST):
                tft.text(font, chr(char), col, line, st7789.WHITE, st7789.BLUE)
                col += font.WIDTH
                if col > tft.width() - font.WIDTH:
                    col = 0
                    line += font.HEIGHT

                    if line > tft.height() - font.HEIGHT:
                        utime.sleep(3)
                        tft.fill(st7789.BLUE)
                        line = 0
                        col = 0

            utime.sleep(3)


main()
