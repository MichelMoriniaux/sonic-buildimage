#!/usr/bin/python
# On Z9264f, the BaseBoard Management Controller is an
# autonomous subsystem provides monitoring and management
# facility independent of the host CPU. IPMI standard
# protocol is used with ipmitool to fetch sensor details.
# Current script support X00 board only. X01 support will 
# be added soon. This provies support for the
# following objects:
#   * Onboard temperature sensors
#   * FAN trays
#   * PSU


import os
import sys
import logging
import subprocess
import commands

Z9264F_MAX_FAN_TRAYS = 4
Z9264F_MAX_PSUS = 2
IPMI_SENSOR_DATA = "ipmitool sdr list"
IPMI_SENSOR_DUMP = "/tmp/sdr"

FAN_PRESENCE = "FAN{0}_prsnt"
PSU_PRESENCE = "PSU{0}_state"
# Use this for older firmware
# PSU_PRESENCE="PSU{0}_prsnt"

ipmi_sdr_list = ""

# Dump sensor registers


def ipmi_sensor_dump():

    status = 1
    global ipmi_sdr_list
    ipmi_cmd = IPMI_SENSOR_DATA
    status, ipmi_sdr_list = commands.getstatusoutput(ipmi_cmd)

    if status:
        logging.error('Failed to execute:' + ipmi_sdr_list)
        sys.exit(0)

# Fetch a BMC register


def get_pmc_register(reg_name):

    for item in ipmi_sdr_list.split("\n"):
        if reg_name in item:
            output = item.strip()

    if not output:
        print('\nFailed to fetch: ' +  reg_name + ' sensor ')
        sys.exit(0)

    output = output.split('|')[1]

    logging.basicConfig(level=logging.DEBUG)
    return output


# Print the information for temperature sensors


def print_temperature_sensors():

    print("\nOnboard Temperature Sensors:")

    print '  PT_Left_temp:                   ',\
        (get_pmc_register('PT_Left_temp'))
    print '  PT_Mid_temp:                    ',\
        (get_pmc_register('PT_Mid_temp'))
    print '  PT_Right_temp:                  ',\
        (get_pmc_register('PT_Right_temp'))
    print '  Broadcom Temp:                  ',\
        (get_pmc_register('TC_Near_temp'))
    print '  Inlet Airflow Temp:             ',\
        (get_pmc_register('ILET_AF_temp'))
    print '  CPU Temp:                       ',\
        (get_pmc_register('CPU_Near_temp'))
    print '  CPU Near Temp:                  ',\
        (get_pmc_register('CPU_temp'))
    print '  DRAM Temp:                      ',\
        (get_pmc_register('DRAM1_temp'))

ipmi_sensor_dump()

print_temperature_sensors()

# Print the information for 1 Fan Tray


def print_fan_tray(tray):

    Fan_Status = [' Normal', ' Abnormal']
    Airflow_Direction = ['B2F', 'F2B']

    print '  Fan Tray ' + str(tray) + ':'

    if (tray == 1):

        fan1_status = int(get_pmc_register('Fan1_Front_state'), 16)
        fan2_status = int(get_pmc_register('Fan1_Rear_state'), 16)

        print '    Fan1 Speed:                   ',\
            get_pmc_register('FAN1_Front_rpm')
        print '    Fan2 Speed:                   ',\
            get_pmc_register('FAN1_Rear_rpm')
        print '    Fan1 State:                   ',\
            Fan_Status[fan1_status]
        print '    Fan2 State:                   ',\
            Fan_Status[fan2_status]

    elif (tray == 2):

        fan1_status = int(get_pmc_register('Fan2_Front_state'), 16)
        fan2_status = int(get_pmc_register('Fan2_Rear_state'), 16)

        print '    Fan1 Speed:                   ',\
            get_pmc_register('FAN2_Front_rpm')
        print '    Fan2 Speed:                   ',\
            get_pmc_register('FAN2_Rear_rpm')
        print '    Fan1 State:                   ',\
            Fan_Status[fan1_status]
        print '    Fan2 State:                   ',\
            Fan_Status[fan2_status]

    elif (tray == 3):

        fan1_status = int(get_pmc_register('Fan3_Front_state'), 16)
        fan2_status = int(get_pmc_register('Fan3_Rear_state'), 16)

        print '    Fan1 Speed:                   ',\
            get_pmc_register('FAN3_Front_rpm')
        print '    Fan2 Speed:                   ',\
            get_pmc_register('FAN3_Rear_rpm')
        print '    Fan1 State:                   ',\
            Fan_Status[fan1_status]
        print '    Fan2 State:                   ',\
            Fan_Status[fan2_status]

    elif (tray == 4):

        fan1_status = int(get_pmc_register('Fan4_Front_state'), 16)
        fan2_status = int(get_pmc_register('Fan4_Rear_state'), 16)

        print '    Fan1 Speed:                   ',\
            get_pmc_register('FAN4_Front_rpm')
        print '    Fan2 Speed:                   ',\
            get_pmc_register('FAN4_Rear_rpm')
        print '    Fan1 State:                   ',\
            Fan_Status[fan1_status]
        print '    Fan2 State:                   ',\
            Fan_Status[fan2_status]


print('\nFan Trays:')

for tray in range(1, Z9264F_MAX_FAN_TRAYS + 1):
    fan_presence = FAN_PRESENCE.format(tray)
    if (get_pmc_register(fan_presence)):
        print_fan_tray(tray)
    else:
        print '\n  Fan Tray ' + str(tray + 1) + ':     Not present'


# Print the information for PSU1, PSU2
def print_psu(psu):
    Psu_Type = ['Normal', 'Mismatch']
    Psu_Input_Type = ['AC', 'DC']
    PSU_STATUS_TYPE_BIT = 4
    PSU_STATUS_INPUT_TYPE_BIT = 1
    PSU_FAN_PRESENT_BIT = 2
    PSU_FAN_STATUS_BIT = 1
    PSU_FAN_AIR_FLOW_BIT = 0
    Psu_Fan_Presence = ['Present', 'Absent']
    Psu_Fan_Status = ['Normal', 'Abnormal']
    Psu_Fan_Airflow = ['B2F', 'F2B']

    # print '    Input:          ', Psu_Input_Type[psu_input_type]
    # print '    Type:           ', Psu_Type[psu_type]

    # PSU FAN details
    if (psu == 1):

        # psu1_fan_status = int(get_pmc_register('PSU1_status'),16)

        print '    PSU1:'
        print '       FAN Temperature:              ',\
            get_pmc_register('PSU1_temp')
        print '       FAN AirFlow Temperature:      ',\
            get_pmc_register('PSU1_AF_temp')
        print '       FAN RPM:                      ',\
            get_pmc_register('PSU1_rpm')
        # print '    FAN Status:      ', Psu_Fan_Status[psu1_fan_status]

        # PSU input & output monitors
        print '       Input Voltage:                 ',\
            get_pmc_register('PSU1_In_volt')
        print '       Output Voltage:                 ',\
            get_pmc_register('PSU1_Out_volt')
        print '       Input Power:                   ',\
            get_pmc_register('PSU1_In_watt')
        print '       Output Power:                  ',\
            get_pmc_register('PSU1_Out_watt')
        print '       Input Current:                   ',\
            get_pmc_register('PSU1_In_amp')
        print '       Output Current:                 ',\
            get_pmc_register('PSU1_Out_amp')

    else:

        # psu2_fan_status = int(get_pmc_register('PSU1_status'),16)
        print '    PSU2:'
        print '       FAN Temperature:              ',\
            get_pmc_register('PSU2_temp')
        print '       FAN AirFlow Temperature:      ',\
            get_pmc_register('PSU2_AF_temp')
        print '       FAN RPM:                      ',\
            get_pmc_register('PSU2_rpm')
        # print '    FAN Status:      ', Psu_Fan_Status[psu2_fan_status]

        # PSU input & output monitors
        print '       Input Voltage:                 ',\
            get_pmc_register('PSU2_In_volt')
        print '       Output Voltage:                 ',\
            get_pmc_register('PSU2_Out_volt')
        print '       Input Power:                   ',\
            get_pmc_register('PSU2_In_watt')
        print '       Output Power:                  ',\
            get_pmc_register('PSU2_Out_watt')
        print '       Input Current:                   ',\
            get_pmc_register('PSU2_In_amp')
        print '       Output Current:                 ',\
            get_pmc_register('PSU2_Out_amp')


print('\nPSUs:')
for psu in range(1, Z9264F_MAX_PSUS + 1):
    psu_presence = PSU_PRESENCE.format(psu)
    if (get_pmc_register(psu_presence)):
        print_psu(psu)
    else:
        print '\n  PSU ', psu, 'Not present'

print '\n    Total Power:                      ',\
    get_pmc_register('PSU_Total_watt')

