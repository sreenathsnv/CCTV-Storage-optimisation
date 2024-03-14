import datetime
import cv2
import winsound
import time
import os

def cam_Model():
    current_date = datetime.date.today()

    # Format the current date as "dd-mm-yyyy"
    formatted_date = current_date.strftime("%d-%m-%Y")
    save_folder = f"./recordings/recordings{time.strftime('%d-%m-%Y')}"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    cam = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = None
    start_time = None
    recording = False
    motion_detected = False

    while cam.isOpened():
        ret, frame1 = cam.read()
        ret, frame2 = cam.read()
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_detected = False
        
        for c in contours:
            if cv2.contourArea(c) < 5000:
                continue
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            motion_detected = True
            
            if not recording:
                recording = True
                start_time = time.time()
                out = cv2.VideoWriter(os.path.join(save_folder, f'record_{start_time}.avi'), fourcc, 20.0, (frame1.shape[1], frame1.shape[0]))
        
        if recording:
            out.write(frame1)
        
        if recording and time.time() - start_time > 10 and not motion_detected:
            out.release()
            recording = False
        
        if cv2.waitKey(10) == ord('q'):
            break
        
        cv2.imshow('CCTV oncapturing...', frame1)

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "main":
    cam_Model()