#This code demonstrate how to show location of hand landmark
import cv2
import mediapipe as mp
import time
import pyfirmata

time.sleep(2.0)
showfinger = []
Nfing = 5
cap = cv2.VideoCapture(0)

#Call hand pipe line module
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

def check_user_input(input):
    try:
        # Convert it into integer
        val = int(input)
        # print("Input is an integer number. Number = ", val)
        bv = True
    except ValueError:
        try:
            # Convert it into float
            val = float(input)
            # print("Input is a float  number. Number = ", val)
            bv = True
        except ValueError:
            # print("No.. input is not a number. It's a string")
            bv = False
    return bv

cport = input('Enter the camera port: ')
while not (check_user_input(cport)):
    print('Please enter a number not string')
    cport = input('Enter the camera port: ')

comport = input('Enter the arduino board COM port: ')
while not (check_user_input(comport)):
    print('Please enter a number not string')
    comport = input('Enter the arduino board COM port: ')

board=pyfirmata.Arduino('COM'+comport)
led_1=board.get_pin('d:13:o') #Set pin to output
led_2=board.get_pin('d:12:o')
led_3=board.get_pin('d:11:o')
led_4=board.get_pin('d:10:o')
led_5=board.get_pin('d:9:o')


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    showfinger.clear()

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)               
                if id == 4:
                    id4 = int(id)
                    cx4 = cx
                if id == 3:
                    id3 = int(id)
                    cx3 = cx
                if id == 8:
                    id8 = int(id)
                    cy8 = cy
                if id == 6:
                    id6 = int(id)
                    cy6 = cy
                if id == 12:
                    id12 = int(id)
                    cy12 = cy
                if id == 10:
                    id10 = int(id)
                    cy10 = cy 
                if id == 16:
                    id16 = int(id)
                    cy16 = cy
                if id == 14:
                    id14 = int(id)
                    cy14 = cy      
                if id == 20:
                    id20 = int(id)
                    cy20 = cy
                if id == 18:
                    id18 = int(id)
                    cy18 = cy                                     
            if cx4 < cx3:
                pong = 0 
                led_1.write(0)
                if "Thumb" in showfinger:
                    showfinger.remove("Thumb")                                      
            else:
                pong = 1
                led_1.write(1)
                if "Thumb" not in showfinger:
                    showfinger.append("Thumb")
                    
            if cy8 > cy6:
                chee = 0
                led_2.write(0)
                if "Index" in showfinger:
                    showfinger.remove("Index") 
            else:
                chee = 1
                led_2.write(1) 
                if "Index" not in showfinger:
                    showfinger.append("Index")
                    
            if cy12 > cy10:
                klang = 0
                led_3.write(0)
                if "Middle" in showfinger:
                    showfinger.remove("Middle")  
            else:
                klang = 1
                led_3.write(1)
                if "Middle" not in showfinger:
                    showfinger.append("Middle")
                    
                    
            if cy16 > cy14:
                nang = 0
                led_4.write(0)
                if "Ring" in showfinger:
                    showfinger.remove("Ring")  
            else:
                nang = 1
                led_4.write(1)
                if "Ring" not in showfinger:
                    showfinger.append("Ring")
                    
                    
            if cy20 > cy18:
                koi = 0
                led_5.write(0)
                if "Pinky" in showfinger:
                    showfinger.remove("Pinky")  
            else:
                koi = 1 
                led_5.write(1)
                if "Pinky" not in showfinger:
                    showfinger.append("Pinky")
                    
                       
            
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.putText(img, "Finger: " + str(showfinger) , (100, 400), cv2.FONT_HERSHEY_PLAIN, 1,(255, 255, 255), 1)
    cv2.putText(img, "Tanawat Arampraphat" , (450, 70), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)     
    cv2.putText(img, "670610759" , (450, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)               
    cv2.imshow("Image", img)
    k=cv2.waitKey(1)
    if k==ord('q'):  #press "q" to exit programe
       break
#Closeing all open windows
#cv2.destroyAllWindows()