F10::Suspend, Toggle
global isRunning = 0

6::
+6::
^6::
!6::
SoundBeep, 750, 250
Run %ComSpec% /c "netsh advfirewall firewall add rule name="boole-block-in" dir=in action=block remoteport=3074 protocol=UDP & netsh advfirewall firewall add rule name="boole-block-out" dir=out action=block remoteport=3074 protocol=UDP ",,hide
Sleep 5000
times = 0
times2 = 0
sleep1min = 0
sleep1max = 3000
sleep2min = 0
sleep2max = 2000

Loop {
    if (isRunning == 2){
        return
    }
    
    times++
    times2++
    
    if(times == 20){
        times = 0
        SoundBeep, 200, 400
        Run %ComSpec% /c "netsh advfirewall firewall delete rule name="boole-block-out"",,hide
        Sleep sleep1min
        Run %ComSpec% /c "netsh advfirewall firewall add rule name="boole-block-out" dir=out action=block remoteport=3074 protocol=UDP ",,hide       
        if(sleep1min < sleep1max){
            sleep1min += 500
        }
    }

    if(times2 == 40){
        times2 = 0
        SoundBeep, 900, 400
        Run %ComSpec% /c "netsh advfirewall firewall delete rule name="boole-block-in"",,hide
        Sleep sleep2min
        Run %ComSpec% /c "netsh advfirewall firewall add rule name="boole-block-in" dir=in action=block remoteport=3074 protocol=UDP ",,hide       
        if(sleep2min < sleep2max){
            sleep2min += 50
        }
    }
    Sleep 10
}
return

7::
+7::
^7::
!7::
isRunning = 2
SoundBeep, 250, 500
Run %ComSpec% /c "netsh advfirewall firewall delete rule name="boole-block-in" & netsh advfirewall firewall delete rule name="boole-block-out"",,hide
Reload
return

