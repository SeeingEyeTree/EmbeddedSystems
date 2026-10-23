#include <gpiod.h>
#include <unistd.h>
#include <stdio.h>

#define CHIP_PATH "/dev/gpiochip0"  // check the chip with `gpioinfo`
#define LINE_NUM  9                 // AON GPIO 9 = onboard ACT LED

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
        gpiod_line_set_value(line, 1);  // On (libgpiod handles active-low)
        usleep(500000);
        gpiod_line_set_value(line, 0);  // Off
        usleep(500000);
    }
}
