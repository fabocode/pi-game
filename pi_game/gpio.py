import yaml, pigpio, time

class Gpio:

    def __init__(self, filepath):
        self.filepath = filepath 
        self.first_button = False
        self.stop_reading = False  
        self.winner_motor = 0
        self.config = {}
        self.buttons = []
        self.motors = []
        self.freq = 0
        self.duty = 0
        self.pi = pigpio.pi()
        if not self.pi.connected:
            exit()

    def load(self):
        """Loads a yaml file"""
        with open(self.filepath, "r") as file_descriptor:

            # load the pins used for the program
            self.config = yaml.load(file_descriptor, Loader=yaml.FullLoader)
            self.buttons = self.config.get('pins')["buttons"]

            # set the pins used for the buttons
            self.button_1 = self.buttons[0]
            self.button_2 = self.buttons[1]
            self.button_3 = self.buttons[2]
            self.button_4 = self.buttons[3]
            
            # set the pins used for the motors
            self.motors = self.config.get('pins')["motors"]
            self.motor_1 = self.motors[0]
            self.motor_2 = self.motors[1]
            self.motor_3 = self.motors[2]
            self.motor_4 = self.motors[3]

            # set the configuration parameters for pwm/motor 
            self.freq = self.config.get('pwm_params')["freq"]
            self.max_dutycycle = float(self.config.get('pwm_params')["max_dutycycle"])
            self.half_dutycycle = float(self.config.get('pwm_params')["half_dutycycle"])
            self.min_dutycycle = float(self.config.get('pwm_params')["min_dutycycle"])

            # max time allowed to run motors
            self.maxtime = float(self.config.get('pwm_params')["max_time"])

    def callback_1(self, g, l, t):
        if not self.first_button and not self.stop_reading:
            self.first_button = True
            self.winner_motor = self.motor_1
        print("Callback 1: " + str(l) + " " + str(t))

    def callback_2(self, g, l, t):
        if not self.first_button and not self.stop_reading:
            self.first_button = True
            self.winner_motor = self.motor_2
        print("Callback 2: " + str(l) + " " + str(t))

    def callback_3(self, g, l, t):
        if not self.first_button and not self.stop_reading:
            self.first_button = True
            self.winner_motor = self.motor_3
        print("Callback 3: " + str(l) + " " + str(t))

    def callback_4(self, g, l, t):
        if not self.first_button and not self.stop_reading:
            self.first_button = True
            self.winner_motor = self.motor_4
        print("Callback 4: " + str(l) + " " + str(t))

    def setup_buttons(self):
        self.pi.set_mode(self.button_1, pigpio.INPUT)
        self.pi.set_pull_up_down(self.button_1, pigpio.PUD_UP)
        self.pi.set_noise_filter(self.button_1, 50000, 50000)  # Debounce switch
        callback1 = self.pi.callback(self.button_1, pigpio.FALLING_EDGE, self.callback_1)
        
        self.pi.set_mode(self.button_2, pigpio.INPUT)
        self.pi.set_pull_up_down(self.button_2, pigpio.PUD_UP)
        self.pi.set_noise_filter(self.button_2, 50000, 50000)  # Debounce switch
        callback2 = self.pi.callback(self.button_2, pigpio.FALLING_EDGE, self.callback_2)
        
        self.pi.set_mode(self.button_3, pigpio.INPUT)
        self.pi.set_pull_up_down(self.button_3, pigpio.PUD_UP)
        self.pi.set_noise_filter(self.button_3, 50000, 50000)  # Debounce switch
        callback3 = self.pi.callback(self.button_3, pigpio.FALLING_EDGE, self.callback_3)
        
        self.pi.set_mode(self.button_4, pigpio.INPUT)
        self.pi.set_pull_up_down(self.button_4, pigpio.PUD_UP)
        self.pi.set_noise_filter(self.button_4, 50000, 50000)  # Debounce switch
        callback4 = self.pi.callback(self.button_4, pigpio.FALLING_EDGE, self.callback_4)
    
    def start_motor(self, motor, target_duty):
        duty = 255 * target_duty
        self.pi.set_PWM_frequency(motor,  self.freq)
        self.pi.set_PWM_dutycycle(motor, duty)
        
    def stop_motor(self, motor):
        self.pi.set_PWM_dutycycle(motor, self.min_dutycycle)

    def start_rest_of_motors(self, winner):
        for motor in self.motors:
            if winner != motor:
                self.start_motor(motor, self.half_dutycycle)

    def stop(self):
        self.pi.set_PWM_dutycycle(self.motor_1, self.min_dutycycle)
        self.pi.set_PWM_dutycycle(self.motor_2, self.min_dutycycle)
        self.pi.set_PWM_dutycycle(self.motor_3, self.min_dutycycle)
        self.pi.set_PWM_dutycycle(self.motor_4, self.min_dutycycle)
        self.pi.stop()


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
                gpio.start_motor(gpio.winner_motor, gpio.max_dutycycle) # start at 100%
                # gpio.start_rest_of_motors(gpio.winner_motor) # run remaining motors at half of power
                start = time.time()
                now = time.time()

            now = time.time()
            time_dif = int(now - start)

            # start counting and running the motors
            if time_dif >= gpio.maxtime and gpio.stop_reading:
                gpio.stop_reading = False
                gpio.stop()
                print("====================================")
                print("============ Race Ended ============")
                print(f"====== Congratulations to {gpio.winner_motor} =======")
                print("====================================")
                exit() # end the program 

            time.sleep(.1) # wait 100ms 

    except KeyboardInterrupt:
        gpio.stop_motor(motor)
        gpio.stop()
        