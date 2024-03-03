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
# 1. Define the lists to store the results.
# 2. Click the Home button
# 3. Launch the App2
# 4. Start measuring time
# 5. Detect the App2 start template (user choose)
# 6. Stop measuring time
# 7. Add the result to the B list

T6T =[]

def App2_startup():

    subprocess.run(["irsend", "SEND_ONCE", "KEY_HOME-1"])
    time.sleep(7)

    while True:
            App_launching.App2()
            start_time = datetime.now()
            loop_time_end = (datetime.now() + timedelta(seconds=60))

            image = cv2.VideoCapture(Config.HDMI)                                          ####/dev/videoX
            image.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            image.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            temp_w, temp_h = Template_list.App2_start_template.shape[::-1]


            while True:
                ret, frame = image.read()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                result = cv2.matchTemplate(gray, Template_list.App2_start_template, cv2.TM_CCOEFF_NORMED)

                frame_per_second = image.get(cv2.CAP_PROP_FPS) 
            
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                top_left = max_loc

                bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)

                detected = cv2.rectangle(gray, top_left, bottom_right, (255,0,0), 2)

                if max_val > 0.95:
                    end_time = datetime.now()
                    print('T6T', '{}'.format(end_time - start_time))
                    repeat = 0
                    T6T.append((utils.no, (end_time - start_time).total_seconds()))
                    time.sleep(3)
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
                    time.sleep(7)
                    break
                elif datetime.now() > loop_time_end:
                    end_time = datetime.now()
                    print('T6T', 'unsuccessful test')
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
