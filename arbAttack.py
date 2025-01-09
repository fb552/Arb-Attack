import socket, sys, time

def open_socket(ip_addr,port): # Create a socket connection to instrument
    global skt
    try:
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.settimeout(8) # 8 second timeout
    except socket.error as e:
        print("Error creating socket: %s" % e)
        sys.exit(1)
    try:
        skt.connect((ip_addr, port))
    except socket.gaierror as e:
        print("Address-related error connecting to instrument: %s" % e)
        sys.exit(1)
    except socket.error as e:
        print("Error connecting to socket on instrument: %s" % e)
        sys.exit(1)

def close_sockets(): # Close all socket connections to instruments
    skt.close()

def send_scpi(command): # Send SCPI command 
    command = command + '\n'
    skt.send(command.encode('ASCII'))
                         
# def enTer(): # Receive instrument data 
#     dataStr=skt.recv(1024).decode('ASCII')
#     return dataStr.strip()

def turn_on(ch, volt, curr):
    send_scpi(f'VOLT {volt},(@{ch})')
    send_scpi(f'CURR {curr},(@{ch})')
    send_scpi(f'OUTP ON,(@{ch})')
    print(f"{volt}V ON @ channel {ch}")

def pulse(Vstar, Vtop, Tstar, Ttop, Tend, step, ch):    
    send_scpi(f'ARB:SEQ:STEP:FUNC:SHAP PULS,{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:PULS:STAR {Vstar},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:PULS:TOP {Vtop},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:PULS:STAR:TIM {Tstar},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:PULS:TOP:TIM {Ttop},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:PULS:END:TIM {Tend},{step},(@{ch})')

def exp(Vstar, Vend, Tstar, T, Tcon, step, ch):    
    send_scpi(f'ARB:SEQ:STEP:FUNC:SHAP EXP,{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:EXP:STAR {Vstar},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:EXP:END {Vend},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:EXP:STAR:TIM {Tstar},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:EXP:TIM {T},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:EXP:TCON {Tcon},{step},(@{ch})')
    
def stair(Vstar, Vend, Tstar, T, Tend, steps, step, ch):
    send_scpi(f'ARB:SEQ:STEP:FUNC:SHAP STAIR,{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:STA:STAR {Vstar},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:STA:END {Vend},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:STA:STAR:TIM {Tstar},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:STA:TIM {T},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:STA:END:TIM {Tend},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:STA:NST {steps},{step},(@{ch})')

def ramp(Vstar, Vend, Tstar, Trise, Tend, step, ch):
    send_scpi(f'ARB:SEQ:STEP:FUNC:SHAP RAMP,{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:RAMP:STAR {Vstar},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:RAMP:END {Vend},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:RAMP:STAR:TIM {Tstar},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:RAMP:RTIM:TIM {Trise},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:RAMP:END:TIM {Tend},{step},(@{ch})')

def trapezoid(Vstar, Vtop, Tstar, Trise, Ttop, Tfall, Tend, step, ch):
    send_scpi(f'ARB:SEQ:STEP:FUNC:SHAP TRAP,{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:TRAP:STAR {Vstar},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:TRAP:TOP {Vtop},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:TRAP:STAR:TIM {Tstar},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:TRAP:RTIM:TIM {Trise},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:TRAP:TOP:TIM {Ttop},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:TRAP:FTIM:TIM {Tfall},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:TRAP:END:TIM {Tend},{step},(@{ch})')

def sin(Vampl, offset, freq, step, ch):
    send_scpi(f'ARB:SEQ:STEP:FUNC:SHAP SIN,{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:SIN:AMPL {Vampl},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:SIN:OFFS {offset},{step},(@{ch})')
    send_scpi(f'ARB:SEQ:STEP:VOLT:SIN:FREQ {freq},{step},(@{ch})')

if __name__ == "__main__":
    
    open_socket('100.124.81.84',5025)  # Select device

    # Reset & configure mainframe / instrument
    send_scpi('*RST')
    send_scpi('OUTP OFF, (@1:4)') # Output off
    send_scpi('DISP:VIEW METER4') # All channel display
    print("Mainframe configured")

    time.sleep(5)

    # Setup 12V supply 
    turn_on(2,12,6)
    time.sleep(5)

    # Setup 3V3 supply 
    turn_on(3,3.45,20)
   
    print("Power on: connect to the EVB through the GUI")

    # Setup Arb
    # To set up output 1 to program a sequence of voltage waveforms, use:
    send_scpi('ARB:FUNC:TYPE VOLT,(@3)')
    send_scpi('ARB:FUNC:SHAP SEQ,(@3)')
    send_scpi('ARB:SEQ:RESet (@3)')
    # Step 0 : voltage pulse
    pulse(3.45,3.6,0.001,0.002,0.001,0,3)
    # Step 1: voltage drop
    pulse(3.45,2.9,0.001,0.002,0.001,1,3)
    # Step 2: exponential up
    exp(3.45,3.6,0.0001,0.003,0.001,2,3)
    # Step 3: exponential down
    exp(3.45,2.9,0.0001,0.005,0.001,3,3)
    # Step 4: sine wave
    sin(0.35,3.25,1000,4,3)

    # Repeat steps:
    send_scpi('ARB:SEQ:STEP:COUN 10,0,(@3)')
    send_scpi('ARB:SEQ:STEP:COUN 10,1,(@3)')
    send_scpi('ARB:SEQ:STEP:COUN 10,4,(@3)')
    
    # Set the sequence to repete continuously
    send_scpi('ARB:SEQ:COUN INF,(@3)')

    print("Transient configured successfully")

    while True:
        input("Press 'enter' to start the arb attack:")

        # Set the transient trigger system and trigger the sequence:
        send_scpi('VOLT:MODE ARB,(@3)')
        send_scpi('INIT:TRAN (@3)')
        send_scpi('*TRG')
        print("Attack sequence initiated")

        input("Press 'enter' to stop the arb attack:")
        send_scpi('ABOR:TRAN (@3)')
        print("Attack sequence aborted")

    # Close socket - release resources
    close_sockets()