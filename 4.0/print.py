import PCC
baudrate = 115200
printid = '1'
tem_position = [0, 2]
portname = '/dev/ttyUSB0'
pc = PCC.PrintControl(printid, portname, baudrate, tem_position)
pc.print_model(filename="1.gcode")