import scanning
import globals
import playsound
import time
import calendar
import openvr
import triad_openvr

# This module is for adding and deleting data in memory and online

def add_data_id(v, status_side):
    data = []
    if status_side == "left":
        first_control = "controller_2"
        second_control = "controller_1"
    else:
        first_control = "controller_1"
        second_control = "controller_2"

    try:
        if v.devices[first_control].get_pose_quaternion != None:
            try:
                for each in v.devices[first_control].get_pose_quaternion():
                    data.append("%.4f" % each)

                return data

            except:
                pass
    except:
        if v.devices[second_control].get_pose_quaternion != None:
            try:
                for each in v.devices[second_control].get_pose_quaternion():
                    data.append("%.4f" % each)

                return data

            except:
                pass


def update_online(data, sheet_name, status_side, status_button, status_trigger, sound_file, vrsystem, c_id):
    row_number = None
    i_d = None
    number = None
    last_row = None
    to_print = "None"

    if status_side == "left" and status_button == "trigger" and status_trigger == "short":
        number = globals.number1
        last_row = globals.lastrow1
        row_number = globals.rownumber1
        i_d = globals.id1
        globals.last_update = 0
        to_print = "LEFT, BLOCK"

    if status_side == "left" and status_button == "trigger" and status_trigger == "long":
        number = globals.number5
        last_row = globals.lastrow5
        row_number = globals.rownumber5
        i_d = globals.id5
        globals.last_update = 2
        to_print = "LEFT, RED BLOCK"

    if status_side == "left" and status_button == "grip_button":
        number = globals.number3
        last_row = globals.lastrow3
        row_number = globals.rownumber3
        i_d = globals.id3
        globals.last_update = 1
        to_print = "LEFT, WIRE"

    if status_side == "right" and status_button == "trigger" and status_trigger == "short":
        number = globals.number2
        last_row = globals.lastrow2
        row_number = globals.rownumber2
        i_d = globals.id2
        globals.last_update = 0
        to_print = "RIGHT, BLOCK"

    if status_side == "right" and status_button == "trigger" and status_trigger == "long":
        number = globals.number4
        last_row = globals.lastrow4
        row_number = globals.rownumber4
        i_d = globals.id4
        globals.last_update = 2
        to_print = "RIGHT, RED BLOCK"

    if status_side == "right" and status_button == "grip_button":
        number = globals.number3
        last_row = globals.lastrow3
        row_number = globals.rownumber3
        i_d = globals.id3
        globals.last_update = 1
        to_print = "RIGHT, WIRE"

    if data[0] != "0.0000" and data[1] != "0.0000" and data[2] != "0.0000":
        print(to_print)
        print(data)
        vrsystem.triggerHapticPulse(c_id, 0, 3000)
        playsound.playsound(sound_file)

        ts1 = calendar.timegm(time.gmtime())
        a = time.ctime(ts1)
        r1 = a.split()

        date_stamp = r1[0] + " " + r1[1] + " " + r1[2] + " " + r1[4]
        time_stamp = r1[3]
        try:
            data_final = [number, i_d, date_stamp, time_stamp, data[0], data[1], data[2], data[3], data[4], data[5], data[6]]
            sheet_name.insert_row(data_final, row_number)

            if status_side == "left" and status_button == "trigger" and status_trigger == "short":
                globals.lastrow1 += 1
                globals.rownumber1 += 1
                globals.number1 += 1
                globals.id1 = ("id no." + str(globals.rownumber1 - 1))
                globals.last_update = 0

            if status_side == "left" and status_button == "trigger" and status_trigger == "long":
                globals.lastrow5 += 1
                globals.rownumber5 += 1
                globals.number5 += 1
                globals.id5 = ("id no." + str(globals.rownumber5 - 1))
                globals.last_update = 2

            if status_side == "left" and status_button == "grip_button":
                globals.lastrow3 += 1
                globals.rownumber3 += 1
                globals.number3 += 1
                globals.id3 = ("id no." + str(globals.rownumber3 - 1))
                globals.last_update = 1

            if status_side == "right" and status_button == "trigger" and status_trigger == "short":
                globals.lastrow2 += 1
                globals.rownumber2 += 1
                globals.number2 += 1
                globals.id2 = ("id no." + str(globals.rownumber2 - 1))
                globals.last_update = 0

            if status_side == "right" and status_button == "trigger" and status_trigger == "long":
                globals.lastrow4 += 1
                globals.rownumber4 += 1
                globals.number4 += 1
                globals.id4 = ("id no." + str(globals.rownumber4 - 1))
                globals.last_update = 2

            if status_side == "right" and status_button == "grip_button":
                globals.lastrow3 += 1
                globals.rownumber3 += 1
                globals.number3 += 1
                globals.id3 = ("id no." + str(globals.rownumber3 - 1))
                globals.last_update = 1

            data = []
        except:
            pass
    else:
        data = []


def delete_data_online(sheet, sheet_name, status_thing, sound_file, vrsystem, c_id):
    if status_thing == "sample1":
        sheet.delete_row(globals.lastrow1)
        vrsystem.triggerHapticPulse(c_id, 0, 3000)
        print("Last Row Deleted in " + str(sheet_name))
        playsound.playsound(sound_file)
        globals.lastrow1 -= 1
        globals.rownumber1 -= 1
        globals.id1 = ("id no." + str(globals.rownumber1 - 1))
        globals.number1 -= 1

    if status_thing == "redSample1":
        sheet.delete_row(globals.lastrow5)
        vrsystem.triggerHapticPulse(c_id, 0, 3000)
        print("Last Row Deleted in " + str(sheet_name))
        playsound.playsound(sound_file)
        globals.lastrow5 -= 1
        globals.rownumber5 -= 1
        globals.id5 = ("id no." + str(globals.rownumber5 - 1))
        globals.number5 -= 1

    if status_thing == "sample2":
        sheet.delete_row(globals.lastrow2)
        vrsystem.triggerHapticPulse(c_id, 0, 3000)
        print("Last Row Deleted in " + str(sheet_name))
        playsound.playsound(sound_file)
        globals.lastrow2 -= 1
        globals.rownumber2 -= 1
        globals.id2 = ("id no." + str(globals.rownumber2 - 1))
        globals.number2 -= 1

    if status_thing == "redSample2":
        sheet.delete_row(globals.lastrow4)
        vrsystem.triggerHapticPulse(c_id, 0, 3000)
        print("Last Row Deleted in " + str(sheet_name))
        playsound.playsound(sound_file)
        globals.lastrow4 -= 1
        globals.rownumber4 -= 1
        globals.id4 = ("id no." + str(globals.rownumber4 - 1))
        globals.number4 -= 1

    if status_thing == "wire":
        sheet.delete_row(globals.lastrow3)
        vrsystem.triggerHapticPulse(c_id, 0, 3000)
        print("Last Row Deleted in " + str(sheet_name))
        playsound.playsound(sound_file)
        globals.lastrow3 -= 1
        globals.rownumber3 -= 1
        globals.id3 = ("id no." + str(globals.rownumber3 - 1))
        globals.number3 -= 1
  
if __name__ == "__main__":
    globals.global_initialize()