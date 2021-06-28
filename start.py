from cosmic.run import start, setup

setup()
print('''
------------------------------------------------
╭━━┳━━┳━━┳╮╭┳┳━━╮
┃╭━┫╭╮┃━━┫╰╯┣┫╭━╯
┃╰━┫╰╯┣━━┃┃┃┃┃╰━╮
╰━━┻━━┻━━┻┻┻┻┻━━╯

Cosmic Ray Detection with Python

By : Naimish Mani B (@naimish240)
------------------------------------------------
''')

calibration_time = int(input("Enter calibration time in seconds: "))
duration = int(input("Enter the number of seconds you want to run for: "))

start(calibration_time, duration)
