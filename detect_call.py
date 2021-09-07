import cv2
import numpy as np
import smtplib
import config

cap = cv2.VideoCapture('people.mp4')

frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1920,1080))
#FOURCC is short for "four character code" - an identifier for a video codec, compression format, color 
# or pixel format used in media files.

ret, frame1 = cap.read()
ret, frame2 = cap.read()
print(frame1.shape)
print(frame2.shape)

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    #used to get a bi-level (binary) image out of a grayscale image 

    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 900:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)
        
        i=1
        for i in range(0,1):
                server = smtplib.SMTP("smtp.gmail.com",587)
                server.starttls()
                server.login('sender_gmail_id',config.EMAIL_PASSWORD)
                server.sendmail('sender_gmail_id',"reciever_gmail_id","Alert!! their is an intruder in your house")
                server.quit()
                print("Email Sent")
          
    #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    image = cv2.resize(frame1, (1920,1080))
    out.write(image)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
out.release()
