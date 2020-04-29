import os


def profile_record_on():
    os.system("callgrind_control --zero > /dev/null")
    os.system("callgrind_control --instr=on > /dev/null")


def profile_record_off(rec_file):
    os.system("callgrind_control -s > " + rec_file )
    os.system("callgrind_control --instr=off > /dev/null")
