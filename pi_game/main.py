from gpio import Gpio
import time, random

file_path = "config.yaml"
gpio = Gpio(file_path)

def get_random_winner_val():
    return random.randint(50, 100) / 100

def get_random_rest_val():
    return random.randint(0, 50) / 100

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

        now = 0
        last = 0

        # do nothing while we wait for button push
        while True:
            if gpio.first_button and not gpio.stop_reading and not gpio.stop_race:
                gpio.stop_reading = True
                print(f"we have a winner! -> motor at pin {gpio.winner_motor} is the winner, start the race and stop with push button")
                print("...")
                print("")
                gpio.start_motor(gpio.winner_motor, gpio.max_dutycycle) # start at 100%
                gpio.start_rest_of_motors(gpio.winner_motor, gpio.half_dutycycle) # run remaining motors at half of power
                now = time.time()
                last = time.time()

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

            # algorithm to change randomly the pace of each motor
            now = time.time()
            time_dif = round(now - last, 1)
            if time_dif >= gpio.hold_race_time and gpio.stop_reading:
                last = time.time()
                gpio.hold_race_time = gpio.time_change_duty   # change every 0.5 seconds

                # get 
                range_winner = get_random_winner_val()
                range_1 = get_random_rest_val()
                range_2 = get_random_rest_val()
                range_3 = get_random_rest_val()
                range_4 = get_random_rest_val()
                # update the values into each motor 
                gpio.start_motor(gpio.winner_motor, range_winner)
                gpio.start_motor_no_winner(gpio.motor_1, range_1)
                gpio.start_motor_no_winner(gpio.motor_2, range_2)
                gpio.start_motor_no_winner(gpio.motor_3, range_3)
                gpio.start_motor_no_winner(gpio.motor_4, range_4)
                print(f"winner: {range_winner} - range_rest {range_1} - range_rest {range_2} - range_rest {range_3} - range_rest {range_4}")

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
