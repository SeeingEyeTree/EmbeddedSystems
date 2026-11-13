#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>

#define PIN 9                  // RP1 GPIO9 = physical header pin 21

// Offsets inside the /dev/gpiomem0 mapping (RP1 datasheet, Table 2)
#define MAP_SIZE   0x30000
#define IO_BANK0   0x00000 // 0x400d0000
#define SYS_RIO0   0x10000 // 0x400e0000
#define PADS_BANK0 0x20000 // 0x400f0000

#define RIO_OUT    0x0
#define RIO_OE     0x4
#define ALIAS_SET  0x2000 // atomic bitmask set on write
#define ALIAS_CLR  0x3000 // atomic bitmask clear on write

#define FUNCSEL_SYS_RIO 5 // a5 in the GPIO function table

#define UNIT       200000
#define DOT        (UNIT)
#define DASH       (3 * UNIT)
#define SYMBOL_GAP (UNIT)
#define LETTER_GAP (3 * UNIT - SYMBOL_GAP)

static volatile uint32_t *out_set;
static volatile uint32_t *out_clr;

static void blink(useconds_t on_time) {
    *out_set = 1 << PIN; // On
    usleep(on_time);
    *out_clr = 1 << PIN; // Off
    usleep(SYMBOL_GAP);
}

int main(void) {
    int fd = open("/dev/gpiomem0", O_RDWR | O_SYNC);
    if (fd < 0) { 
        perror("open /dev/gpiomem0"); return 1;
    }
    volatile uint32_t *base = mmap(NULL, MAP_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (base == MAP_FAILED) { 
        perror("mmap"); return 1; 
    }

    // Register pointers base is uint32_t* divide offsets by 4
    volatile uint32_t *ctrl = base + (IO_BANK0 + 8 * PIN + 4) / 4; // GPIOn_CTRL
    volatile uint32_t *pad = base + (PADS_BANK0 + 4 + 4 * PIN) / 4; // pad GPIOn
    volatile uint32_t *oe_set = base + (SYS_RIO0 + ALIAS_SET + RIO_OE) / 4;
    out_set = base + (SYS_RIO0 + ALIAS_SET + RIO_OUT) / 4;
    out_clr = base + (SYS_RIO0 + ALIAS_CLR + RIO_OUT) / 4;

    *ctrl = (*ctrl & ~0x1fu) | FUNCSEL_SYS_RIO; // route the pin to SYS_RIO
    *pad &= ~(1u << 7); // clear OD (reset value is 1)
    *oe_set = 1u << PIN; // output enable

    while(true) {
        for (int i = 0; i < 3; i++){ // s dot dot dot
            blink(DOT);
        }
        usleep(LETTER_GAP);
        for (int i = 0; i < 3; i++){ // o dash dash dash
            blink(DASH);
        }
        usleep(LETTER_GAP);
        for (int i = 0; i < 3; i++){
            blink(DOT);
        }
        usleep(4*UNIT);
    }
}
