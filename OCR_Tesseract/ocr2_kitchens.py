# Code for the Stackoverflow thread: https://stackoverflow.com/questions/65277845/how-to-obtain-the-best-result-from-pytesseract/65278387?noredirect=1#comment115407021_65278387
# Question and initial code by Matteo
# Extended with additional image processing by Todor, 13.12.2020
# Recognizes "Cucine" if given only with the box with "Lube"

import cv2
import numpy as np
import pytesseract
#pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\pytesseract\tesseract.exe'
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
print(pytesseract.pytesseract.tesseract_cmd)
#path_to_image = "logo.png"
path_to_image = "logo2.png" #cropped the region with "Cucine" and "Lube"
path_to_image = "kitchens.png"
image = cv2.imread(path_to_image)
h, w, _ = image.shape
h1, w1 = h, w
w*=5; h*=5
w = (int)(w); h = (int) (h)
#green channel

alpha = 1.4 #contrast
beta = -0.4 #brightness

#alpha = 1.0 #contrast
#beta =  0.0 #brightness

image2 = image.copy()
#image2 = cv2.resize(image2,(w*4,h*4), interpolation = cv2.INTER_AREA)
#image2 = cv2.resize(image2,(w*2,h*4), interpolation = cv2.INTER_AREA)
#cv2.imshow("SHEAR",image2)

b,g,r = cv2.split(image2)

mask = cv2.inRange(g, 225, 255) 
b[mask!=0] = 0
g[mask!=0] = 0
r[mask!=0] = 0

b[mask==0] = 255
g[mask==0] = 255
r[mask==0] = 255
cv2.imshow("B",g)

custom_config = r'--oem 3 --psm 11' 
text = pytesseract.image_to_string(g, config=custom_config)#, lang="ita")
print(text)
cv2.waitKey(0)  

contrast = image.copy()

#Change contrast and brightness - might be not necessary, just find appropriate values for the mask
for y in range(image.shape[0]):
    for x in range(image.shape[1]):
        for c in range(image.shape[2]):
            contrast[y,x,c] = np.clip(alpha*image[y,x,c] + beta, 0, 255)
cv2.imshow('contrast', contrast)
cv2.waitKey(0)            
h, w, _ = contrast.shape 
contrast = cv2.resize(contrast,(w*3,h*3), interpolation = cv2.INTER_AREA)
contrast = cv2.resize(contrast,(w*2,h*3), interpolation = cv2.INTER_AREA)

contrastBW = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.floodFill(contrastBW, None, (0,0), 255)
contrastBW = cv2.adaptiveThreshold(contrastBW, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,3,1)

cv2.imshow('contrastBW', contrastBW)
cv2.waitKey(0)  
text = pytesseract.image_to_string(contrastBW)#, lang="ita")
print(text)


image = contrast

b,g,r = cv2.split(image)
mask = cv2.inRange(g, 210, 255) 
b[mask!=0] = 0
g[mask!=0] = 0
r[mask!=0] = 0

b[mask==0] = 255
g[mask==0] = 255
r[mask==0] = 255

image = cv2.merge([b,g,r])
cv2.imshow('MASK', image)
image = cv2.resize(image, (w,h), interpolation = cv2.INTER_AREA)

#Colors are not needed, but it doesn't matter
text = pytesseract.image_to_string(image)#, lang="ita")
print(text)
text = pytesseract.image_to_string(g, lang="ita",  config=custom_config)
print(text)
cv2.waitKey(0)

cv2.imwrite("logo_without_threshold_median_etc.png", g)

def Additional():
    image = cv2.resize(image, (w,h), interpolation = cv2.INTER_AREA) #Resize 3 times
    # converting image into gray scale image
    #mask = mas

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('grey image', gray_image)
    cv2.waitKey(0)
    # converting it to binary image by Thresholding
    # this step is require if you have colored image because if you skip this part
    # then tesseract won't able to detect text correctly and this will give incorrect result
    threshold_1 = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # display image
    cv2.imshow('threshold image default', threshold_1)            
    cv2.imwrite("logo_thresh_bin.png", threshold_1)
    cv2.waitKey(0)

    threshold_img = threshold_1

    #cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    threshold_img = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,            cv2.THRESH_BINARY,13,2) #cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)[1]
    #cv2.imshow('ADAPTIVE THRESHOLD image', threshold_img)    

    threshold_img = cv2.resize(threshold_img, (w1,h1), interpolation = cv2.INTER_AREA) #Resize 3 times

    #cv2.waitKey(0)
    #threshold_img = cv2.GaussianBlur(threshold_img,(3,3),0)
    #threshold_img = cv2.GaussianBlur(threshold_img,(3,3),0)
    #threshold_img = cv2.medianBlur(threshold_img,3)
    #cv2.imshow('medianBlur', threshold_img)            
    #cv2.waitKey(0)
    threshold_img  = cv2.bitwise_not(threshold_img)
    cv2.imshow('Invert', threshold_img)            
    cv2.waitKey(0)
    cv2.imwrite("logo_out.png", threshold_img)
    kernel = np.ones((1, 1), np.uint8)  
    # Using cv2.erode() method  
    threshold_img = cv2.dilate(threshold_img, kernel)  
    cv2.imshow('Dilate', threshold_img)            
    cv2.waitKey(0)
    #cv2.imshow('threshold image', threshold_img)
    # Maintain output window until user presses a key
    #cv2.waitKey(0)
    # Destroying present windows on screen
    cv2.destroyAllWindows()
    # now feeding image to tesseract
    print(dir(pytesseract))
    text = pytesseract.image_to_string(threshold_img, lang="ita")
    box = pytesseract.image_to_boxes(threshold_img, lang="ita")
    data = pytesseract.image_to_data(threshold_img, lang="ita")
    print(text)
    print(box)
    print(data)
    
#Additional()    #trying other transformations
