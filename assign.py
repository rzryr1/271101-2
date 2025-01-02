import cv2
from cvzone.HandTrackingModule import HandDetector
from pyfirmata import Arduino, SERVO
import time


def rotateservo(pin, angle):
    board.digital[pin].write(angle)
    time.sleep(0.015)


def servo(total_angle, pin):
    if total_angle > 180:
        total_angle = 180  
    rotateservo(pin, total_angle)

cport = int(input('Enter the camera port: '))
video = cv2.VideoCapture(cport)

comport = input('Enter the Arduino board COM port: ')
board = Arduino(f'COM{comport}')
pin = 9  
board.digital[pin].mode = SERVO

detector = HandDetector(detectionCon=0.7, maxHands=2)

while True:
    success, image = video.read()
    if not success:
        print("Failed to access camera.")
        break

    
    hands, img = detector.findHands(image, flipType=False)

    total_angle = 0  

    
    for hand in hands:
        fingers = []
        lmList = hand["lmList"]  
        hand_type = hand["type"]  

        
        if hand_type == "Right":  
            if lmList[4][0] < lmList[3][0]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:  
            if lmList[4][0] > lmList[3][0]:
                fingers.append(1)
            else:
                fingers.append(0)

        
        for i in range(1, 5):
            if lmList[4 * i + 4][1] < lmList[4 * i + 2][1]:  
                fingers.append(1)
            else:
                fingers.append(0)

        
        total_fingers = fingers.count(1)
        hand_angle = total_fingers * 18  
        total_angle += hand_angle
    
    servo(total_angle, pin)

    
    cv2.putText(image, f"Total Angle: {total_angle} Degrees", (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
    cv2.putText(img, "Tanawat Arampraphat" , (450, 60), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)     
    cv2.putText(img, "670610759" , (450, 90), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
                

    
    cv2.imshow("Hand Tracking", image)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video.release()
cv2.destroyAllWindows()
