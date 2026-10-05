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

            print("x={0}, y={1}, z={2}".format(x, y, z))
