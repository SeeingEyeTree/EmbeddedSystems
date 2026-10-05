from sense_hat import SenseHat
import time
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
        down z <= -0.9
        xp = x >=thres
        xn = x <= -thres
        yn =  y <=thres
        yp = y>=thres
        x = xp or xn
        y = yp or yn
        if up and not (x or y):
            sense.show_message("up")
        elif down and not (x or y):
            print('down')

        print("x={0}, y={1}, z={2}".format(x, y, z))
