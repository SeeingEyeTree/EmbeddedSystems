// Blink SOS on the Pi 5 ACT LED (AON GPIO 9) using mmap() on /dev/mem.
// AON GPIO is a brcmstb GPIO block inside the BCM2712 (not RP1), so
// /dev/gpiomem0 cannot reach it; we map the physical address directly.
//
// Before running, stop the kernel from touching the LED:
//   echo none | sudo tee /sys/class/leds/ACT/trigger
// Build: gcc blink.c -o blink     Run: sudo ./blink
//
// Addresses come from the BCM2712 device tree (gpio@7d517c00 under the
// soc at 0x1000000000). Verify on your Pi before trusting them:
//   xxd -p /proc/device-tree/axi/gpio@7d517c00/reg 2>/dev/null ||
//   find /proc/device-tree -name 'gpio@7d517c00'
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>

#define AON_GPIO_PHYS  0x107d517c00ULL   // AON GPIO bank 0
#define PAGE_MASK_4K   (~0xfffULL)

// brcmstb GPIO bank 0 register offsets
#define GIO_DATA       0x04   // pin levels / output values
#define GIO_IODIR      0x08   // 1 = input, 0 = output

#define PIN            9      // AON GPIO 9, ACT LED, active-low (0 = on)

#define UNIT       200000
#define DOT        (UNIT)
#define DASH       (3 * UNIT)
#define SYMBOL_GAP (UNIT)
#define LETTER_GAP (3 * UNIT - SYMBOL_GAP)  // blink() already adds one symbol gap

static volatile uint32_t *data;

static void blink(useconds_t on_time) {
    *data &= ~(1u << PIN);  // On  (active-low)
    usleep(on_time);
    *data |= (1u << PIN);   // Off
    usleep(SYMBOL_GAP);
}

int main(void) {
    int fd = open("/dev/mem", O_RDWR | O_SYNC);
    if (fd < 0) { perror("open /dev/mem (need sudo)"); return 1; }

    uint64_t page = AON_GPIO_PHYS & PAGE_MASK_4K;
    uint64_t off  = AON_GPIO_PHYS - page;
    volatile uint8_t *map = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE,
                                 MAP_SHARED, fd, (off_t)page);
    if (map == MAP_FAILED) { perror("mmap"); return 1; }

    volatile uint32_t *iodir = (volatile uint32_t *)(map + off + GIO_IODIR);
    data = (volatile uint32_t *)(map + off + GIO_DATA);

    printf("IODIR=%08x DATA=%08x\n", *iodir, *data);  // sanity check
    *data |= (1u << PIN);     // start with LED off
    *iodir &= ~(1u << PIN);   // pin 9 -> output

    while (true) {
        for (int i = 0; i < 3; i++) blink(DOT);   // s
        usleep(LETTER_GAP);
        for (int i = 0; i < 3; i++) blink(DASH);  // o
        usleep(LETTER_GAP);
        for (int i = 0; i < 3; i++) blink(DOT);   // s
        usleep(4 * UNIT);
    }
}
