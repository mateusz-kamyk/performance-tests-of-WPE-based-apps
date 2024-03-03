import cv2
import subprocess
import time
import datetime
from datetime import datetime, timedelta
import Template_list
import Config
import App_launching
import utils

#This test measures how long it takes to start the app.
#Steps:
# 1. Define the lists A, B to store the results.
# 2. Prelaunch the App1 (start of the WPE)
# 3. Click the Home button
# 4. Launch the App1
# 5. Start measuring time
# 5. Detect the preview image template
# 6. Stop measuring A time
# 7. Add the result to the A list
# 8. Detect the App1 homepage template
# 9. Stop measuring B time
# 10. Add the result to the B list

T2T_A = []
T2T_B = []

def App1_startup():

    App_launching.App1()

    time.sleep(20)
    subprocess.run(["irsend", "SEND_ONCE", "KEY_HOME-1"])
    time.sleep(7)

    while True:
            App_launching.App1()
            start_time = datetime.now()
            
            image = cv2.VideoCapture(Config.HDMI)                                          
            image.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            image.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            temp_w, temp_h = Template_list.App1_start_template.shape[::-1]

            loop_time_end = (datetime.now() + timedelta(seconds=60))
            print('A - Black screen duration (from start to loading icon)')
            print('B - Total start-up time')

            while True:

                ret, frame = image.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                result = cv2.matchTemplate(gray, Template_list.App1_start_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                top_left = max_loc
                bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)
                detected = cv2.rectangle(gray, top_left, bottom_right, (255,0,0), 2)

                if max_val > 0.95:
                    end_time_wpe = datetime.now()
                    print('T2T_A', '{}'.format(end_time_wpe - start_time))
                    T2T_A.append((utils.no, (end_time_wpe - start_time).total_seconds()))
                    break
                elif datetime.now() > loop_time_end:
                    end_time = datetime.now()
                    print('T2T_A', 'unsuccessful test')
                    break
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break
            
            image.release()
            cv2.waitKey(0)

            cv2.destroyAllWindows()

            image = cv2.VideoCapture(Config.HDMI)                                          ####/dev/videoX
            image.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            image.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            temp_w, temp_h = Template_list.App1_homepage_template.shape[::-1]


            while True:
                ret, frame = image.read()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                result = cv2.matchTemplate(gray, Template_list.App1_homepage_template, cv2.TM_CCOEFF_NORMED)

                frame_per_second = image.get(cv2.CAP_PROP_FPS) 
            
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                top_left = max_loc

                bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)

                detected = cv2.rectangle(gray, top_left, bottom_right, (255,0,0), 2)

                if max_val > 0.98:
                    end_time = datetime.now()
                    print('T2T_B', '{}'.format(end_time - start_time))
                    repeat = 0
                    T2T_B.append((utils.no,(end_time - start_time).total_seconds()))
                    break
                elif datetime.now() > loop_time_end:
                    end_time = datetime.now()
                    print('T2T_B', 'unsuccessful test')
                    repeat = 1
                    break
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break

            image.release()
            cv2.waitKey(0)

            cv2.destroyAllWindows()
            if repeat == 0:
                break

    cv2.destroyAllWindows()
