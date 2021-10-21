from gpio import Gpio
import time

file_path = "config.yaml"
gpio = Gpio(file_path)

if __name__ == "__main__":
    try:
        print("====================================")
        print("=== Welcome to the button race! ====")
        print("====================================")
        gpio.load() # load data from config file
        gpio.setup_buttons()

        # start motor_1
        motor = gpio.motor_1
        duty = gpio.max_dutycycle
        

        # to measure time 
        start = 0
        now = 0

        # do nothing while we wait for button push
        while True:
            if gpio.first_button and not gpio.stop_reading:
                gpio.stop_reading = True
                print(f"we have a winner! -> motor at pin {gpio.winner_motor} is the winner, start the race and stop after 10 seconds")
                print("...")
                print("")
                gpio.start_motor(gpio.winner_motor, gpio.max_dutycycle) # start at 100%
                gpio.start_rest_of_motors(gpio.winner_motor) # run remaining motors at half of power
                start = time.time()
                now = time.time()

            now = time.time()
            time_dif = int(now - start)

            # start counting and running the motors
            if time_dif >= gpio.maxtime and gpio.stop_reading:
                gpio.stop_motors()
                print("====================================")
                print("============ Race Ended ============")
                print(f"====== Congratulations to {gpio.winner_motor} =======")
                print("====================================")
                print("")
                
                # this code is optional, I din't know if we needed to restart or stop the program
                want_to_continue = input("Would you like to restart?: (Y/n): ")
                if want_to_continue.lower() == 'n':
                    print("Closing program now...")
                    gpio.stop()
                    exit() # end the program 
                else:
                    print("Game was restarted!...")
                    print("")
                    # gpio.start()
                    gpio.stop_reading = False
                    gpio.first_push = False
                    gpio.first_button = False
                    now = 0 
                    start = 0
                    gpio.winner_motor = 0
                    gpio.stop_motors()
                    continue

            time.sleep(.1) # wait 100ms 

    except KeyboardInterrupt:
        gpio.stop_motor(motor)
        gpio.stop()
