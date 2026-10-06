from sense_hat import SenseHat
import time
o = (255, 165, 0)
r = (255, 0, 0)          # red
yellow = (255, 255, 0)        # yellow
g = (0, 128, 0)          # green
b = (0, 0, 255)          # blue
v = (128, 0, 128)        # violet
k = (0, 0, 0)            # nothing
sense = SenseHat()

def clear_sensehat():
    for r in range(8):
        for c in range(8):
            sense.set_pixel(c, r, (0,0,0))


def row(row_num, color):
    for r in range(8):
        sense.set_pixel(row_num, r, color)


def col(col_num, color):
    for c in range(8):
        sense.set_pixel(c, col_num, color)

if __name__ == "__main__":
    while True:	
        acceleration = sense.get_accelerometer_raw()	

        x = acceleration['x']	
        y = acceleration['y']	
        z = acceleration['z']	
        
        x=round(x, 1)	
        y=round(y, 1)	
        z=round(z, 1)	

        #up
        thres = 0.4
        up = z >= 0.9
        down = z <= -0.9
        xp = x >=thres
        xn = x <= -thres
        yn =  y <= -thres
        yp = y>=thres
        xgs = xp or xn
        ygs = yp or yn
        clear_sensehat()
        if up and not (xgs or ygs):
            sense.show_message("up")
        elif down and not (xgs or ygs):
            print('down')
        elif xp:
            row(7,r)
        elif xn:
            row(0,o)
        elif yp:
            col(7,yellow)
        elif yn:
            col(0,b)
        else:
            clear_sensehat()

        #print("x={0}, y={1}, z={2}".format(x, y, z))
        #print("up={0}, down={1}, xp={2}, xn={3}, yp={4}, yn={5}".format(up, down, xp, xn, yp, yn))
