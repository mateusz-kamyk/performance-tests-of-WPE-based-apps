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
# 2. Search "ATM" video
# 3. Detect the video icon template
# 4. Click OK to open the video preview
# 5. Start measuring time
# 6. Detect the video preview template
# 7. Stop measuring time
# 8. Add the result to the list

T7T = []

def ATM_video_searching():
    #Go to 'Search' tab, type and navigate to "ATM"
    subprocess.run(["irsend", "SEND_ONCE", "KEY_LEFT-1"])
    time.sleep(5)
    subprocess.run(["irsend", "SEND_ONCE", "KEY_UP-1"])
    time.sleep(3)
    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
    time.sleep(8)
    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
    time.sleep(2)
    for _ in range(0, 3):
        subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
        time.sleep(1.5)
    subprocess.run(["irsend", "SEND_ONCE", "KEY_RIGHT-1"])
    time.sleep(1.5)
    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
    time.sleep(2)
    subprocess.run(["irsend", "SEND_ONCE", "KEY_LEFT-1"])
    time.sleep(1.5)
    subprocess.run(["irsend", "SEND_ONCE", "KEY_UP-1"])
    time.sleep(1.5)
    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
    time.sleep(7)
    for _ in range(0, 6):    
        subprocess.run(["irsend", "SEND_ONCE", "KEY_RIGHT-1"])
        time.sleep(2)
    
def App2_video_preview():
        
        n=0
        for r in range(1,11):

            ATM_video_searching()

            image = cv2.VideoCapture(Config.HDMI)                                  ####/dev/videoX
            image.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            image.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            temp_w, temp_h = Template_list.App2_video_ATM_poster_template.shape[::-1]

            loop_time_end = (datetime.now() + timedelta(seconds=10))

            while True:
                ret, frame = image.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                result = cv2.matchTemplate(gray, Template_list.App2_video_ATM_poster_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                top_left = max_loc
                bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)
                detected = cv2.rectangle(gray, top_left, bottom_right, (255,0,0), 2)

                if max_val > 0.95:
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
                    start_time = datetime.now()
                    break
                
                elif datetime.now() > loop_time_end:
                    print("'ATM' poster not found")
                    for _ in range(0, 2):    
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

            temp_w, temp_h = Template_list.App2_Audio_icon_video_preview_template.shape[::-1]

            loop_time_end = (datetime.now() + timedelta(seconds=30))

            while True:

                ret, frame = image.read()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                result = cv2.matchTemplate(gray, Template_list.App2_Audio_icon_video_preview_template, cv2.TM_CCOEFF_NORMED)

                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                top_left = max_loc

                bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)

                detected = cv2.rectangle(gray, top_left, bottom_right, (255,0,0), 2)

        
                if max_val > 0.95:
                    end_time = datetime.now()
                    print('T7T', '{}'.format(end_time - start_time))
                    T7T.append((utils.no, (end_time - start_time).total_seconds()))
                    n=1
                    break
                elif datetime.now() > loop_time_end:
                    end_time = datetime.now()
                    print('T7T', 'Time exceeded - unsuccessful test')
                    cv2.destroyAllWindows()
                    App_launching.App2()
                    time.sleep(25)
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
                    time.sleep(10)
                    break
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break

            image.release()
            cv2.waitKey(0)

            cv2.destroyAllWindows()

            if n==1:
                break
            

        cv2.destroyAllWindows()


