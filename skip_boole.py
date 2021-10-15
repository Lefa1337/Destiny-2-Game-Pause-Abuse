
import pydivert
from threading import Thread
import time
import keyboard  
import winsound
import argparse


#don't touch
drop_in = False
initiate_in = False
total_packets_in = 0
packets_min_in = 0
packets_max_in = 0
drop_out = False
initiate_out = False
total_packets_out = 0
packets_min_out = 0
packets_max_out = 0
debug = False
allow = 0
block = 0
slow = 0
inital = 0
enable = ""
disable = ""
#10~ packets per second


def is_any_thread_alive(threads):
    return True in [t.is_alive() for t in threads]


def log(msg):
    if debug:
        print(msg)


def process_packet_out():
    global drop_out
    global initiate_out
    global total_packets_out
    global packets_min_out
    global packets_max_out

    with pydivert.WinDivert(filter="udp.DstPort == 3074") as w:
        for packet in w:
            total_packets_out = total_packets_out + 1

            
            if not drop_out:
                #do not drop
                try:
                    w.send(packet)
                except Exception as e:
                    log(e)
            else:
                #slow the packet
                time.sleep(slow)
                # how many packets to BLOCK to get into the "Mode"
                if total_packets_out < inital and initiate_out:
                    log(f"BLOCKED out {total_packets_out} (initial)")
                    pass #DROP
                elif initiate_out:
                    initiate_out = False
                    total_packets_out = 0
                if not initiate_out and total_packets_out <= packets_min_out:
                    try:
                        log(f"PASS out {total_packets_out}")
                        w.send(packet)
                    except Exception as e:
                        log(e)
                elif not initiate_out: 
                    if (total_packets_out - packets_min_out) > block:  # how many packets to BLOCK
                        total_packets_out = 0
                        if packets_min_out < packets_max_out:
                            packets_min_out = packets_min_out + 1
                    log(f"BLOCKED out {total_packets_out}")
                    pass #DROP


def process_packet_in():
    global drop_in
    global initiate_in
    global total_packets_in
    global packets_min_in
    global packets_max_in

    with pydivert.WinDivert(filter="udp.SrcPort == 3074") as w:
        for packet in w:
            total_packets_in = total_packets_in + 1

            if not drop_in:
                #do not drop
                try:
                    w.send(packet)
                except Exception as e:
                    log(e)
            else:
                #slow the packet
                time.sleep(slow)
                # how many packets to BLOCK to get into the "Mode"
                if total_packets_in < inital and initiate_in:
                    log(f"BLOCKED in {total_packets_in} (initial)")
                    pass #DROP
                elif initiate_in:
                    initiate_in = False
                    total_packets_in = 0
                if not initiate_in and total_packets_in <= packets_min_in:  
                    try:
                        log(f"PASS in {total_packets_in}")
                        w.send(packet)
                    except Exception as e:
                        log(e)
                elif not initiate_in: 
                    if (total_packets_in - packets_min_in) > block: # how many packets to BLOCK
                        total_packets_in = 0
                        if packets_min_in < packets_max_in:
                            packets_min_in = packets_min_in + 1
                    log(f"BLOCKED in {total_packets_in}")
                    pass #DROP


def check_last_update():
    while True:
        global drop_in
        global initiate_in
        global total_packets_in
        global packets_min_in
        global packets_max_in
        global drop_out
        global initiate_out
        global total_packets_out
        global packets_min_out
        global packets_max_out

        try:  
            if keyboard.read_key() == enable: 
                print(f"Enabled")
                print(f"\n")
                winsound.Beep(750, 250)
                drop_in = True
                initiate_in = True
                #timings in
                total_packets_in = 0
                packets_min_in = 1
                packets_max_in = allow
                
                drop_out = True
                initiate_out = True
                #timings out
                total_packets_out = 0
                packets_min_out = 1
                packets_max_out = allow

            if keyboard.read_key() == disable:
                print(f"\n")
                print(f"Disabled")
                winsound.Beep(250, 500)
                drop_in = False
                drop_out = False
        except:
            break 


parser = argparse.ArgumentParser(description='Pausing the game, infinite Chaos Reach glitch')
parser.add_argument('-a','--allow', type=int, default=6, help='Packets to allow, default to 6')
parser.add_argument('-b','--block', type=int, default=4, help='Packets to block, default to 4. Lower this number to 3 if you cannot unpause the game')
parser.add_argument('-s','--slow', type=float, default=0.2, help='Slow down the packets, default to 0.2')
parser.add_argument('-i','--inital', type=int, default=20, help='How many packets to drop, to pause the game, default to 20')
parser.add_argument('-e','--enable', type=str, default="6", help='Key to enable the pause, default to "6"')
parser.add_argument('-d','--disable', type=str, default="7", help='Key to disable the pause, default to "7"')
args = parser.parse_args()
allow = args.allow
block = args.block
slow = args.slow
inital = args.inital
enable = args.enable
disable = args.disable


print(f"Boole! v3.0\n\n")
print(f'Press "{enable}" to enable\nPress "{disable}" to disable')
print(f'\nRun "./skip_boole.exe -h" to see all options')
t1 = Thread(target=check_last_update,daemon=True)
t2 = Thread(target=process_packet_in,daemon=True)
t3 = Thread(target=process_packet_out,daemon=True)
t1.start()
t2.start()
t3.start()
while is_any_thread_alive([t1,t2, t3]):
    time.sleep(0)

