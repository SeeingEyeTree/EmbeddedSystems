#include <gpiod.h>
#include <unistd.h>
#include <stdio.h>

int main(void) {
    struct gpiod_chip *chip = gpiod_chip_open("/dev/gpiochip0");
    if (!chip) { perror("chip"); return 1; }

    struct gpiod_line_settings *s = gpiod_line_settings_new();
    gpiod_line_settings_set_direction(s, GPIOD_LINE_DIRECTION_OUTPUT);
    struct gpiod_line_config *lc = gpiod_line_config_new();
    unsigned int off = 9;
    gpiod_line_config_add_line_settings(lc, &off, 1, s);
    struct gpiod_request_config *rc = gpiod_request_config_new();
    gpiod_request_config_set_consumer(rc, "blink");

    struct gpiod_line_request *req = gpiod_chip_request_lines(chip, rc, lc);
    if (!req) { perror("request"); return 1; }

    for (;;) {
        gpiod_line_request_set_value(req, 9, GPIOD_LINE_VALUE_ACTIVE);
        usleep(500000);
        gpiod_line_request_set_value(req, 9, GPIOD_LINE_VALUE_INACTIVE);
        usleep(500000);
    }
}
