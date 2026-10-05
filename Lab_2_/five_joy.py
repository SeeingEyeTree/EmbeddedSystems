from sense_hat import SenseHat
o = (255, 165, 0)
r = (255, 0, 0)          # red
y = (255, 255, 0)        # yellow
g = (0, 128, 0)          # green
b = (0, 0, 255)          # blue
v = (128, 0, 128)        # violet
k = (0, 0, 0)            # nothing
sense = SenseHat()

def clear_sensehat():
    for r in range(8):
        for c in range(8):
            sense.set_pixel(c, r, (0,0,0))



def task1():
    sense.show_message("fly away")


def task2():
    sense.show_letter("E",o)


def task3():
    temp = sense.get_temperature()
    msg = f'Temp is {temp}'
    sense.show_message(msg)


def task4():
    rainbow_flag = [
    [r] * 8,
    [o] * 8,
    [y] * 8,
    [g] * 8,
    [b] * 8,
    [v] * 8,
    [k] * 8,
    [k] * 8,
    ]
    for i in range(len(rainbow_flag)):
        for j in range(8):
            sense.set_pixel(i,j, rainbow_flag[i][j])



def task5():
    x_end = 7
    y_end = 7
    for i in range(7):
        x = i
        for j in range(7):
            y = j
            
            if (x_end - x) != 0 :
                slope = (y_end - y) / (x_end - x) 
            else:
                slope = 0

            for k in range(7 - x + 1):
                px = x + k
                py = int(y + k * slope) # round to a int so pix accepts
                if 0 <= py <= 7:
                    sense.set_pixel(px, py, (0, 128, 0))
            time.sleep(0.2)
            clear_sensehat()




if __name__ == "__main__":
    direction = sense.stick.get_events()
    while True:
        thing = ""
        for event in sense.stick.get_events():        
            #print(event.direction, event.action)
            thing = event.direction + " " + event.action
            #print(type(thing))
            #print(thing)
        if thing == "middle held":
            task1()
        elif thing == "left held":
            task2()
        elif thing == "right held":
            task3()
        elif thing == "up held":
            task4()
        elif thing == "down held":
            task5()