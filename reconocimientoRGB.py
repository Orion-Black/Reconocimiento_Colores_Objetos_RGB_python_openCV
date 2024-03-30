import cv2 # importamos CV2 para el tratamiento de imagenes
import numpy as np # Importamos numpy para trabajar con matrices

#Función para identificar los objetos y clasificar su color
def detectarColor(frame, colorBajo, colorAlto, nombreColor):
    # Convertimos el frame actual de BGR a HSV
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Creamos la mascara del color brindado
    mascara = cv2.inRange(hsvFrame, colorBajo, colorAlto)
    # Encontramos los contornos de la mascara
    contornos,_ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iteramos todos los contornos disponibles
    for c in contornos:
        # Obtenemos el area del contorno identificado
        area = cv2.contourArea(c)
        # obtenemos coordenadas y valores width y height del contorno identificado
        x, y, w, h = cv2.boundingRect(c)

        # Si el area del contorno es mayor a 10000 (Nota: deriva de "100x100" sobre la imagen) se resalta el contorno
        if (area > 10000 and area < 25000):
            #Dibujar un rectangulo amarillo alrededor del contorno del objeto
            cv2.rectangle(frame, (x,y), (x + w, y + h), (0,255,255), 3)
            #Colocar nombre del color detectado
            cv2.putText(frame, f"{nombreColor} {x}, {y}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 1)
            
    return frame


# Función de inicio del programa
def iniciar():
    # Capturar flujo de video de la camara IP
    video = cv2.VideoCapture("http://192.168.84.239:40000/video")

    # Definir los rangos de colores HSV para rojo, verde y azul
    rojoBajo1 = np.array([0,120,20], np.uint8) #Ajustar el segundo valor si cambia iluminacion xd (120 to whatever)
    rojoAlto1 = np.array([18,255,255], np.uint8)

    rojoBajo2 = np.array([170,120,20], np.uint8)
    rojoAlto2 = np.array([179,255,255], np.uint8)

    verdeBajo = np.array([40, 100, 20], np.uint8)
    verdeAlto = np.array([80, 255,255], np.uint8)

    azulBajo = np.array([100, 100, 20], np.uint8)
    azulAlto = np.array([135, 255, 255], np.uint8)

    # Ciclo while infinito para desplegar el video procesado
    while video.isOpened():
        # Capturamos los frames a usar
        ret, frame = video.read()
        # Si se detectan frames se inicia el procesamiento si no hay frames se finaliza el programa
        if ret == True:
            # Detectar los colores de los objetos
            frame = detectarColor(frame, rojoBajo1, rojoAlto1, "Rojo")
            frame = detectarColor(frame, rojoBajo2, rojoAlto2, "Rojo")
            frame = detectarColor(frame, verdeBajo, verdeAlto, "Verde")
            frame = detectarColor(frame, azulBajo, azulAlto, "Azul")
            # Mostrar el frame con objetos detectados en una ventana
            cv2.imshow("Camara Brazo", frame)
            # Configurar la tecla q para terminar la ejecución
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    # Liberamos los recursos utilizados
    video.release()
    cv2.destroyAllWindows()

# Iniciar ejecución del programa
iniciar()

