#include <gpiod.h>
#include <unistd.h>
#include <stdio.h>

#define CHIP_PATH "/dev/gpiochip11" 
#define LINE_NUM  9                 // AON GPIO 9 onboard ACT LED


#define UNIT       200000
#define DOT        (UNIT)
#define DASH       (3 * UNIT)
#define SYMBOL_GAP (UNIT)
#define LETTER_GAP (3 * UNIT - SYMBOL_GAP)  // blink() already adds one symbol gap


static void blink(struct gpiod_line *line, useconds_t on_time) {
    gpiod_line_set_value(line, 1);  // On libgpiod something
    usleep(on_time);
    gpiod_line_set_value(line, 0);  // Off
    usleep(SYMBOL_GAP);
}

int main(void) {
    // this stuff does something
    struct gpiod_chip *chip = gpiod_chip_open(CHIP_PATH); // find where the led is
    if (!chip) { perror("chip"); return 1; }

    struct gpiod_line *line = gpiod_chip_get_line(chip, LINE_NUM);
    if (!line) { perror("get_line"); return 1; }

    if (gpiod_line_request_output(line, "blink", 0) < 0) {
        perror("request_output");  // "Device busy": set the ACT trigger to none first
        return 1;
    }

    while(true) {
        for (int i = 0; i < 3; i++){ // s dot dot dot
            blink(line, DOT);
        }   
        usleep(LETTER_GAP);
        for (int i = 0; i < 3; i++){ // o dash dash dash
            blink(line, DASH);
        }   
        usleep(LETTER_GAP);
        for (int i = 0; i < 3; i++){
            blink(line, DOT);
        }   
        usleep(4*UNIT);
    }
}
