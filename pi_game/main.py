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

        # do nothing while we wait for button push
        while True:
            if gpio.first_button and not gpio.stop_reading and not gpio.stop_race:
                gpio.stop_reading = True
                print(f"we have a winner! -> motor at pin {gpio.winner_motor} is the winner, start the race and stop with push button")
                print("...")
                print("")
                gpio.start_motor(gpio.winner_motor, gpio.max_dutycycle) # start at 100%
                gpio.start_rest_of_motors(gpio.winner_motor) # run remaining motors at half of power

            # check if turn off is activated
            if gpio.turn_off_motors:
                gpio.turn_off_motors = False
                gpio.reset()

            # check if turn off is activated
            if gpio.turn_on_motors:
                gpio.turn_on_motors = False
                gpio.start_all_motors()   # turn them all on
                
            # check individual turn calls
            if gpio.motor_individual_start:
                gpio.motor_individual_start = False
                gpio.start_motor(gpio.motor_call, gpio.min_dutycycle)   # turn them off individually 

            # continue until stop button is pushed
            if gpio.stop_race:
                gpio.stop_motors()
                print("====================================")
                print("============ Race Ended ============")
                print(f"====== Congratulations to {gpio.winner_motor} =======")
                print("====================================")
                print("")
                
                
                print("Game was restarted!...")
                print("")
                gpio.stop_reading = False
                gpio.first_push = False
                gpio.first_button = False
                now = 0 
                start = 0
                gpio.winner_motor = 0
                gpio.stop_race = False
                gpio.stop_motors()

            time.sleep(.1) # wait 100ms 

    except KeyboardInterrupt:
        gpio.stop_motor(motor)
        gpio.stop()
