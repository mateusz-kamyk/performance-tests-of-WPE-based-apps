import cv2
import subprocess
import time
import datetime
from datetime import datetime, timedelta
import Template_list
import Config
import App_launching
import utils

#This test measures how long it takes to open the video preview.
#Steps:
# 1. Define a list to store the results.
# 2. Search "Moonlight" video
# 3. Detect the video icon template
# 4. Click OK to open the video preview
# 5. Start measuring time
# 6. Detect the video preview template
# 7. Stop measuring time
# 8. Add the result to the list

T3T = []

def Moonlight_video_searching():
            #"Moonlight" video searching
            subprocess.run(["irsend", "SEND_ONCE", "KEY_LEFT-1"])
            time.sleep(5)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_UP-1"])
            time.sleep(3)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
            time.sleep(8)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
            time.sleep(4)
            for _ in range(0, 3):
                subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
                time.sleep(1)
            for _ in range(0, 2):    
                subprocess.run(["irsend", "SEND_ONCE", "KEY_RIGHT-1"])
                time.sleep(1)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
            time.sleep(1)
            for _ in range(0, 2):
                subprocess.run(["irsend", "SEND_ONCE", "KEY_UP-1"])
                time.sleep(1)
            for _ in range(0, 2):
                subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
                time.sleep(1)
            for _ in range(0, 2):
                subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
                time.sleep(1)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_LEFT-1"])
            time.sleep(1)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
            time.sleep(1)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_UP-1"])
            time.sleep(1)
            for _ in range(0, 2):    
                subprocess.run(["irsend", "SEND_ONCE", "KEY_RIGHT-1"])
                time.sleep(1)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
            time.sleep(1)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_UP-1"])
            time.sleep(1)
            for _ in range(0, 2):    
                subprocess.run(["irsend", "SEND_ONCE", "KEY_LEFT-1"])
                time.sleep(1)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
            time.sleep(1)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
            time.sleep(1)
            for _ in range(0, 2):    
                subprocess.run(["irsend", "SEND_ONCE", "KEY_LEFT-1"])
                time.sleep(1)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
            time.sleep(1)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_RIGHT-1"])
            time.sleep(1)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
            time.sleep(1)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_UP-1"])
            time.sleep(1)
            for _ in range(0, 2):    
                subprocess.run(["irsend", "SEND_ONCE", "KEY_LEFT-1"])
                time.sleep(1)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
            time.sleep(1)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
            time.sleep(1)
            for _ in range(0, 9):    
                subprocess.run(["irsend", "SEND_ONCE", "KEY_RIGHT-1"])
                time.sleep(1)
            subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
            time.sleep(3)   


def App1_video_preview():
        
        n=0
        for r in range(1,11):

            Moonlight_video_searching()

            image = cv2.VideoCapture(Config.HDMI)                                  ####/dev/videoX
            image.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            image.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            temp_w, temp_h = Template_list.App1_video_moonlight_template.shape[::-1]

            loop_time_end = (datetime.now() + timedelta(seconds=10))

            while True:
                ret, frame = image.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                result = cv2.matchTemplate(gray, Template_list.App1_video_moonlight_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                top_left = max_loc
                bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)
                detected = cv2.rectangle(gray, top_left, bottom_right, (255,0,0), 2)

                if max_val > 0.98:
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
                    start_time = datetime.now()
                    break
                
                elif datetime.now() > loop_time_end:
                    print("'Moonlight' poster not found")
                    for _ in range(0, 3):    
                        subprocess.run(["irsend", "SEND_ONCE", "KEY_BACK-1"])
                        time.sleep(8)
                    break
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break


            image.release()
            cv2.waitKey(0)

            cv2.destroyAllWindows()

            image = cv2.VideoCapture(Config.HDMI)                                  ####/dev/videoX
            image.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            image.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            temp_w, temp_h = Template_list.App1_play_button_video_preview.shape[::-1]

            loop_time_end = (datetime.now() + timedelta(seconds=30))

            while True:

                ret, frame = image.read()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                result = cv2.matchTemplate(gray, Template_list.App1_play_button_video_preview, cv2.TM_CCOEFF_NORMED)

                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                top_left = max_loc

                bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)

                detected = cv2.rectangle(gray, top_left, bottom_right, (255,0,0), 2)

        
                if max_val > 0.98:
                    end_time = datetime.now()
                    print('T3T', '{}'.format(end_time - start_time))
                    T3T.append((utils.no, (end_time - start_time).total_seconds()))
                    n=1
                    break
                elif datetime.now() > loop_time_end:
                    end_time = datetime.now()
                    print('T3T', 'Time exceeded - unsuccessful test')
                    App_launching.App1()
                    time.sleep(25)
                    break
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break

            image.release()
            cv2.waitKey(0)

            cv2.destroyAllWindows()

            if n==1:
                break
            

        cv2.destroyAllWindows()

