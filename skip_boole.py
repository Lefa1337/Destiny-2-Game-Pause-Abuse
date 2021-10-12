
import pydivert
from threading import Thread
import time
import keyboard  
import winsound


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


#10~ packets per second

def is_any_thread_alive(threads):
    return True in [t.is_alive() for t in threads]


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
                    print(e)
            else:
                #slow the packet
                time.sleep(0.20)
                # how many packets to BLOCK to get into the "Mode"
                if total_packets_out < 20 and initiate_out:
                    pass #DROP
                elif initiate_out:
                    initiate_out = False
                    total_packets_out = 0
                if not initiate_out and total_packets_out <= packets_min_out:
                    try:
                        print(f"PASS out {total_packets_out}")
                        w.send(packet)
                    except Exception as e:
                        print(e)
                elif not initiate_out: 
                    if (total_packets_out - packets_min_out) > 5:  # how many packets to BLOCK
                        total_packets_out = 0
                        if packets_min_out < packets_max_out:
                            packets_min_out = packets_min_out + 1
                    print(f"BLOCKED out {total_packets_out}")
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
                    print(e)
            else:
                #slow the packet
                time.sleep(0.20)
                # how many packets to BLOCK to get into the "Mode"
                if total_packets_in < 20 and initiate_in:
                    pass #DROP
                elif initiate_in:
                    initiate_in = False
                    total_packets_in = 0
                if not initiate_in and total_packets_in <= packets_min_in:  
                    try:
                        print(f"PASS in {total_packets_in}")
                        w.send(packet)
                    except Exception as e:
                        print(e)
                elif not initiate_in: 
                    if (total_packets_in - packets_min_in) > 5: # how many packets to BLOCK
                        total_packets_in = 0
                        if packets_min_in < packets_max_in:
                            packets_min_in = packets_min_in + 1
                    print(f"BLOCKED in {total_packets_in}")
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
            if keyboard.read_key() == '6': 
                print(f"Enabled")
                print(f"\n\n")
                winsound.Beep(750, 250)
                drop_in = True
                initiate_in = True
                #timings in
                total_packets_in = 0
                packets_min_in = 1
                packets_max_in = 10
                
                drop_out = True
                initiate_out = True
                #timings out
                total_packets_out = 0
                packets_min_out = 1
                packets_max_out = 10

            if keyboard.read_key() == '7':
                print(f"\n\n")
                print(f"Disabled")
                winsound.Beep(250, 500)
                drop_in = False
                drop_out = False
        except:
            break 


print(f"Boole! v2.1\n\n")
print(f"Press 6 to enable\nPress 7 to disable")
t1 = Thread(target=check_last_update,daemon=True)
t2 = Thread(target=process_packet_in,daemon=True)
t3 = Thread(target=process_packet_out,daemon=True)
t1.start()
t2.start()
t3.start()
while is_any_thread_alive([t1,t2, t3]):
    time.sleep(0)

