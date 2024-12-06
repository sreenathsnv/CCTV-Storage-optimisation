import tkinter as tk
import winsound  
import datetime
import cv2
import time
import os
import threading
import requests
from tkinter import messagebox
from combine import combine_videos,create_folder
from io import BytesIO
import torch
import time
import os

class Connect:
    camera_connected = False
    stop_camera = False
    CONNECT_URL = None
    root = None
    def __init__(self,token) -> None:
        self.root = tk.Tk()
        self.root.title("connecting")

        self.set_token(token)
        print(self.CONNECT_URL)
        self.root.configure(bg="#DDE5F4")


        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()


        x = (screen_width // 2) - (300 // 2) 
        y = (screen_height // 2) - (200 // 2) 


        self.root.geometry('300x200+{}+{}'.format(x, y))


        heading_label = tk.Label(self.root, text="START SURVEILLANCE....................", font=("Helvetica", 16), bg="#DDE5F4")
        heading_label.pack(pady=20)


        connect_button = tk.Button(self.root, text="Connect", command=self.connect, font=("Helvetica", 12), bg="#e0ccff", width=15, height=2)
        connect_button.place(relx=0.3, rely=0.5, anchor=tk.CENTER)


        close_button = tk.Button(self.root, text="Close", command=self.close_window, font=("Helvetica", 12), bg="#ffcccc", width=15, height=2)
        close_button.place(relx=0.7, rely=0.5, anchor=tk.CENTER)




        self.root.mainloop()

    def set_token(self,token):
        
        self.CONNECT_URL = token

    def connect(self):
        
        if not self.camera_connected:
            winsound.PlaySound("./alert.wav", winsound.SND_FILENAME)
            threading.Thread(target=self.cam_Model).start()
            self.camera_connected = True
            print("Connecting...")  # Placeholder action when the button is clicked

    def close_window(self):
        
        if self.camera_connected:
            self.stop_camera_model()
            self.camera_connected = False
            print("Stopping camera model...")
        
        self.upload_sequence()
        self.root.destroy()  # Close the Tkinter window

    def cam_Model(self):
        current_date = datetime.date.today()

        # Format the current date as "dd-mm-yyyy"
        formatted_date = current_date.strftime("%d-%m-%Y")
        save_folder = f'./recordings/recordings{formatted_date}'
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Load YOLOv5 model (pre-trained on COCO dataset)
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

        cam = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = None
        start_time = None
        recording = False
        motion_detected = False

        while cam.isOpened():
            if self.stop_camera:
                break

            ret, frame1 = cam.read()
            ret, frame2 = cam.read()

            # Motion Detection Logic
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

            # Object Detection Logic using YOLOv5
            results = model(frame1)
            for *xyxy, conf, cls in results.xyxy[0]:  # Bounding boxes, confidence, and class index
                x1, y1, x2, y2 = map(int, xyxy)  # Convert to integers
                label = f"{model.names[int(cls)]} {conf:.2f}"  # Class name and confidence
                cv2.rectangle(frame1, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Draw bounding box
                cv2.putText(frame1, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            if recording:
                out.write(frame1)

            if recording and time.time() - start_time > 10 and not motion_detected:
                out.release()
                recording = False

            if cv2.waitKey(10) == ord('q'):
                break

            cv2.imshow('CCTV with Object and Motion Detection', frame1)

        cam.release()
        cv2.destroyAllWindows()

    def stop_camera_model(self):
        
        self.stop_camera = True

    def upload_sequence(self):
        print("upload started")
        FOLDER_PATH = f"./recordings/recordings{datetime.datetime.now().strftime('%d-%m-%Y')}"

        create_folder(f"./outputs/output{datetime.datetime.now().strftime('%d-%m-%Y')}")

        OUTPUT_PATH = f"./outputs/output{datetime.datetime.now().strftime('%d-%m-%Y')}/output_combined_video{datetime.datetime.now().strftime('%d-%m-%Y')}.MP4"

        print("combined started")
        combine_videos(FOLDER_PATH, OUTPUT_PATH)
        print("video combined")
        print(OUTPUT_PATH)

        try:
            with open(OUTPUT_PATH, "rb") as file:
                url = "http://127.0.0.1:8000/api/upload/"

                payload = {}
                files = {
                    'footage': open(OUTPUT_PATH, 'rb')
                }
                headers = {
                    'Authorization': 'Token ' + self.CONNECT_URL
                }

                response_data = requests.request("POST", url, headers=headers, data=payload, files=files)
                response_code = response_data.status_code
                if response_code == 201:
                    print("File uploaded successfully.")
                    messagebox.showinfo("Prompt", "File uploaded successfully.")
                else:
                    print("Failed to upload file:", response_data)
                    messagebox.showinfo("Prompt", "Failed to upload file")

        except Exception as e:
            print(f"Error occurred: {e}")
            messagebox.showinfo("Prompt", f"Error occurred: {e}")

# Close curl connection
