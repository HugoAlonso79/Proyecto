import numpy as np
import imflatfield as ff
import imadjust as ij
import im2double as i2d
import histogram as h
import cv2

from skimage.measure import regionprops_table

# detector HaarCascade de caras 
face_detect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# activar camara
cap = cv2.VideoCapture(0)

# variables globales
bd_stdR = []
bd_stdL = []
bd_meanR = []
bd_meanL = []
bd_hRnegro = []
bd_hRblanco = []
bd_hLnegro = []
bd_hLblanco = []
bd_difR = []
bd_difL = []

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
            adjust_e = ij.imadjust(flatfielde,(0.3,0.5)) # 0.5 - 0.7

            double_e = i2d.im2double(adjust_e)

            # parametros de segmentacion
            alto, ancho = double_e.shape[:2]
            mid = round(ancho/2)
            
            sec_R = [0,0,mid,alto]
            sec_L = [mid+1,0,ancho,alto]

            # separamos el ojo izquierdo y derecho

            Reye = double_e[sec_R[1]:sec_R[1]+sec_R[3],sec_R[0]:sec_R[0]+sec_R[2]]
            Leye = double_e[sec_L[1]:sec_L[1]+sec_L[3],sec_L[0]:sec_L[0]+sec_L[2]]          

            ######################## EXTRACÍÓN DE PROPIEDADES PARA DETECCIÓN ##################
            # HISTOGRAMA
            hR = h.hist(Reye)
            hL = h.hist(Leye)

            hR_blanco = hR[0]
            hR_negro = hR[-1]

            hL_blanco = hL[0]
            hL_negro = hL[-1]

            # PROMEDIO
            mean_R = Reye.mean()*(Reye.shape[0]*Reye.shape[1])
            mean_L = Leye.mean()*(Leye.shape[0]*Leye.shape[1])

            # DESVIACIÓN ESTANDAR
            std_R = Reye.std()*(Reye.shape[0]*Reye.shape[1])
            std_L = Leye.std()*(Leye.shape[0]*Leye.shape[1])

            # OBTENER PROPIEDADES DE REGION DE LA IMAGEN
            props_R = regionprops_table(Reye.astype(int), properties=['convex_image','orientation','convex_area'])
            props_L = regionprops_table(Leye.astype(int), properties=['convex_image','orientation','convex_area'])
            
            heightR, widthR = props_R['convex_image'][0].shape
            heightL, widthL = props_L['convex_image'][0].shape

            difR = widthR - heightR
            difL = widthL - heightL

            areaR = props_R['convex_area'][0]
            areaL = props_L['convex_area'][0]

            OR = props_R['orientation'][0]
            OL = props_L['orientation'][0]

            # ALMACENAJE DE DATA
            bd_stdR.append(std_R)
            bd_stdL.append(std_L)
            bd_meanR.append(mean_R)
            bd_meanL.append(mean_L)
            bd_hRnegro.append(hR_negro)
            bd_hLnegro.append(hL_negro)
            bd_hRblanco.append(hR_blanco)
            bd_hLblanco.append(hL_blanco)
            bd_difR.append(difR)
            bd_difL.append(difL)

            imagen = cv2.hconcat([Reye, Leye])

            cv2.imshow('1',flatfielde)
            cv2.imshow('2',adjust_e)
            cv2.imshow('Ojos',imagen)


    ######################## CONTROL ##################################
    # si se presiona tecla 'esc' termina el programa
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


