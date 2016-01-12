# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera 
import numpy as np
import time
import cv2


def nothing(x):
    pass

    
# Dimenciones de video
Ancho = 320
Alto = 240

# Variable GLobales
pTerm = iTerm = pTermY = iTermY = x = y = 0

# Variables Control PI en X
P = 0.3
I = 0.1 

# Variables Control PI en X
Py = 0.3
Iy = 0.1

# Creamos las barras de seleccion de colores 
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)

# creamos un switch for ON/OFF para aplicar los colores selecccionados 
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)

# Definimos Las Funciones 
def map( z, in_min, in_max, out_min, out_max):
	 return (z - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
			
def constrain( q, a, b):	
	 if q < a:
		  return a 
	 if q > b:
		  return b
	 else:
		 return q	  

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (Ancho, Alto) # resolucion de salida de video
camera.framerate = 24
rawCapture = PiRGBArray(camera, size=(Ancho, Alto))

# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    imagen = frame.array

    #Establecemos el rango de colores que vamos a detectar
    azul_bajos = np.array([86, 31, 4], dtype=np.uint8)
    azul_altos = np.array([220, 88, 50], dtype=np.uint8)

    #Crear una mascara con solo los pixeles dentro del rango de verdes
    mask = cv2.inRange(imagen, azul_bajos, azul_altos)

    #Encontrar el area de los objetos que detecta la camara
    moments = cv2.moments(mask)
    area = moments['m00']

    #Descomentar para ver el area por pantalla
    #print area
    if(area > 20000):
        #Buscamos el centro x, y del objeto
        x = int(moments['m10']/moments['m00'])
        y = int(moments['m01']/moments['m00'])
        cv2.rectangle(imagen, (x, y), (x+20, y+20),(255,0,255), 1) 

        print ("aca iba el mapeo del movimiento")
    
    # get current positions of four trackbars
    r = cv2.getTrackbarPos('R','image')
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')
    if s == 0:
        img[:] = 0
    else:
        img[:] = [b,g,r]

    # show the frame
    cv2.imshow("Monitor", imagen)
    key = cv2.waitKey(1) & 0xFF
 
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
 
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
       

