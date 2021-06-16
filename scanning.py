# all modules should be imported using from ... import ...

import triad_openvr

import time
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import calendar

import openvr
from threading import Event

import globals
import scan_controllers
import scan_add_data
import os

# This is main module for googlesheet and scanning

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return len(str_list)+1

# GSpread
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("Vive_to_Google-7fb9e315949a.json", scope)

try:
    client = gspread.authorize(creds)
except:
    print("Internet Connection Error")
    quit()

# CHANGE THE NAME OF SPREADSHEET TO YOUR SPREADSHEET ##########################################
sheet1 = client.open('Vive to Google').worksheet('Scan Point 1')
sheet2 = client.open('Vive to Google').worksheet('Scan Point 2')
# sheet for wires
sheet3 = client.open('Vive to Google').worksheet('Wire')
# sheet for red pieces
sheet5 = client.open('Vive to Google').worksheet('Red Point 1')
sheet4 = client.open('Vive to Google').worksheet('Red Point 2')


#globals.endrow1 = next_available_row(sheet1)
globals.rownumber1 = next_available_row(sheet1)
globals.number1 = globals.rownumber1 - 1
globals.id1 = ("id no." + str(globals.rownumber1 - 1))
globals.lastrow1 = globals.rownumber1 - 1

#globals.endrow2 = next_available_row(sheet2)
globals.rownumber2 = next_available_row(sheet2)
globals.number2 = globals.rownumber2 - 1
globals.id2 = ("id no." + str(globals.rownumber2 - 1))
globals.lastrow2 = globals.rownumber2 - 1

#globals.endrow3 = sheet3.get_all_values()
#globals.rownumber3 = len(globals.endrow3) + 1
globals.rownumber3 = next_available_row(sheet3)
globals.number3 = globals.rownumber3 - 1
globals.id3 = ("id no." + str(globals.rownumber3 - 1))
globals.lastrow3 = globals.rownumber3 - 1

#globals.endrow4 = next_available_row(sheet4)
globals.rownumber4 = next_available_row(sheet4)
globals.number4 = globals.rownumber4 - 1
globals.id4 = ("id no." + str(globals.rownumber4 - 1))
globals.lastrow4 = globals.rownumber4 - 1

#globals.endrow5 = sheet5.get_all_values()
globals.rownumber5 = next_available_row(sheet5)
globals.number5 = globals.rownumber5 - 1
globals.id5 = ("id no." + str(globals.rownumber5 - 1))
globals.lastrow5 = globals.rownumber5 - 1

globals.last_update = 0
globals.scanPiece = "white"


def con_states(c_id, vrsystem):
    result, pControllerState = vrsystem.getControllerState(c_id)
    d = scan_controllers.from_controller_state_to_dict(pControllerState)
    return d


def trigger_time(right_id, vrsystem):
    status_trigger = "short"
    start_time = time.process_time()
    end_time = 0
    d2 = con_states(right_id, vrsystem)
    while d2['trigger'] != 0:
        d2 = con_states(right_id, vrsystem)
        # print("looping inside")
        end_time = time.process_time()
        continue

    time_taken = start_time - end_time
    if abs(time_taken) > 1:
        status_trigger = "long"
    return status_trigger

def scan():
    print("Scan started...")
    #time.sleep(5)
    stoppingSign = globals.stopSign
    if globals.stopSign == "stop":
        exit()

    v = triad_openvr.triad_openvr()
    v.print_discovered_objects()

    if len(sys.argv) == 1:
        interval = 1 / 250
    elif len(sys.argv) == 2:
        interval = 1 / float(sys.argv[1])
    else:
        print("Invalid number of arguments")
        interval = False

    vrsystem = openvr.VRSystem()
    triggerState = 1
    data1 = []
    data2 = []
    data3 = []


    lastupdate = 0
    c_path = os.getcwd()
    # Sound Files names
    c1_r = c_path + "\VSounds\controller1_recorded.mp3"
    c1_d = c_path + "\VSounds\controller1_deleted.mp3"
    c2_r = c_path + "\VSounds\controller2_recorded.mp3"
    c2_d = c_path + "\VSounds\controller2_deleted.mp3"
    w_r = c_path + "\VSounds\pika.mp3"
    w_d = c_path + "\VSounds\pikad.mp3"

    currentPiece = globals.scanPiece

    if interval:
        while(True):
            start = time.time()

            currentPiece = globals.scanPiece
            stoppingSign = globals.stopSign
            if stoppingSign == "stop":
                print("Scan stopped")
                return


            left_id, right_id = scan_controllers.get_controller_ids(vrsystem)


            if left_id != None:
                #con_states(left_id, vrsystem)
                result, pControllerState1 = vrsystem.getControllerState(left_id)
                d1 = scan_controllers.from_controller_state_to_dict(pControllerState1)

            if right_id != None:
                d2 = con_states(right_id, vrsystem)

            # Input into right_id and Sheet
            if right_id != None:
                d2 = con_states(right_id, vrsystem)

                # default triggers
                status_trigger = "short"
                status_side = "right"
                status_button = "trigger"
                add_sheet = sheet2
                data = []

                if d2['trigger'] == 1:

                    if currentPiece == "White Piece":
                        status_trigger = "short"
                        status_side = "right"
                        status_button = "trigger"
                        add_sheet = sheet2

                    if currentPiece == "Red Piece":
                        status_trigger = "long"
                        status_side = "right"
                        status_button = "trigger"
                        add_sheet = sheet4

                    if currentPiece == "Wire":
                        status_trigger = "None"
                        status_side = "right"
                        status_button = "grip_button"
                        add_sheet = sheet3


                    data = scan_add_data.add_data_id(v, status_side)
                    scan_add_data.update_online(data, add_sheet, status_side, status_button, status_trigger, c2_r, vrsystem, right_id)
                    data = []


            # Delete from right_id and Sheet
            if right_id != None and d2['trackpad_pressed']:
                if currentPiece == "White Piece":
                    status_thing = "sample2"
                    if globals.lastrow2> 1:
                        scan_add_data.delete_data_online(sheet2, "White1 Sheet", status_thing, c1_d, vrsystem, right_id)

                if currentPiece == "Wire":
                    status_thing = "wire"
                    if globals.lastrow3> 1:
                        scan_add_data.delete_data_online(sheet3, "Wire Sheet", status_thing, w_d, vrsystem, right_id)

                if currentPiece == "Red Piece":
                    status_thing = "redSample2"
                    if globals.lastrow4 > 1:
                        scan_add_data.delete_data_online(sheet4, "Red1 Sheet", status_thing, w_d, vrsystem, right_id)

            ######################################################################
            # input left_id and Sheet
            #if left_id != None and triggerState == d1['trigger']:
            if left_id != None:
                d1 = con_states(left_id, vrsystem)
                # default triggers
                status_trigger = "short"
                status_side = "left"
                status_button = "trigger"
                add_sheet = sheet1
                data = []

                if d1['trigger'] == 1:

                    if currentPiece == "White Piece":
                        status_trigger = "short"
                        status_side = "left"
                        status_button = "trigger"
                        add_sheet = sheet1

                    if currentPiece == "Red Piece":
                        status_trigger = "long"
                        status_side = "left"
                        status_button = "trigger"
                        add_sheet = sheet5

                    if currentPiece == "Wire":
                        status_trigger = "None"
                        status_side = "left"
                        status_button = "grip_button"
                        add_sheet = sheet3

                    data = scan_add_data.add_data_id(v, status_side)
                    scan_add_data.update_online(data, add_sheet, status_side, status_button, status_trigger, c1_r, vrsystem, left_id )
                    data = []

            # Delete from left_id and Sheet
            if left_id != None and d1['trackpad_pressed']:
                if currentPiece == "White Piece":
                    status_thing = "sample1"
                    if globals.lastrow1 > 1:
                        scan_add_data.delete_data_online(sheet1, "White2 Sheet", status_thing, c1_d, vrsystem, left_id)

                if currentPiece == "Wire":
                    status_thing = "wire"
                    if globals.lastrow3 > 1:
                        scan_add_data.delete_data_online(sheet3, "Wire Sheet", status_thing, w_d, vrsystem, left_id)

                if currentPiece == "Red Piece":
                    status_thing = "redSample1"
                    if globals.lastrow5 > 1:
                        scan_add_data.delete_data_online(sheet5, "Red2 Sheet", status_thing, w_d, vrsystem, left_id)

            Event().wait(interval-(time.time()-start))

if __name__ == "__main__":
    globals.global_initialize()
    scan()