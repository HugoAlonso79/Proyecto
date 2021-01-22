import numpy as np
import imflatfield as ff
import imadjust as ij
import im2double as i2d
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
            flatfielde = ff.gammaCorrection(eye, 0.7) #valor 0.73 análogo a alpha=60 en MATLAB

            # ajuste de contraste - funcion análoga Imadjust de MATLAB
            adjust_e = ij.imadjust(flatfielde,(0.5,0.7))

            double_e = i2d.im2double(adjust_e)

            # parametros de segmentacion
            alto, ancho = double_e.shape[:2]
            mid = round(ancho/2)
            
            sec_R = [0,0,mid,alto]
            sec_L = [mid+1,0,ancho,alto]

            Reye = double_e[sec_R[1]:sec_R[1]+sec_R[3],sec_R[0]:sec_R[0]+sec_R[2]]
            Leye = double_e[sec_L[1]:sec_L[1]+sec_L[3],sec_L[0]:sec_L[0]+sec_L[2]]

           
            

            cv2.imshow('Derecho',Reye)
            cv2.imshow('Izquierdo',Leye)


    ######################## CONTROL ##################################
    # si se presiona tecla 'esc' termina el programa
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


