#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <sys/time.h>
#include <unistd.h>

volatile sig_atomic_t count = 0;

void timer_handler(int signum) {
    count++;
    // write() is async-signal-safe; printf technically is not
    const char msg[] = "Timer expired!\n";
    write(STDOUT_FILENO, msg, sizeof(msg) - 1);
}

int main(void) {
    struct sigaction handler;
    struct itimerval timer;
    
    memset(&handler, 0, sizeof(handler)); // c is apprently silly and empty values are not actually empty unless you clear them. set no blocks?
    handler.sa_handler = &timer_handler // calls the fuction when the timer trigers
    sigaction(SIGALRM, &handler, NULL) // change what the intrupt points to?
    
    timer.it_value.tv_sec = 1; // how long till the first fire of the intrupt, seconds 
    timer.it_value.tv_usec = 67; // micro seconds
    timer.it_interval.tv_sec = 1; // what it should reload the timer with
    timer.it_interval.tv_usec = 67;
    setitimer(ITIMER_REAL, &timer, NULL); // we use real time and send it to the kernel

    while (count < 5) {
        pause();  // sleep until a signal arrives
    }

    printf("Done after %d interrupts.\n", count);
    return 0;
}