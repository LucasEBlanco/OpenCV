# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera 
import numpy as np
import time
import cv2

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

		#Control PI en Ancho
        error = (Ancho/2) - x
        pTerm = P * error
        iTerm += I * error   
        iTerm = constrain(iTerm, (-Ancho/2), Ancho/2)    
        PiX =  pTerm + iTerm       
        
        mapeoX = map(PiX, -Ancho/2, Ancho/2, 0, 140)
  
        
        #Control en PI anltura
        errorY = (Alto/2) - y
        pTermY = Py * errorY
        iTermY += Iy * errorY
        iTermY = constrain(iTermY, (-Alto/2) , Alto/2) 
        PiY = pTermY + iTermY
        PiY = constrain(PiY, (-Alto/2) , Alto/2) 
        mapeoY = map(PiY, -Alto/2, Alto/2, 60, 0)

        print (">>PtermY: %d, PiY: %d, MApeo Y to Grado: %d"%(pTermY, PiY, mapeoY))
	
    # show the frame
    cv2.imshow("Monitor", imagen)
    key = cv2.waitKey(1) & 0xFF
 
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
 
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
       

