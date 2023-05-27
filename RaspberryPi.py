import time,random
import requests
import json
import math
import smbus2
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

db = "https://foureeestudents-default-rtdb.firebaseio.com/"
keyfile = "foureeestudents-firebase-adminsdk-ilz08-652f7ffde1.json"

scopes = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/firebase.database"
]

credentials = service_account.Credentials.from_service_account_file(keyfile,scopes=scopes)

authed_session = AuthorizedSession(credentials)



# Configuration algorithm
R0 = 0.75
t_wait = 0.5 # wait after peak detected
goal_freq = 3 # Hz, 180steps/mins best athelet
t = 0.33 # s
t_contact = 2

battery_life = 100 # s, this should be read from battery
Enable = 1
Disable = 0


# Sensor Status configuration
# temperature_sensor_status = enable
# temperature_sensor_status = Enable
# Pressure_sensor = Enable

force_threshold = 3
auto_quit_time = 3
 
stand_detect_time = 1
tem_reach_time = 0
reach_index = 0

pace_index_total = 0
force_index_total = 0
weight_force_index_total = 0

percent_total = 0
bar_weight = 6


temp_threshold = 30

n = 0
quit = 0
start = False

# Configuration adc reading
n = 0
start_notice = [0]
Result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
DayReport = [0, 0, 0, 0, 0, 0, 0, 0]
Weight_result = [0, 0]
Weight_report = [0, 0, 0, 0]


SENSOR_L_ADDR = 0x48
SENSOR_R_ADDR = 0x49

si7021_ADD = 0x40
si7021_READ_TEMPERATURE = 0xE3

L_bus = smbus2.SMBus(1)
R_bus = smbus2.SMBus(1)
Temp_bus = smbus2.SMBus(1)

L_cmd_meas_pres = smbus2.i2c_msg.write(0x48, [0x01, 0x42,0x83])
L_cmd_read_res = smbus2.i2c_msg.write(0x48, [0x00])
L_read_result = smbus2.i2c_msg.read(0x48,2)

R_cmd_meas_pres = smbus2.i2c_msg.write(0x49, [0x01, 0x42,0x83])
R_cmd_read_res = smbus2.i2c_msg.write(0x49, [0x00])
R_read_result = smbus2.i2c_msg.read(0x49,2)

L_bus.i2c_rdwr(L_cmd_meas_pres)
L_bus.i2c_rdwr(L_cmd_meas_pres)

R_bus.i2c_rdwr(R_cmd_meas_pres)
R_bus.i2c_rdwr(R_cmd_meas_pres)

# Sensor related code
def get_temp():
    #Set up a write transaction that sends the command to measure temperature
    cmd_meas_temp = smbus2.i2c_msg.write(si7021_ADD,[si7021_READ_TEMPERATURE])

    #Set up a read transaction that reads two bytes of data
    read_result = smbus2.i2c_msg.read(si7021_ADD,2)
    Temp_bus.i2c_rdwr(cmd_meas_temp)
    time.sleep(0.1)
    Temp_bus.i2c_rdwr(read_result)

    #convert the result to an int
    temperature = int.from_bytes(read_result.buf[0]+read_result.buf[1],'big')
    temp = temperature*175.72/65536 - 46.85
    return temp

def check_temp(reach_index):
    current_temp = get_temp() 
    if current_temp < temp_threshold and reach_index == 0:
        tem_reach_time = 0
        return current_temp, time.time(), tem_reach_time,0
    elif current_temp >= temp_threshold and reach_index == 0:
        tem_reach_time = time.time()
        return current_temp, tem_reach_time, round(tem_reach_time),1
    if reach_index == 1 :
        return current_temp, time.time(), round(tem_reach_time),1

def mass_conv(adc_value) :
    voltage = (adc_value-21) * 2.62 / (26453.0-21.0)
    r_inv = voltage / (2.62*R0 - R0*voltage)
    # m = (r_inv - 0.15) / (2.25 * 0.0001)
    m_g = r_inv / (2.4 * 0.0001)
    if m_g <= 0 :
        m_kg = 0
    elif m_g > 0:
        m_kg = round(m_g * 0.001,2)
    return m_kg

def getLValue() :
    time.sleep(0.05)
    L_bus.i2c_rdwr(L_cmd_read_res, L_read_result)
    L_adc_value = int.from_bytes(L_read_result.buf[0]+L_read_result.buf[1],'big')
    return mass_conv(L_adc_value)

def getRValue() :
    time.sleep(0.05)
    R_bus.i2c_rdwr(R_cmd_read_res, R_read_result)
    R_adc_value = int.from_bytes(R_read_result.buf[0]+R_read_result.buf[1],'big')
    return mass_conv(R_adc_value)


# Detectors
def peak_detect(previous_val, Index):

    peak_value = previous_val
    t = time.time()
    test_start = time.time()
    print("test start time = ", test_start)
    test_time = 0

    if Index == 0 : #Left
        new_val = getLValue()
        # print ("---Wait---")
    elif Index == 1: #Right
        new_val = getRValue()
        # print ("---Wait---")
    
    # 只要有压力就持续监测,并筛选出最大值
    # 如果时间太长就自动停止, 进入站立检测
    while new_val > force_threshold and test_time < 1:
        # print("peak detection start")

        if peak_value < new_val : 
            peak_value = new_val
            # print(" --- new --- ")
            t = time.time()
            # print ("new = ", peak_value)
        elif peak_value > new_val :
            # if previous_val - new_val > ErrorSignalThreshold : #expect a gradual
            #     return "error", time.time()
            # print("time = ", round(t,2))
            # print ("remain", new_val)
            pass
        elif peak_value == new_val :
            peak_value = new_val
            t = time.time()
            # print("-same-", new_val)

        if Index == 0 : #Left
            new_val = getLValue()
            # print ("---Wait---")
        elif Index == 1: #Right
            new_val = getRValue()
            # print ("---Wait---")
        
        test_time = time.time() - test_start
        # print("test time = ", test_time)

    # print("peak =", peak_value)
    return peak_value, round(t,2)


def stand_detect():
    detect_start = time.time()
    detect_time = 0
    #print("stand detect start")
    #time.sleep(2)
    while detect_time < stand_detect_time :
        if getLValue() < force_threshold or getRValue() < force_threshold :
            return False
        detect_time = time.time()-detect_start
    #print("---- stand detected -----", detect_time)
    return True

def running_start_detect() :
    while getLValue() > force_threshold and getRValue() > force_threshold :
        pass
    pass

def user_input():
    path="level1.json"
    response = requests.get(db+path)
    if response.ok:
        return response.json()
    else:
        raise ConnectionError("Could not access database:{}".format(response.text))
        pass

def weight_on_detect(initial_left, initial_right):
    current_left = getLValue()
    current_right = getRValue()
    dif_left = current_left - initial_left
    dif_right = current_right - initial_right
    if dif_left > bar_weight and dif_right > bar_weight :
        load = dif_left + dif_right
        return load, True
    else :
        return 0, False


# User Interface
def pace_advice(freq) :
    if freq < 1:
        return "Frequency too high, get exausted quickly", 1
    elif freq < 10 and freq > 1:
        return "Perfect frequency, keep going", 0
    elif freq > 10:
        return "Frequency too low, need to improve", -1

def force_advice(percent) :
    if percent > 0.5 : 
        return "Right foot too much force", 1
    elif percent < 0.5 :
        return "Left foot too much force", -1
    elif percent == 0.5 :
        return "Perfect", 0

def pace_advice_summary(index) :
    if index < 5 and index > -5 :
        return "Pace balance"
    if index > 5 :
        return "Pace overall too high"
    if index < -5 :
        return "Pace overall too low"

def force_advice_summary(index) :
    if index < 5 and index > -5 :
        return "Force balance"
    if index > 5 :
        return "Force overall on right foot"
    if index < -5 :
        return "Force overall on left foot"

def blood_circulation_report(reachtime) :
    if reachtime < 5 :
        return "Good blood circulation"
    if reachtime > 5 :
        return "Poor blood circulation"
    if reachtime == 0:
        return "Not reach. Blood Circulation Warning!"

def result_generation(peak_L,peak_R, t1, t2) :         
    force_percent = peak_R/(peak_R + peak_L)
    t_dif = t2-t1
    f_step = 1/t_dif
    
    Result[0] = peak_L
    Result[1] = peak_R
    Result[2] = round(f_step,2)
    Result[3] = round(force_percent*100,2) # right percent
    Result[4] = round((1-force_percent)*100,2) # left percent
    Result[5],pace_index = pace_advice(f_step)
    Result[6],force_index = force_advice (force_percent)

    global reach_index

    Result7, Result8, Result9,reach_index = check_temp(reach_index)
    time = Result8 - start_time
    Result[7]=round(Result7,2)
    Result[8]=round(time,2)
    Result[9]=Result9

    path = "postlist.json"
    data = {"Left":Result[0], "Right":Result[1], "Frequency":Result[2], "Right_Percentage":Result[3],"Left_Percentage":Result[4],"Pace_Advice":Result[5],"Force_Advice":Result[6],"temperature":Result[7],"time":Result[8],"ideal_temperature_reach_time":Result[9]}

    print("Writing {} to {}".format(data, path))
    response = authed_session.post(db+path, json=data)

    if response.ok:
        print("Created new node named {}".format(response.json()["name"]))
    else:
        raise ConnectionError("Could not write to database: {}".format(response.text))
    #time.sleep(0.1) 

    return Result, pace_index, force_index, force_percent

def report_generation(starttime) :
    print("num_step",num_step)
    print("Report Generation in PROGRESS")
    average_percent = percent_total/num_step
    total_time_taken = time.time() - starttime
    global reach_index
    current_temp, time1, tem_reach_time,reach_index = check_temp(reach_index)

    DayReport[0] = pace_advice_summary(pace_index_total)
    DayReport[1] = num_step
    DayReport[2] = force_advice_summary(force_index_total)
    DayReport[3] = round(average_percent*100,2) # right percent
    DayReport[4] = round((1-average_percent)*100,2) # left percent
    # DayReport[5] = num_stand 
    # this is the number of stand
    # set this as zero as stand is not being tested
    DayReport[5] = 0
    DayReport[6] = round(total_time_taken,2)
    DayReport[7] = blood_circulation_report(tem_reach_time)

    path = "summary.json"
    data = {"Pace summary":DayReport[0], "Number_of steps":DayReport[1], "Force_summary":DayReport[2], "Right_Percentage_ average":DayReport[3],"Left_Percentage_average":DayReport[4],"Number_of_stands":DayReport[5],"Total_time":DayReport[6],"Blood_Circulation":DayReport[7]}

    print("Writing {} to {}".format(data, path))
    response = authed_session.post(db+path, json=data)

    if response.ok:
        print("Created new node named {}".format(response.json()["name"]))
    else:
        raise ConnectionError("Could not write to database: {}".format(response.text))
    #time.sleep(0.1)

    return DayReport

def weight_result_generation():
    left = getLValue()
    right = getRValue()
    if right == 0 or left == 0:
        return
    right_percent = right/(right + left)
    left_percent = 1 - right_percent
    Weight_result[0] = round(right_percent*100, 2)
    Weight_result[1] = round(left_percent*100, 2)

    global weight_force_index_total # need test
    weightAdvice, weight_force_index = force_advice(right_percent)
    weight_force_index_total = weight_force_index_total + weight_force_index

    path = "postlist2.json"
    data = {"Right":Weight_result[0], "Left":Weight_result[1]}

    print("Writing {} to {}".format(data, path))
    response = authed_session.post(db+path, json=data)

    if response.ok:
        print("Created new node named {}".format(response.json()["name"]))
    else:
        raise ConnectionError("Could not write to database: {}".format(response.text))
    #time.sleep(0.1) 

    return

def pause_resume():
    while user_input() == 4:
        if user_input() == 5:
            break
        pass



def weight_report_generation(startTIME, numOfLife) :
    print("Weight Report Generation in PROGRESS")

    Weight_report[0] = load_weight
    Weight_report[1] = time.time()-startTIME
    Weight_report[2] = force_advice_summary(weight_force_index_total) # need test
    Weight_report[3] = numOfLife

    return Weight_report

def quit_procedure():
    print("System Auto Quit after", auto_quit_time, "sec")
    print("press pause or stop")
    
    t_quit_process_start = time.time()
    quit_test_time = 0
    while quit_test_time < auto_quit_time:
        if stand_detect() == True :
            if user_input() == 3:
                return 1
            elif user_input() == 4: #输入是4进入pause_resume
                pause_resume()
                return 0
            quit = 1
            quit_test_time = time.time() - t_quit_process_start
            count_down = round(4 - quit_test_time)
            print(count_down)
        else : 
            print("Running Starts")
            print("Analysis Continues")
            quit = 0
            break
            
        return quit


while 1 :

    num_step = 0
    quit = 0

    print ("Mode Selection Available")

    while 1:
        user = user_input()
        if user == 1 or user == 2: 
            break
        # print("Mode Not Selected")

    print("user: ", user)

    # Force detected, get ready for sports
    while start == False :
        start = stand_detect()

    # Inital infors
    Init_temp, start_time, tem_reach_time,reach_index = check_temp(reach_index)
    print(Init_temp, start_time, tem_reach_time,reach_index)

    # Running Mode
    if user == 1 :
        
        
        print("You can start RUNNING whenever you are ready.")
        print("Analysis will starts automatically")
        print("----------------------------------")

        # Running detection starts
        running_start_detect()
    

        print("Enjoy your Run")

        while 1 :
            print("num_step",num_step)
            force_L = getLValue()
            force_R = getRValue()
            print(force_L, force_R)

            # if receives a valid force from left foot, peak detector starts
            if force_L > force_threshold :
                # error detection is being removed
                peak_L, t1 = peak_detect(force_L,0)
                print("peak_L = ", peak_L)
                num_step = num_step + 1

                while force_R <= force_threshold:
                    force_R = getRValue()
                peak_R, t2 = peak_detect(force_R,1)
                print("peak_R = ", peak_R)
                result,pace_index, force_index, force_percent = result_generation(peak_L,peak_R, t1, t2)
                pace_index_total = pace_index + pace_index_total
                force_index_total = force_index + force_index_total
                percent_total = force_percent + percent_total
                num_step = num_step + 1
                print(Result)
        
                if stand_detect() == True :
                    print("Analysis STOPS.")
                    print("Continue analysis by running")
                    quit = quit_procedure()
                    #time.sleep(2)
                elif stand_detect == False :
                    print("Analysis Continues")
                    quit = 0

            # if receives a valid force from right foot, peak detector starts
            elif force_R > force_threshold :
                peak_R, t1 = peak_detect(force_R,1)
                print("peak_R = ", peak_R)
                num_step = num_step + 1

                while force_L <= force_threshold:
                    force_L = getLValue()
                peak_L, t2 = peak_detect(force_L,0)
                print("peak_L = ", peak_L)

                result,pace_index, force_index, force_percent = result_generation(peak_L,peak_R, t1, t2)
                pace_index_total = pace_index + pace_index_total
                force_index_total = force_index + force_index_total
                percent_total = force_percent + percent_total
                num_step = num_step + 1
                print(Result)

                if stand_detect() == True :
                    print("Analysis STOPS.")
                    print("Continue analysis by running")
                    quit = quit_procedure()
                    time.sleep(2)
                elif stand_detect == False :
                    print("Analysis Continues")
                    quit = 0

            if user_input() == 3:
                quit = 1
            elif user_input() == 4: #输入是4进入pause_resume
                pause_resume()
                quit = 0

            if quit == 1 :
                    print("Analysis Stops")
                    DayReport = report_generation(start_time)
                    print(DayReport)
                    break
                    
    # Weightlifting Mode
    # All you need is one click
    elif user == 2 :
        print("You can start WEIGHTLIFTING whenever you are ready.")
        num_of_lift = 0
        starting_L_mass = getLValue()
        starting_R_mass = getRValue()
        while 1 :
            # detect if the weight is on, do nothing if not on
            load_weight, weight_detector = weight_on_detect(starting_L_mass,starting_R_mass)
            if weight_detector == True :
                print("Weight detected")
                # wait after minor adjustments
                # start analysis
                while weight_detector == True :
                    weight_result_generation()
                    load_weight, weight_detector = weight_on_detect(starting_L_mass,starting_R_mass)
                    pass
                num_of_lift = num_of_lift + 1
                print("Weight-lifting STOP.")
            
            if user_input() == 3 :
                break

        print("Number of lifes", num_of_lift)
        print("Session Ends")
        report = weight_report_generation(start_time, num_of_lift)
        print(report)

    print("THE END")

    while 1 :
        user = user_input() 
        if user == 3:
            break

