import cv2
import subprocess
import time
import datetime
from datetime import datetime
from telnetlib import Telnet
import Template_list
import Config
import utils

#This test measures how long it takes to reboot the device.
#Steps:
# 1. Define a list to store the results.
# 2. Connect via telnet
# 3. Reboot the device
# 4. Start measuring time
# 5. Check the rebooting via serial
# 6. Detect the user choosing template
# 7. Check the end of reboot via serial
# 8. Stop measuring time
# 9. Add the result to the list

T1T = []

###TEST 1: REBOOT DURATION###

def RebootPerformance():

    for a in range (1, 2):

        tn =Telnet(Config.IP)
        time.sleep(0.5)
        tn.write(b'root\n')
        time.sleep(0.5)
        tn.write('reboot'.encode() + b'\r\n')

        while True:
            response = Config.ser.readlines()
            file = open("tmp_rebootT.txt", "w")
            file.write(str(response))
            with open("tmp_rebootT.txt", "r") as file:
                content = file.read()
                if 'CPU 0123' in content:
                    start_time = datetime.now()
                    print('rebooting...')
                    break

        time.sleep(30)

        image = cv2.VideoCapture(Config.HDMI)                                            ####/dev/videoX
        image.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        image.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        temp_w, temp_h = Template_list.epg_user_template.shape[::-1]

        while True:

            ret, frame = image.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            result = cv2.matchTemplate(gray, Template_list.epg_user_template, cv2.TM_CCOEFF_NORMED)

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            top_left = max_loc

            bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)

            detected = cv2.rectangle(gray, top_left, bottom_right, (255,0,0), 2)

            if max_val > 0.96:
                end_time = datetime.now()
                print("T1:", '{}'.format(end_time - start_time))
                T1T.append((utils.no, (end_time - start_time).total_seconds()))
                break
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

        image.release()
        cv2.waitKey(0)

        time.sleep(5)

        while True:
            response = Config.ser.readlines()
            file = open("tmp_rebootT.txt", "w")
            file.write(str(response))
            with open("tmp_rebootT.txt", "r") as file:
                content = file.read()
                if ' ' in content:
                    break

        cv2.destroyAllWindows()

        time.sleep(3)

        subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
        time.sleep(5)

    cv2.destroyAllWindows()












