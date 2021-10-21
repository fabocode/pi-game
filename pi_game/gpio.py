import yaml, pigpio, time

class Gpio:

    def __init__(self, filepath):

        self.first_push = False
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
        self.stop_race = False

        # first test is failing
        self.count_filter = 0 
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
            self.button_5 = self.buttons[4]
            
            # set the pins used for the motors
            self.motors = self.config.get('pins')["motors"]
            self.motor_1 = self.motors[0]
            self.motor_2 = self.motors[1]
            self.motor_3 = self.motors[2]
            self.motor_4 = self.motors[3]
            self.motor_5 = False

            # set the configuration parameters for pwm/motor 
            self.freq = self.config.get('pwm_params')["freq"]
            self.max_dutycycle = float(self.config.get('pwm_params')["max_dutycycle"])
            self.half_dutycycle = float(self.config.get('pwm_params')["half_dutycycle"])
            self.min_dutycycle = float(self.config.get('pwm_params')["min_dutycycle"])

            # max time allowed to run motors
            self.maxtime = float(self.config.get('pwm_params')["max_time"])

            # glitch for debouncing
            self.glitch = int(self.config.get('pins')["glitch"])

            # set maximum number of pushes to filter input
            self.filter_limit = int(self.config.get('pins')["max_num_button_pushes"])

    def stop_motors(self):
        self.pi.set_PWM_dutycycle(self.motor_1, self.min_dutycycle)
        self.pi.set_PWM_dutycycle(self.motor_2, self.min_dutycycle)
        self.pi.set_PWM_dutycycle(self.motor_3, self.min_dutycycle)
        self.pi.set_PWM_dutycycle(self.motor_4, self.min_dutycycle)

    def callback(self, button_gpio, l, t):
        ''' Callback to handle button push input'''
        
        # in the 1st push I'm receiving multiple trigger events 
        # this will check for each input, count and get only the last counted input
        # which is always the correct push
        # so this algorithm is a filter for button pushes
        print(f"button pushed: {button_gpio}")
        if not self.first_push and not self.stop_reading:
            if self.count_filter >= self.filter_limit and not self.first_button and not self.stop_reading:
                print(f"how many times? {self.count_filter} - {self.filter_limit}")
                if button_gpio == self.button_5:
                    self.first_button = True
                    print("pushed stop!!!!!!!!!!!!!!!!!!!")
                    # self.winner_motor = self.motor_5
                    self.stop_race = True

                if button_gpio == self.button_4:
                    self.first_button = True
                    self.winner_motor = self.motor_4
                    
                if button_gpio == self.button_3:
                    self.first_button = True
                    self.winner_motor = self.motor_3
                    
                if button_gpio == self.button_2:
                    self.first_button = True
                    self.winner_motor = self.motor_2
                    
                if button_gpio == self.button_1:
                    self.first_button = True
                    self.winner_motor = self.motor_1    
            else:
                self.count_filter += 1
        if self.stop_reading and button_gpio == self.button_5:
            self.first_button = True
            print("pushed stop!!!!!!!!!!!!!!!!!!!")
            # self.winner_motor = self.motor_5
            self.stop_race = True
            

    def setup_buttons(self):
        ''' Setup buttons as interrupts '''
        self.pi.set_mode(self.button_1, pigpio.INPUT)
        self.pi.set_pull_up_down(self.button_1, pigpio.PUD_UP)
        self.pi.set_noise_filter(self.button_1, 50000, 50000)  # Debounce switch
        self.pi.set_glitch_filter(self.button_1, self.glitch) # Ignore edges shorter than GLITCH microseconds.
        callback1 = self.pi.callback(self.button_1, pigpio.FALLING_EDGE, self.callback)
        
        self.pi.set_mode(self.button_2, pigpio.INPUT)
        self.pi.set_pull_up_down(self.button_2, pigpio.PUD_UP)
        self.pi.set_noise_filter(self.button_2, 50000, 50000)  # Debounce switch
        self.pi.set_glitch_filter(self.button_2, self.glitch)
        callback2 = self.pi.callback(self.button_2, pigpio.FALLING_EDGE, self.callback)
        
        self.pi.set_mode(self.button_3, pigpio.INPUT)
        self.pi.set_pull_up_down(self.button_3, pigpio.PUD_UP)
        self.pi.set_noise_filter(self.button_3, 50000, 50000)  # Debounce switch
        self.pi.set_glitch_filter(self.button_3, self.glitch)
        callback3 = self.pi.callback(self.button_3, pigpio.FALLING_EDGE, self.callback)
        
        self.pi.set_mode(self.button_4, pigpio.INPUT)
        self.pi.set_pull_up_down(self.button_4, pigpio.PUD_UP)
        self.pi.set_noise_filter(self.button_4, 50000, 50000)  # Debounce switch
        self.pi.set_glitch_filter(self.button_4, self.glitch)
        callback4 = self.pi.callback(self.button_4, pigpio.FALLING_EDGE, self.callback)
    
        self.pi.set_mode(self.button_5, pigpio.INPUT)
        self.pi.set_pull_up_down(self.button_5, pigpio.PUD_UP)
        self.pi.set_noise_filter(self.button_5, 50000, 50000)  # Debounce switch
        self.pi.set_glitch_filter(self.button_5, self.glitch)
        callback4 = self.pi.callback(self.button_5, pigpio.FALLING_EDGE, self.callback)
    
    def start_motor(self, motor, target_duty):
        ''' Send pulses to motor '''
        duty = 255 * target_duty
        self.pi.set_PWM_frequency(motor,  self.freq)
        self.pi.set_PWM_dutycycle(motor, duty)
        
    def stop_motor(self, motor):
        ''' Stop motor '''
        self.pi.set_PWM_dutycycle(motor, self.min_dutycycle)

    def start_rest_of_motors(self, winner):
        ''' Starts all the motors at half duty cycle instead winner motor '''
        for motor in self.motors:
            if winner != motor:
                self.start_motor(motor, self.half_dutycycle)

    def start(self):
        self.pi = pigpio.pi()

    def stop(self):
        self.stop_motors()
        self.pi.stop()
