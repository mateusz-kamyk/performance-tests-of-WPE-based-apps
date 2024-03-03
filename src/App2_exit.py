import cv2
import subprocess
import time
import datetime
from datetime import datetime, timedelta
import Template_list
import Config
import App_launching
import utils

#This test measures how long it takes to exit the app.
#Steps:
# 1. Define a list to store the results.
# 2. Navigate to app homepage
# 3. Click the Home button
# 4. Start measuring time
# 5. Detect the EPG template
# 6. Stop measuring time
# 7. Add the result to the list

T10T = []


def App2_exit_time():
        
        for _ in range (0, 4):
            subprocess.run(["irsend", "SEND_ONCE", "KEY_BACK-1"])
            time.sleep(8)
    

        while True:

            image = cv2.VideoCapture(Config.HDMI)                                        ####/dev/videoX
            image.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            image.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            temp_w, temp_h = Template_list.epg_home_template.shape[::-1]

            subprocess.run(["irsend", "SEND_ONCE", "KEY_HOME-1"])

            start_time = datetime.now()

            loop_time_end = (datetime.now() + timedelta(seconds=60))

            while True:

                ret, frame = image.read()
                gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                result = cv2.matchTemplate(gray2, Template_list.epg_home_template, cv2.TM_CCOEFF_NORMED)

                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                top_left = max_loc
                bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)

                detected = cv2.rectangle(gray2, top_left, bottom_right, (255,0,0), 2)
            
                if max_val > 0.98:
                    end_time = datetime.now()
                    print('T10T', '{}'.format(end_time - start_time))
                    repeat = 0
                    T10T.append((utils.no, (end_time - start_time).total_seconds()))
                    break

                elif datetime.now() > loop_time_end:
                    print('T10T', 'Time exceeded - unsuccessful test')
                    repeat = 1
                    App_launching.App2()
                    time.sleep(25)
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
                    time.sleep(15)
                    break                

                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break

            image.release()
            cv2.waitKey(0)

            time.sleep(2)

            cv2.destroyAllWindows()
            if repeat == 0:
                break        

        cv2.destroyAllWindows()