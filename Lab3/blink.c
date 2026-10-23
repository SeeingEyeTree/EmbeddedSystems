#include <gpiod.h>
#include <unistd.h>
#include <stdio.h>

#define CHIP_PATH "/dev/gpiochip11" // check the chip with `gpioinfo`
#define LINE_NUM  9                 // AON GPIO 9 = onboard ACT LED

// Morse timing (microseconds): dash = 3 dots, gap between symbols = 1 dot,
// between letters = 3 dots, between words = 7 dots.
#define UNIT       200000
#define DOT        (UNIT)
#define DASH       (3 * UNIT)
#define SYMBOL_GAP (UNIT)
#define LETTER_GAP (3 * UNIT - SYMBOL_GAP)  // blink() already adds one symbol gap
#define WORD_GAP   (7 * UNIT - SYMBOL_GAP)

static void blink(struct gpiod_line *line, useconds_t on_time) {
    gpiod_line_set_value(line, 1);  // On (libgpiod handles active-low)
    usleep(on_time);
    gpiod_line_set_value(line, 0);  // Off
    usleep(SYMBOL_GAP);
}

int main(void) {
    struct gpiod_chip *chip = gpiod_chip_open(CHIP_PATH);
    if (!chip) { perror("chip"); return 1; }

    struct gpiod_line *line = gpiod_chip_get_line(chip, LINE_NUM);
    if (!line) { perror("get_line"); return 1; }

    if (gpiod_line_request_output(line, "blink", 0) < 0) {
        perror("request_output");  // "Device busy": set the ACT trigger to none first
        return 1;
    }

    for (;;) {
        for (int i = 0; i < 3; i++) blink(line, DOT);   // S
        usleep(LETTER_GAP);
        for (int i = 0; i < 3; i++) blink(line, DASH);  // O
        usleep(LETTER_GAP);
        for (int i = 0; i < 3; i++) blink(line, DOT);   // S
        usleep(WORD_GAP);
    }
}
