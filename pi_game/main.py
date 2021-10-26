from gpio import Gpio
import time, random

file_path = "config.yaml"
gpio = Gpio(file_path)

def get_random_val(start, end):
    return random.randint(start, end) / 100


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
        last_start_race = 0

        is_running_at_start = True
        
        last_stop = time.time()
        last_start = time.time()
        last_end = time.time()

        # do nothing while we wait for button push
        while True:
            ## poll the stop and start motors input
            should_end = gpio.get_end_button()
            now = time.time()
            if now - last_end >= .5 and not should_end:
                if not gpio.first_push and not gpio.stop_reading:
                    if gpio.count_filter >= gpio.filter_limit and not gpio.first_button and not gpio.stop_reading:
                        gpio.first_button = True
                        gpio.stop_race = True
                        print(f"button 5 (END) pressed: {should_end}")

                if gpio.stop_reading:
                    gpio.first_button = True
                    gpio.stop_race = True
                    print(f"button 5 (END) pressed: {should_end}")
                last_end = time.time()

            should_stop_motors = gpio.get_stop_button()
            now = time.time()
            if now - last_stop >= .5 and should_stop_motors:
                if not gpio.first_push and not gpio.stop_reading:
                    if gpio.count_filter >= gpio.filter_limit and not gpio.first_button and not gpio.stop_reading:
                        gpio.turn_off_motors = True
                        print(f"button 6 (STOP_MOTORS) pressed: {should_stop_motors}")

                if gpio.stop_reading:
                    gpio.first_button = True
                    gpio.turn_off_motors = True
                    print(f"button 6 (STOP_MOTORS) pressed: {should_stop_motors}")
                last_stop = time.time()

            should_start_motors = gpio.get_start_button() 
            # if not should_start_motors:
            now = time.time()
            # print(f"pushed start {now - last_start}")
            if now - last_start >= .5 and not should_start_motors:  # if status is keeped for 200ms 
                if not gpio.first_push and not gpio.stop_reading:
                    if gpio.count_filter >= gpio.filter_limit and not gpio.first_button and not gpio.stop_reading:
                        gpio.turn_on_motors = True
                        print(f"button 11 (START_MOTORS) pressed: {should_start_motors}")

                if gpio.stop_reading:
                    gpio.first_button = True
                    gpio.turn_on_motors = True
                    print(f"button 11 (START_MOTORS) pressed: {should_start_motors}")
                last_start = time.time()


            if gpio.first_button and not gpio.stop_reading and not gpio.stop_race:
                gpio.stop_reading = True
                print(f"we have a winner! -> motor at pin {gpio.winner_motor} is the winner, start the race and stop with push button")
                print("...")
                print("")
                range_winner = get_random_val(0, 50)
                range_rest = get_random_val(50, 100)
                gpio.start_motor(gpio.winner_motor, range_winner) # start at 100%
                gpio.start_rest_of_motors(gpio.winner_motor, range_rest) # run remaining motors at half of power
                now = time.time()
                last = time.time()
                last_start_race = time.time()

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

            '''
            Losing button:
                0-2sec, every sec, vary between 50% - 100%.
                2-end, every sec, vary between 0%-50%
            Winning button:
                0-2sec, every sec, vary between 0-50%.
                2-end, every sec, 100%
            '''
            # algorithm to change randomly the pace of each motor
            now = time.time()
            time_dif = round(now - last, 1)
            time_dif_sec = round(now - last_start_race, 1)

            if time_dif_sec > gpio.one_sec and gpio.stop_reading:
                last_start_race = time.time()
            
                if time_dif > gpio.hold_race_time and gpio.stop_reading:
                    last = time.time()
                    is_running_at_start = False
                    gpio.hold_race_time = gpio.time_change_duty   # change every 1 second

                    # get the random values 
                    range_winner = gpio.max_dutycycle
                    range_1 = get_random_val(0, 100)
                    range_2 = get_random_val(0, 100)
                    range_3 = get_random_val(0, 100)
                    range_4 = get_random_val(0, 100)
                    # update the values into each motor 
                    gpio.start_motor(gpio.winner_motor, range_winner)
                    gpio.start_motor_no_winner(gpio.motor_1, range_1)
                    gpio.start_motor_no_winner(gpio.motor_2, range_2)
                    gpio.start_motor_no_winner(gpio.motor_3, range_3)
                    gpio.start_motor_no_winner(gpio.motor_4, range_4)

                elif time_dif <= gpio.hold_race_time and gpio.stop_reading and is_running_at_start:
                    # get random values 
                    range_winner = get_random_val(0, 50)
                    range_1 = get_random_val(50, 100)
                    range_2 = get_random_val(50, 100)
                    range_3 = get_random_val(50, 100)
                    range_4 = get_random_val(50, 100)
                    # update the values into each motor 
                    gpio.start_motor(gpio.winner_motor, range_winner)
                    gpio.start_motor_no_winner(gpio.motor_1, range_1)
                    gpio.start_motor_no_winner(gpio.motor_2, range_2)
                    gpio.start_motor_no_winner(gpio.motor_3, range_3)
                    gpio.start_motor_no_winner(gpio.motor_4, range_4)

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
                last_start_race = 0
                gpio.winner_motor = 0
                gpio.stop_race = False
                is_running_at_start = True
                gpio.stop_motors()

            time.sleep(.1) # wait 100ms 

    except KeyboardInterrupt:
        gpio.stop_motor(motor)
        gpio.stop()
