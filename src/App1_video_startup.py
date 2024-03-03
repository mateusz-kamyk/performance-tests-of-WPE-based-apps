import cv2
import subprocess
import time
import datetime
from datetime import datetime, timedelta
import Template_list
import Config
import App_launching
import App1_video_preview_opening_time
import utils

#This test measures how long it takes to start playing video.
#Steps:
# 1. Define a list to store the results.
# 2. Detect the video icon template (1st episode)
# 3. Click OK to start playing video
# 4. Start measuring time
# 5. Detect the video playing tamplate
# 6. Stop measuring time
# 7. Add the result to the list

T4T = []

def App1_video_startup():
        
        n=0
        for r in range(1,11):

            subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
            time.sleep(3)

            image = cv2.VideoCapture(Config.HDMI)                                  ####/dev/videoX
            image.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            image.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            temp_w, temp_h = Template_list.App1_video_1episode_template.shape[::-1]

            loop_time_end = (datetime.now() + timedelta(seconds=10))

            while True:
                ret, frame = image.read()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                result = cv2.matchTemplate(gray, Template_list.App1_video_1episode_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                top_left = max_loc
                bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)
                detected = cv2.rectangle(gray, top_left, bottom_right, (255,0,0), 2)

                if max_val > 0.98:
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
                    start_time = datetime.now()
                    break
                
                elif datetime.now() > loop_time_end:
                    print("'1st episode' icon not found")
                    App_launching.App1()
                    time.sleep(25)
                    App1_video_preview_opening_time.Moonlight_video_searching()
                    time.sleep(5)
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
                    time.sleep(10)
                    break
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break


            image.release()
            cv2.waitKey(0)

            cv2.destroyAllWindows()

            image = cv2.VideoCapture(Config.HDMI)                                  ####/dev/videoX
            image.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            image.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            temp_w, temp_h = Template_list.App1_video_template.shape[::-1]

            loop_time_end = (datetime.now() + timedelta(seconds=30))

            while True:

                ret, frame = image.read()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                result = cv2.matchTemplate(gray, Template_list.App1_video_template, cv2.TM_CCOEFF_NORMED)

                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                top_left = max_loc

                bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)

                detected = cv2.rectangle(gray, top_left, bottom_right, (255,0,0), 2)

        
                if max_val > 0.98:
                    end_time = datetime.now()
                    print('T4T', '{}'.format(end_time - start_time))
                    T4T.append((utils.no, (end_time - start_time).total_seconds()))
                    n=1
                    break
                elif datetime.now() > loop_time_end:
                    end_time = datetime.now()
                    print('T4T', 'Time exceeded - unsuccessful test')
                    break
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break

            image.release()
            cv2.waitKey(0)

            cv2.destroyAllWindows()

            if n==1:
                break
            

        cv2.destroyAllWindows()

