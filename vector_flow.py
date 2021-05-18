import cv2
import numpy as np
import copy
import math
import time

def vector_flow(video_path):
    cap = cv2.VideoCapture(video_path)
    
    # Take first frame and find corners in it
    ret, old_frame = cap.read()
    image = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

    mask = np.zeros_like(old_frame)
    while True:
        maxMag = 0
        ret, frame = cap.read()
        if not ret:
            break
        image2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        #Shape is an array that conatains width and height
        #arrows is a 3D array of imageSize x 3
        arrows = np.zeros((image.shape[0], image.shape[1], 3), np.float32)
        mag = np.zeros((image.shape[0],image.shape[1],1),np.float32)
        theta = np.zeros((image.shape[0],image.shape[1],1),np.float32)
        
        u = np.zeros((image.shape[0],image.shape[1],1),np.float32)
        v = np.zeros((image.shape[0],image.shape[1],1),np.float32)
        
        ix = np.zeros((image.shape[0], image.shape[1],1), np.float32)
        iy = np.zeros((image.shape[0], image.shape[1], 1), np.float32)
        it = np.zeros((image.shape[0], image.shape[1], 1), np.float32)

        ixx = np.zeros((image.shape[0], image.shape[1], 1), np.float32)
        ixy = np.zeros((image.shape[0], image.shape[1], 1), np.float32)
        iyy = np.zeros((image.shape[0], image.shape[1], 1), np.float32)
        ixt = np.zeros((image.shape[0], image.shape[1], 1), np.float32)
        iyt = np.zeros((image.shape[0], image.shape[1], 1), np.float32)
        
        for i in range(0,image.shape[0],1):
            for j in range(0,image.shape[1],1):
                if(j>0 and j<image.shape[1]-1):
                    ix[i][j] = int(image[i][j-1]) - int(image[i][j+1])
                
                if(i>0 and i<image.shape[0]-1):
                    iy[i][j] = int(image[i-1][j]) - int(image[i+1][j])
                
                ixx[i][j] = ix[i][j]*ix[i][j]
                iyy[i][j] = iy[i][j]*iy[i][j]
                ixy[i][j] = ix[i][j]*iy[i][j]
                
                #magnitude of change for one pixel
                it[i][j] = int(image2[i][j]) - int(image[i][j])
                ixt[i][j] = ix[i][j] * it[i][j]
                iyt[i][j] = iy[i][j] * it[i][j]

        #print("iamge size :", image.shape[0], image.shape[1])

        pos = 0

        # traversal of the image pixel by pixel
        for i in range(0, image.shape[0], 5):
            for j in range(0, image.shape[1], 5):
                ixxsum = 0
                iyysum = 0
                ixysum = 0
                ixtsum = 0
                iytsum = 0

                # for each pixel create a 15x15 border 
                # and add all of them into a single variable 
                for l in range(-6,7):
                    for m in range(-6,7):
                        #clamp in image
                        if((i+l>0 and i+l<image.shape[0]) and (j+m>0 and j+m<image.shape[1])):
                            ixxsum += ixx[i+l][j+m]
                            iyysum += iyy[i+l][j+m]
                            ixysum += ixy[i+l][j+m]
                            ixtsum += ixt[i+l][j+m]
                            iytsum += iyt[i+l][j+m]

                pos += 1

                #if((ixxsum*iyysum)-(ixysum*ixysum) == 0):
                if ixxsum*iyysum == ixysum**2:
                    u[i][j] = 0
                    v[i][j] = 0
                    theta[i][j] = 0
                else:
                    u[i][j] = ((-iyysum*ixtsum) + ixysum*iytsum)/((ixxsum*iyysum)-(ixysum*ixysum))
                    v[i][j] = ((ixysum*ixtsum) - (ixxsum*iytsum))/((ixxsum*iyysum)-(ixysum*ixysum))
                    theta[i][j] = math.atan2(v[i][j], u[i][j])
                
                #distantce between u[i][j] si v[i][j]
                mag[i][j] = math.sqrt((u[i][j]**2) + (v[i][j]**2))
                if (mag[i][j] > maxMag):
                    maxMag = mag[i][j]
                if (maxMag == 0):
                    maxMag = 1
        
        #print("End of giant for")

        #Makes steps 5 by 5 pixels to calculate movement
        for i in range(0,image.shape[0],5):
            for j in range(0,image.shape[1],5):
                scaleflow = 15 * (mag[i][j] / maxMag)
            
                cv2.arrowedLine(arrows,(j,i),((int(((scaleflow*u[i][j]) + j))),(int((i+(scaleflow*v[i][j]))))),(0,255,0))


        cv2.imshow("arrows",arrows/255)

        k = cv2.waitKey(25) & 0xFF
        if k == 27:
            break
        if k == ord("c"):
            mask = np.zeros_like(old_frame)

        # Now update the previous frame and previous points
        image = image2.copy()
    