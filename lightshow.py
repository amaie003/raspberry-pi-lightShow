import time
from rpi_ws281x import *
import argparse
import math
import socket
import json

# LED strip configuration:
LED_COUNT      = 140      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def solidLightWipe(strip,color,wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i,color)
        strip.show()
        time.sleep(wait_ms/1000)
 

def breath(strip,color,speed,wait_ms=50):
    increment = 1
    initialColor = list(color)
    print("start "+str(color[0])+","+str(color[1])+","+str(color[2]))
    while True:
        for i in range(strip.numPixels()):
            #print("set "+str(color[0])+","+str(color[1])+","+str(color[2]))
            #print("increase?"+str(increment))
            strip.setPixelColor(i,Color(math.floor(color[0]),math.floor(color[1]),math.floor(color[2])))
        strip.show()

        if increment == 1:
            color[0] = min(255, color[0]*(1+speed))
            color[1] = min(255, color[1]*(1+speed))
            color[2] = min(255, color[2]*(1+speed))
        elif increment == -1:
            color[0] = max(0, color[0]*(1-speed))
            color[1] = max(0, color[1]*(1-speed))
            color[2] = max(0, color[2]*(1-speed))
        
        if (color[0] >= initialColor[0] or color[1] >= initialColor[1] or color[2] >= initialColor[2]):
            color[0] = initialColor[0]
            color[1] = initialColor[1]
            color[2] = initialColor[2]
            time.sleep(10)
            increment = -1
        
        if(color[0]<= 2 or color[1]<= 2 or color[2]<= 2):
            increment = 1
        time.sleep(wait_ms/1000.0)

def make_histogram(cluster):
    """
    Count the number of pixels in each cluster
    :param: KMeans cluster
    :return: numpy histogram
    """
    numLabels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    hist, _ = np.histogram(cluster.labels_, bins=numLabels)
    hist = hist.astype('float32')
    hist /= hist.sum()
    return hist
def make_bar(color):
    """
    Create an image of a given color
    :param: height of the image
    :param: width of the image
    :param: BGR pixel values of the color
    :return: tuple of bar, rgb values, and hsv values
    """
   
    red, green, blue = int(color[2]), int(color[1]), int(color[0])

    return (red, green, blue)
# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
 
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
 
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
 
    try:
        print("---------Welcome to the lightshow---------------")
        print("Enter '0' for breathing mode")
        print("Enter 'X' to exit")
        print("------------------------------------------------")
        option = input("Enter Option:")
        if option == "0":
            colorR = input ("Breath Color Red Level:")
            colorG = input ("Breath Color Green Level:")
            colorB = input ("Breath Color Blue Level:")
            speed = input("Enter color speed")
            breath(strip,[int(colorR),int(colorG),int(colorB)],float(speed),70)
        elif option == 'x' or option == 'X':
            solidLightWipe(strip, Color(0,0,0), 20)
        elif option == "1":
            HOST = '192.168.1.188'
            PORT = 12345
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print("socket created")

            try:
                s.bind((HOST,PORT))
            except socket.error:
                print("Bind Failed")
            s.listen(1)
            print("Socket awaitng message")
            (conn,addr) = s.accept()
            print("Connected")

            while True:
                data = conn.recv(1024)
                data = json.loads(data.decode())
                

                print("I Sent a Message back in response to" + str(data["r"]) + ","+str(data["g"]) + ","+str(data["b"]))
                if data == "Hello":
                    reply = "Hi,back"
                elif data == "test":
                    reply = "test back"
                elif data == "quit":
                    conn.send("Terminating")
                    break
                else:
                    reply = "unknown"
                conn.send(reply)
            conn.close()

    except KeyboardInterrupt:
        if args.clear:
            solidLightWipe(strip, Color(0,0,0), 10)







