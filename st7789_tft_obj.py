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
        self.status_count = 0
        self.last_status = ""

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
        signature_y = self.tft.height() - self.font.HEIGHT * 2  # Adjusted for two lines
        # Only clear the area occupied by the signature text
        self.tft.fill_rect(
            signature_x,
            signature_y,
            signature_width,
            self.font.HEIGHT * 2,
            background
        )
        self.tft.text(font, signature, signature_x, signature_y, color, background)

    def tft_status(
    self, font=font, status0="loading", color=st7789.GREEN, background=st7789.BLACK
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
        if status0 != 'loading': 
            self.last_status = status0

        # Calculate position for status text
        status_width = len(status0) * font.WIDTH
        max_height = (
            self.tft.height() - self.font.HEIGHT
        )  # Maximum height of text within display
        status_x = 0  # Adjusted to the left edge of the screen
        status_y = max_height - self.font.HEIGHT  # Adjusted for one line from the bottom

        # Clear the status area
        self.tft.fill_rect(
            0, status_y, self.tft.width() // 2, self.font.HEIGHT, background
        )

        # Display status text
        # Append additional dots based on status count
        dots = "." * (self.status_count % 3 + 1)
        if self.last_status != '': 
            status_text = f"{self.last_status}{dots}"
            self.tft.text(font, status_text, status_x, status_y, color, background)
        else: 
            status_text = f"{status0}{dots}"
            self.tft.text(font, status_text, status_x, status_y, color, background)
        # Increment status count if status text has changed
        if status0 != self.last_status and status0 != 'loading':
            self.status_count = 0
            self.last_status = status0
        else:
            self.status_count += 1

        # Reset status count when it reaches the threshold
        if self.status_count > 3:
            self.status_count = 0




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
    utime.sleep(2)
    tft_test.tft_terminal_in(
        text="grace like to gi sai mean but just forgive that, she is always like this ")
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Grace")
    utime.sleep(0.5)
    tft_test.tft_terminal_in(text="Frank")
    tft_test.tft_signature()
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
    tft_test.tft_status(status0='hi grace')
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


