import cv2
import subprocess
import time
import datetime
from datetime import datetime, timedelta
import Template_list
import Config

#Functions for Apps are responsible for startup process:
# 1. Navigation through EPG UI
# 2. Template detection - checking if the app icon has been detected
# 3. If template not detected after 60 sec - trying again


#App1 launching
def App1():

    #Define a variable responsible for repeating the start of the app
    n=0

    #A loop that results in max 10 attempts to start the app
    for r in range(1,11):

        #Close cv window
        cv2.destroyAllWindows()

        #Navigate through EPG UI
        time.sleep(1)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_HOME-1"])
        time.sleep(7)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
        time.sleep(2.5)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
        time.sleep(2.5)

        for _ in range (1, 7):
            subprocess.run(["irsend", "SEND_ONCE", "KEY_RIGHT-1"])
            time.sleep(2)

        #Template detection part
        for _ in range (1, 2):

            #Set up the connected device (STB)
            image = cv2.VideoCapture(Config.HDMI)                                          ####/dev/videoX
            image.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            image.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            #Set template weight and hight using defined template
            temp_w, temp_h = Template_list.App1_EPG_logo_template.shape[::-1]

            #Set 60 sec timing
            loop_time_end = (datetime.now() + timedelta(seconds=6))

            #Template detection process
            while True:

                #Read the image from STB
                ret, frame = image.read()

                #Set the gray color of the frame
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                #Compare image with template using TM_CCOEFF_NORMED method
                result = cv2.matchTemplate(gray, Template_list.App1_EPG_logo_template, cv2.TM_CCOEFF_NORMED)

                #Find the min and max values (positions)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                #The highest value is in left corner (result of using TM_CCOEFF_NORMED method)
                top_left = max_loc

                #Determine the bottom right corner
                bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)

                #Draw rectangle on the most possible area
                detected = cv2.rectangle(gray, top_left, bottom_right, (255,0,0), 2)
                
                #If maximum value > 0.97, then template is detected
                if max_val > 0.97:
                    #Click OK to start the app
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
                    print("App1 launched")
                    #Set the variable to 1 to end the main loop
                    n=1
                    break

                #If template detecting takes more than one minute then leave the EPG
                elif datetime.now() > loop_time_end:
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_BACK-1"])
                    time.sleep(2)
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_BACK-1"])
                    time.sleep(3)
                    break

                #Shut the cv image
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break

            #Release memory    
            image.release()
            cv2.waitKey(0)

            #Close cv windows
            cv2.destroyAllWindows()

        #If detected template, then break the loop
        if n==1:
            break



#App2 launching
def App2():
    n=0
    for r in range(1,11):
        cv2.destroyAllWindows()
        time.sleep(1)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_HOME-1"])
        time.sleep(7)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
        time.sleep(2.5)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
        time.sleep(2.5)

        for _ in range (1, 9):
            subprocess.run(["irsend", "SEND_ONCE", "KEY_RIGHT-1"])
            time.sleep(2)

        for _ in range (1, 2):

            image = cv2.VideoCapture(Config.HDMI)                                          ####/dev/videoX
            image.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            image.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            temp_w, temp_h = Template_list.App2_EPG_logo_template.shape[::-1]

            loop_time_end = (datetime.now() + timedelta(seconds=6))

            while True:

                ret, frame = image.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                result = cv2.matchTemplate(gray, Template_list.App2_EPG_logo_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                top_left = max_loc
                bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)
                detected = cv2.rectangle(gray, top_left, bottom_right, (255,0,0), 2)

                if max_val > 0.97:
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
                    print("App2 launched")
                    n=1
                    break
                elif datetime.now() > loop_time_end:
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_BACK-1"])
                    time.sleep(2)
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_BACK-1"])
                    time.sleep(3)
                    break
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break
                
            image.release()
            cv2.waitKey(0)

            cv2.destroyAllWindows()

        if n==1:
            break



#App3 launching
def App3():
    n=0
    for r in range(1,11):
        cv2.destroyAllWindows()
        time.sleep(1)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_HOME-1"])
        time.sleep(7)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
        time.sleep(2.5)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
        time.sleep(2.5)

        for _ in range (1, 10):
            subprocess.run(["irsend", "SEND_ONCE", "KEY_RIGHT-1"])
            time.sleep(2)

        for _ in range (1, 2):

            image = cv2.VideoCapture(Config.HDMI)                                          ####/dev/videoX
            image.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            image.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            temp_w, temp_h = Template_list.App3_EPG_logo_template.shape[::-1]

            loop_time_end = (datetime.now() + timedelta(seconds=6))

            while True:

                ret, frame = image.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                result = cv2.matchTemplate(gray, Template_list.App3_EPG_logo_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                top_left = max_loc
                bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)
                detected = cv2.rectangle(gray, top_left, bottom_right, (255,0,0), 2)

                if max_val > 0.97:
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
                    print("App3 launched")
                    n=1
                    break
                elif datetime.now() > loop_time_end:
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_BACK-1"])
                    time.sleep(2)
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_BACK-1"])
                    time.sleep(3)
                    break
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break
                
            image.release()
            cv2.waitKey(0)

            cv2.destroyAllWindows()

        if n==1:
            break



#App4 launching
def App4():
    n=0
    for r in range(1,11):
        cv2.destroyAllWindows()
        time.sleep(1)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_HOME-1"])
        time.sleep(7)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
        time.sleep(2.5)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
        time.sleep(2.5)

        for _ in range (1, 11):
            subprocess.run(["irsend", "SEND_ONCE", "KEY_RIGHT-1"])
            time.sleep(2)

        for _ in range (1, 2):

            image = cv2.VideoCapture(Config.HDMI)                                          ####/dev/videoX
            image.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            image.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            temp_w, temp_h = Template_list.App4_EPG_logo_template.shape[::-1]

            loop_time_end = (datetime.now() + timedelta(seconds=6))

            while True:

                ret, frame = image.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                result = cv2.matchTemplate(gray, Template_list.App4_EPG_logo_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                top_left = max_loc
                bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)
                detected = cv2.rectangle(gray, top_left, bottom_right, (255,0,0), 2)

                if max_val > 0.97:
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
                    print("App4 launched")
                    n=1
                    break
                elif datetime.now() > loop_time_end:
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_BACK-1"])
                    time.sleep(2)
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_BACK-1"])
                    time.sleep(3)
                    break
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break
                
            image.release()
            cv2.waitKey(0)

            cv2.destroyAllWindows()

        if n==1:
            break



#App5 launching
def App5():
    n=0
    for r in range(1,11):
        cv2.destroyAllWindows()
        time.sleep(1)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_HOME-1"])
        time.sleep(7)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
        time.sleep(2.5)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
        time.sleep(2.5)

        for _ in range (1, 12):
            subprocess.run(["irsend", "SEND_ONCE", "KEY_RIGHT-1"])
            time.sleep(2)

        for _ in range (1, 2):

            image = cv2.VideoCapture(Config.HDMI)                                          ####/dev/videoX
            image.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            image.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            temp_w, temp_h = Template_list.App5_EPG_logo_template.shape[::-1]

            loop_time_end = (datetime.now() + timedelta(seconds=6))

            while True:

                ret, frame = image.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                result = cv2.matchTemplate(gray, Template_list.App5_EPG_logo_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                top_left = max_loc
                bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)
                detected = cv2.rectangle(gray, top_left, bottom_right, (255,0,0), 2)

                if max_val > 0.97:
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
                    print("App5 launched")
                    n=1
                    break
                elif datetime.now() > loop_time_end:
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_BACK-1"])
                    time.sleep(2)
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_BACK-1"])
                    time.sleep(3)
                    break
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break
                
            image.release()
            cv2.waitKey(0)

            cv2.destroyAllWindows()

        if n==1:
            break

#App6 launching
def App6():
    n=0
    for r in range(1,11):
        cv2.destroyAllWindows()
        time.sleep(1)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_HOME-1"])
        time.sleep(7)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
        time.sleep(2.5)
        subprocess.run(["irsend", "SEND_ONCE", "KEY_DOWN-1"])
        time.sleep(2.5)

        for _ in range (1, 8):
            subprocess.run(["irsend", "SEND_ONCE", "KEY_RIGHT-1"])
            time.sleep(2)

        for _ in range (1, 2):

            image = cv2.VideoCapture(Config.HDMI)                                          ####/dev/videoX
            image.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            image.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            temp_w, temp_h = Template_list.App6_EPG_logo_template.shape[::-1]

            loop_time_end = (datetime.now() + timedelta(seconds=6))

            while True:

                ret, frame = image.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                result = cv2.matchTemplate(gray, Template_list.App6_EPG_logo_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                top_left = max_loc
                bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)
                detected = cv2.rectangle(gray, top_left, bottom_right, (255,0,0), 2)

                if max_val > 0.97:
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_OK-1"])
                    print("App6 launched")
                    n=1
                    break
                elif datetime.now() > loop_time_end:
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_BACK-1"])
                    time.sleep(2)
                    subprocess.run(["irsend", "SEND_ONCE", "KEY_BACK-1"])
                    time.sleep(3)
                    break
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break
                
            image.release()
            cv2.waitKey(0)

            cv2.destroyAllWindows()

        if n==1:
            break

