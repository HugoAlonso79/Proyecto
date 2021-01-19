import numpy as np
import imflatfield as ff
import cv2

# detector HaarCascade de caras 
face_detect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# activar camara
cap = cv2.VideoCapture(0)

while 1:
    # captura de imagen y extraccion del canal verde
    ret, frame = cap.read()
    canal = frame[:,:,2]
    
    # detectar cara
    faces = face_detect.detectMultiScale(canal,1.1,5)
    if len(faces) != 0:
        max_i = 0
        for a in range(len(faces)):
            if faces[a][2] > faces[max_i][2]:
                max_i = a

        # recortar cara
        bbox_face = faces[max_i]                   
        face = canal[bbox_face[1]:bbox_face[1]+bbox_face[3], bbox_face[0]:bbox_face[0]+bbox_face[2]]
        facepic = frame[bbox_face[1]:bbox_face[1]+bbox_face[3], bbox_face[0]:bbox_face[0]+bbox_face[2]]

        # detector HaarCascade de ojos
        eye_detect = cv2.CascadeClassifier('haarcascade_mcs_eyepair_big.xml')

        # detectar ojos
        eyes = eye_detect.detectMultiScale(face)
        
        if len(eyes) != 0:
            maxi = 0
            for b in range(len(eyes)):
                if eyes[b][2] > eyes[maxi][2]:
                    maxi = b

            # recortar ojos        
            bbox_eye = eyes[maxi] 
            eye = face[bbox_eye[1]:bbox_eye[1]+bbox_eye[3], bbox_eye[0]:bbox_eye[0]+bbox_eye[2]]
            eyepic = facepic[bbox_eye[1]:bbox_eye[1]+bbox_eye[3], bbox_eye[0]:bbox_eye[0]+bbox_eye[2]]

            # correccion de campo de plano para emparejar sombreado
            flatfielde = ff.gammaCorrection(eye, 0.7) #valor 0.73 analogo a alpha=60 en MATLAB

            cv2.imshow('Blink Detection',flatfielde)


    ######################## CONTROL ##################################
    # si se presiona tecla 'esc' termina el programa
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


