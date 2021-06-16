#!/usr/bin/python3

import os
import psutil
import platform
import getpass
import socket
import cpuinfo
import subprocess
# import tensorflow as tf
import distro
import re

def conv(bytes, suffix="B"):
    fact = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < fact:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= fact

inf = platform.uname()
mem = psutil.virtual_memory()
frq = psutil.cpu_freq()
tempentry = 0

TERM_NAMES = {
    'hyper': 'Hyper Terminal',
    'gnome-terminal': 'GNOME Terminal',
    'urxvt': 'urxvt',
    'kitty': 'kitty',
    'nvim': 'Neovim Terminal',
    'NeoVimServer': 'VimR Terminal',
    'vscode': 'VSCode',
}

os.system("clear")
temps = psutil.sensors_temperatures()
for name, entries in temps.items():
        # print(name)
        # for entry in entries:
        #     print("Current temperature: %s °C" % (entry.current))
        if name == "coretemp":
            for entry in entries:
                tempentry = entry.current + tempentry
                # print("Current core temperature: %s °C" % (entry.current))
            tempentry = tempentry/len(entries)
            # print("Average core temperature: %s °C" % tempentry)

fans = psutil.sensors_fans()
names = set(list(fans.keys()))
battery = psutil.sensors_battery()

# def get_distro():
#     with open("/etc/os-release") as i:
#         return i.read().split("\"")[1]
# linuxdistro = get_distro()

def get_issue():
    with open("/etc/issue") as i:
        return i.read().split("\\")[0]
issue = get_issue()

# def get_distro(removeLinux = False):
#     linuxdistro = distro.linux_distribution()[0]
#     if removeLinux:
#         linuxdistro = re.sub(linuxdistro, flags=re.IGNORECASE)
#     linuxdistro = linuxdistro.rstrip()
#     return linuxdistro

# lindistro = get_distro()

# def get_distro_ver(removeLinux = False):
#     distrover = distro.linux_distribution()[1]
#     if removeLinux:
#         distrover = re.sub(distrover, flags=re.IGNORECASE)
#     distrover = distrover.rstrip()
#     return distrover

# lindistrover = get_distro_ver()

def get_uptime():
    with open('/proc/uptime') as i:
        uptime_sec = float(i.readline().split()[0])
        hrs = uptime_sec / 3600
        min = (hrs - int(hrs)) * 60
        hrs = int(hrs)
        min = int(min)
        string = ''
        if hrs != 0 and min != 0:
            string += str(hrs) + ' hours and '
            string += str(min) + ' minutes'
        elif min != 0 or hrs == 0:
            string += str(min) + ' minutes'
        elif hrs!=0 and min == 0:
            string += str(hrs) + ' hours'
        return string

uptime = get_uptime()

def get_username():
    username = getpass.getuser()
    return username

user = get_username()

def get_host():
    hostname = socket.gethostname()
    return hostname

host = get_host()

def get_shell():
    shell_type = os.environ['SHELL']
    if shell_type == "/usr/bin/zsh":
        return "zsh"
    elif shell_type == "/usr/bin/fish":
        return "fish"
    elif shell_type == "/usr/bin/bash":
        return "bash"

shell = get_shell()

# def get_term():
#     term_type = os.environ['TERM']
#     return term_type

def get_term():
    term = 'Unknown'
    for ppid in psutil.Process().parents():
        name = ppid.name()
        if name in ['screen', 'tmux', 'conmon', 'sshd', os.environ['TERM']]:
            term = name
        for term_name, term_pretty_name in TERM_NAMES.items():
            if term_name in name:
                term = term_pretty_name
    return term


term = get_term()

def get_cpu():
    cpu = cpuinfo.get_cpu_info()
    return cpu['brand_raw']

cpu = get_cpu()

def get_gpu():
    cmd = subprocess.run(['lspci'], capture_output=True)
    stdout = cmd.stdout.decode('ascii')
    for line in stdout.splitlines():
        if '3D' in line:
            if '[' in line:
                return line[line.rfind('[') + 1:line.rfind(']')]
            else:
                return line.split('3D controller: ')[1]

gpu = get_gpu()

# def get_gpu2():
#     cmd = subprocess.run(['lspci'], capture_output=True)
#     stdout = cmd.stdout.decode('ascii')
#     for line in stdout.splitlines():
#         if 'VGA' in line:
#             if '[' in line:
#                 return line[line.rfind('[') + 1:line.rfind(']')]
#             else:
#                 return line.split('VGA compatible controller: ')[1]

# gpu2 = get_gpu2()
 
def timechange(secs):
    mm, ss = divmod(secs,60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)


#print("\033[33;1m=\033[m"*32)
print("  ", f"\033[37;1m• User:            \033[34;1m %s@%s\033[m" % (user, host))
print("  ", f"\033[37;1m• System:           \033[34;1m{inf.system}\033[m")
if inf.system == "Linux":
    print("  ","  ", f"\033[37;1m• Distro:        \033[36;1m{issue}\033[m")
    # print("  ","  ", f"\033[37;1m• Distro:        \033[36;1m%s %s\033[m" %(lindistro, lindistrover))
    print("  ","  ", f"\033[37;1m• Kernel:        \033[36;1m{inf.release}\033[m")
    print("  ","  ", f"\033[37;1m• Architecture:  \033[36;1m{inf.machine}\033[m")
    print("  ","  ", f"\033[37;1m• Shell:         \033[36;1m{shell}\033[m")
    print("  ","  ", f"\033[37;1m• Terminal:      \033[36;1m{term}\033[m")
print("  ","  ", f"\033[37;1m• Uptime:        \033[36;1m{uptime}\033[m")
print("  ", f"\033[37;1m• RAM:              \033[32;1m{conv(mem.used)} / {conv(mem.total)} ({mem.percent}%)\033[m")
print("  ", f"\033[37;1m• CPU Name:         \033[33;1m{cpu}\033[m")
print("  ","  ", f"\033[37;1m• CPU frequency: \033[33;1m{frq.current:.2f}Mhz ({psutil.cpu_count(logical=False)} cores)\033[m")
print("  ","  ", f"\033[37;1m• CPU Temp:      \033[33;1m{tempentry} °C\033[m")
for name in names:
    if name in fans:
        for entry in fans[name]:
            if entry.label == "Processor Fan":
                print("  ","  ", f"\033[37;1m• CPU Fan:      \033[34;1m %s RPM\033[m" % (entry.current))
            # else:
            #     print("  ", f"\033[37;1m• %-16s \033[34;1m %s RPM\033[m" % (entry.label or name, entry.current))
print("  ", f"\033[37;1m• GPU Name:         \033[33;1m{gpu}")
for name in names:
    if name in fans:
        for entry in fans[name]:
            if entry.label == "Video Fan":
                print("  ","  ", f"\033[37;1m• GPU Fan:      \033[34;1m %s RPM\033[m" % (entry.current))

# print("  ", f"\033[37;1m• GPU Name:         \033[33;1m{gpu2}")
if battery:
    print("  ", f"\033[37;1m• Battery:")
    print("  ", "  ", f"\033[37;1m• Charge:        \033[35m%s%%\033[37;1m" % round(battery.percent,2))
    if battery.power_plugged:
        print("  ", "  ", f"\033[37;1m• Status:        %s" % ("\033[35mCharging" if battery.percent < 100 else "\033[32;1mFully Charged\033[m"))
    else:
        print("  ", "  ", f"\033[37;1m• Time left:     \033[35m%s\033[m" % timechange(battery.secsleft))
        print("  ", "  ", f"\033[37;1m• Status:        \033[35mDischarging\033[m")
        print("  ", "  ", f"\033[37;1m• Plugged in:    \033[35mNo\033[m")
