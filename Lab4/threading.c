#include <sched.h>
#include <pthread.h>
#include <stdio.h>
//#include <chrono>
//#include <windows.h>
#include <unistd.h>


pthread_mutex_t mutex;
pthread_mutexattr_t mutexattr;
pthread_t thread1, thread2, thread3;

struct sched_param param; //declare structure variable
int priority1 = 10;
int priority2 = 5;
int priority3 = 1;
int policy; // policy is an int variable;
int waiter_priority = 0; // prio of waiting threads

void CPU_wait(){
    for (volatile long i = 0; i < 100000000; i++);
}


static void doWork(int id, int prio)
{
    
    for (int percent = 10; percent < 100; percent += 10) {
        CPU_wait();
        int runing_prio;
        if (prio > waiter_priority){
            runing_prio = prio;
        }
        else{
            runing_prio = waiter_priority;
        }
        printf("Thread %d running, priority %d, process %d%% ...\n", id, runing_prio, percent);
    }
}


void function(int id, int prio)
{
    printf("Thread %d requests the lock\n", id);
    if (prio > waiter_priority) 
    {
        waiter_priority = prio;
    }
    //critical section: lock the mutex, do some work here, unlock the mutex.
    pthread_mutex_lock(&mutex);
    waiter_priority = 0;                                // we hold it; nobody else is waiting yet
    printf("Thread %d had the lock\n", id);
    
    doWork(id, prio);
    printf("Thread %d released the lock\n", id); 
    pthread_mutex_unlock(&mutex);
}


void *function1(void *arg)
{
    //function 1 for thread 1.
    //do some work here and call function()
    printf("Thread 1 starts\n");
    function(1, priority1);
    printf("Thread 1 complete\n");
    return NULL;
}

void *function2(void *arg)
{
    //function 2 for thread 2.
    //do some work here
    printf("Thread 2 starts\n");
    doWork(2, priority2);
    printf("Thread 2 complete\n");
    return NULL;
}

void *function3(void *arg)
{
    //function 3 for thread 3.
    //do some work here and call function()
    printf("Thread 3 starts\n");
    function(3, priority3);
    printf("Thread 3 complete\n");
    return NULL;
}

int main()
{
    policy = SCHED_FIFO; // assign SCHED_FIFO to declared policy variable
    int maxpriority = sched_get_priority_max(policy); // get max priority
    int minpriority = sched_get_priority_min(policy); // get min priority

    struct sched_param mp; mp.sched_priority = maxpriority;
    pthread_setschedparam(pthread_self(), SCHED_FIFO, &mp); // main always needs to run with max prio


    //create mutex and initialize it.
    pthread_mutexattr_init(&mutexattr); //initialize mutex attribute first
    pthread_mutexattr_setprotocol(&mutexattr, PTHREAD_PRIO_INHERIT);
    //setting protocol for mutex attribute
    pthread_mutex_init(&mutex, &mutexattr); //init mutex with


    //set different priority for each thread
    struct sched_param param1, param2, param3;


    //create thread 1, thread 2 and thread 3
    printf("Creating thread 3");
    pthread_create(&thread3, NULL, function3, NULL);
    param3.sched_priority = priority3; //assign priority to structure variable
    pthread_setschedparam(thread3,policy,&param3); // set thread1
    
    usleep(500000);
    printf("Creating thread 1");
    pthread_create(&thread1, NULL, function1, NULL);
    param1.sched_priority = priority1;
    pthread_setschedparam(thread1,policy,&param1); // set thread1
    
    usleep(500000);
    printf("Creating thread 2");
    pthread_create(&thread2, NULL, function2, NULL);
    param2.sched_priority = priority2;
    pthread_setschedparam(thread2,policy,&param2); // set thread1
    
    
    


    //set handler for thread 1, thread 2 and thread 3 respectively. For instance, function 1 for thread 1, function 2 for thread 2 and function 3 for thread 3
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    pthread_join(thread3, NULL);
    return 0;

}