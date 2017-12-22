import numpy as np
import cv2

def nothing(x): pass

cap = cv2.VideoCapture(0)
factor = 0.4

cv2.namedWindow('Color Tresholds')
 
#assign strings for ease of coding
hh='Hue High'
hl='Hue Low'
sh='Saturation High'
sl='Saturation Low'
vh='Value High'
vl='Value Low'
wnd = 'Color Tresholds'
#Begin Creating trackbars for each
cv2.createTrackbar(hl, wnd,22,179,nothing)
cv2.createTrackbar(hh, wnd,31,179,nothing)
cv2.createTrackbar(sl, wnd,114,255,nothing)
cv2.createTrackbar(sh, wnd,218,255,nothing)
cv2.createTrackbar(vl, wnd,146,255,nothing)
cv2.createTrackbar(vh, wnd,255,255,nothing)

while 1:
    ret, img = cap.read()
    img = cv2.resize(img,(round(img.shape[1]*factor),round(img.shape[0]*factor)),interpolation = cv2.INTER_AREA)
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hul=cv2.getTrackbarPos(hl, wnd)
    huh=cv2.getTrackbarPos(hh, wnd)
    sal=cv2.getTrackbarPos(sl, wnd)
    sah=cv2.getTrackbarPos(sh, wnd)
    val=cv2.getTrackbarPos(vl, wnd)
    vah=cv2.getTrackbarPos(vh, wnd)
 
    #make array for final values
    HSVLOW=np.array([hul,sal,val])
    HSVHIGH=np.array([huh,sah,vah])

    # Threshold the HSV image
    mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)

    erosionPx = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    eroded = cv2.erode(mask,erosionPx)

    dilatedPx = cv2.getStructuringElement(cv2.MORPH_RECT,(8,8))
    dilated = cv2.dilate(eroded,dilatedPx)

    _,contours,hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    imgcopy = img.copy()
    imgcopy2 = img.copy()
    imgCONT = cv2.drawContours(imgcopy, contours, -1, (255, 0, 0), 2)

    nTrack = np.shape(contours)[0]
    
    cv2.imshow('Camera Input',img)
    cv2.imshow('Camera Input MASK',mask)
    cv2.imshow('Camera Input ERODED',eroded)
    cv2.imshow('Camera Input DILATED',dilated)
    cv2.imshow('Camera Input CONTOURS',imgCONT)

    if nTrack >= 1:
        cnt = contours[0]
        M = cv2.moments(cnt)
        area = cv2.contourArea(cnt)
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(imgcopy2,center,radius,(0,0,255),2)
        txt = '(%s,%s)' % (str(round(x)),str(round(y)))
        cv2.putText(imgcopy2,txt,(int(x + radius),int(y-radius)),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255))
        
    cv2.imshow('Camera Input TRACKING',imgcopy2)
        
        
    k = cv2.waitKey(5) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
