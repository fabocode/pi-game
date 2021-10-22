import yaml, pigpio, time
import RPi.GPIO as GPIO 

class Gpio:

    def __init__(self, filepath):
        GPIO.setmode(GPIO.BCM)
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

        self.turn_off_motors = False
        self.turn_on_motors = False
        self.motor_individual_start = False
        self.motor_call =  0

        # first test is failing
        self.count_filter = 0 
        if not self.pi.connected:
            exit()
    
    def start_motor_no_winner(self, motor, duty):
        if motor != self.winner_motor:
            self.start_motor(motor, duty)
        else:
            print(f"no update {motor}, because is the winner ")

    def load(self):
        """Loads a yaml file"""
        with open(self.filepath, "r") as file_descriptor:

            # load the pins used for the program
            self.config = yaml.load(file_descriptor, Loader=yaml.FullLoader)

            # set the pins used for the buttons
            self.buttons = self.config.get('pins')["buttons"]
            self.button_1 = self.buttons[0]
            self.button_2 = self.buttons[1]
            self.button_3 = self.buttons[2]
            self.button_4 = self.buttons[3]
            self.button_5 = self.buttons[4]
            self.button_6 = self.buttons[5]
            self.button_7 = self.buttons[6]
            self.button_8 = self.buttons[7]
            self.button_9 = self.buttons[8]
            self.button_10 = self.buttons[9]
            self.button_11 = self.buttons[10]
            
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
            self.hold_race_time = float(self.config.get('pwm_params')["hold_race_time"])
            self.time_change_duty = float(self.config.get('pwm_params')["time_change_duty"])
            self.one_sec = float(self.config.get('pwm_params')["one_sec"])

            # glitch for debouncing
            self.glitch = int(self.config.get('pins')["glitch"])

            # set maximum number of pushes to filter input
            self.filter_limit = int(self.config.get('pins')["max_num_button_pushes"])

    def stop_motors(self):
        self.pi.set_PWM_dutycycle(self.motor_1, self.min_dutycycle)
        self.pi.set_PWM_dutycycle(self.motor_2, self.min_dutycycle)
        self.pi.set_PWM_dutycycle(self.motor_3, self.min_dutycycle)
        self.pi.set_PWM_dutycycle(self.motor_4, self.min_dutycycle)

    def start_all_motors(self):
        self.start_motor(self.motor_1, self.max_dutycycle)
        self.start_motor(self.motor_2, self.max_dutycycle)
        self.start_motor(self.motor_3, self.max_dutycycle)
        self.start_motor(self.motor_4, self.max_dutycycle)
    
    def reset(self):
        self.stop_reading = False
        self.first_push = False
        self.first_button = False
        self.winner_motor = 0
        self.stop_race = False
        self.first_button = False
        self.turn_off_motors = False
        self.individual_start = False
        self.stop_motors()

    def button_pressed_callback_1(self, channel):
        if not self.first_push and not self.stop_reading:
            if self.count_filter >= self.filter_limit and not self.first_button and not self.stop_reading:
                self.first_button = True
                self.winner_motor = self.motor_1    

    def button_pressed_callback_2(self, channel):
        if not self.first_push and not self.stop_reading:
            if self.count_filter >= self.filter_limit and not self.first_button and not self.stop_reading:
                self.first_button = True
                self.winner_motor = self.motor_2    


    def button_pressed_callback_3(self, channel):
         if not self.first_push and not self.stop_reading:
            if self.count_filter >= self.filter_limit and not self.first_button and not self.stop_reading:
                self.first_button = True
                self.winner_motor = self.motor_3   


    def button_pressed_callback_4(self, channel):
        if not self.first_push and not self.stop_reading:
            if self.count_filter >= self.filter_limit and not self.first_button and not self.stop_reading:
                self.first_button = True
                self.winner_motor = self.motor_4   

        
    def button_pressed_callback_5(self, channel):
        if not self.first_push and not self.stop_reading:
            if self.count_filter >= self.filter_limit and not self.first_button and not self.stop_reading:
                self.first_button = True
                self.stop_race = True

        if self.stop_reading:
            self.first_button = True
            self.stop_race = True

    def button_pressed_callback_6(self, channel):
        if not self.first_push and not self.stop_reading:
            if self.count_filter >= self.filter_limit and not self.first_button and not self.stop_reading:
                self.turn_off_motors = True

        if self.stop_reading:
            self.first_button = True
            self.turn_off_motors = True

    def button_pressed_callback_7(self, channel):
        if not self.first_push and not self.stop_reading:
            if self.count_filter >= self.filter_limit and not self.first_button and not self.stop_reading:
                self.motor_individual_start = True
                self.motor_call = self.motor_1

    def button_pressed_callback_8(self, channel):
        if not self.first_push and not self.stop_reading:
            if self.count_filter >= self.filter_limit and not self.first_button and not self.stop_reading:
                self.motor_individual_start = True
                self.motor_call = self.motor_2

    def button_pressed_callback_9(self, channel):
        if not self.first_push and not self.stop_reading:
            if self.count_filter >= self.filter_limit and not self.first_button and not self.stop_reading:
                self.motor_individual_start = True
                self.motor_call = self.motor_3

    def button_pressed_callback_10(self, channel):
        if not self.first_push and not self.stop_reading:
            if self.count_filter >= self.filter_limit and not self.first_button and not self.stop_reading:
                self.motor_individual_start = True
                self.motor_call = self.motor_4

    def button_pressed_callback_11(self, channel):
        if not self.first_push and not self.stop_reading:
            if self.count_filter >= self.filter_limit and not self.first_button and not self.stop_reading:
                self.turn_on_motors = True

        if self.stop_reading:
            self.first_button = True
            self.turn_on_motors = True


    def setup_buttons(self):
        ''' Setup buttons as interrupts '''
        GPIO.setup(self.button_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_1, GPIO.FALLING, 
                callback=self.button_pressed_callback_1, bouncetime=300)
        
        GPIO.setup(self.button_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_2, GPIO.FALLING, 
                callback=self.button_pressed_callback_2, bouncetime=300)
        
        GPIO.setup(self.button_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_3, GPIO.FALLING, 
                callback=self.button_pressed_callback_3, bouncetime=300)
        
        GPIO.setup(self.button_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_4, GPIO.FALLING, 
                callback=self.button_pressed_callback_4, bouncetime=300)
        
        GPIO.setup(self.button_5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_5, GPIO.FALLING, 
                callback=self.button_pressed_callback_5, bouncetime=300)
        
        GPIO.setup(self.button_6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_6, GPIO.FALLING, 
                callback=self.button_pressed_callback_6, bouncetime=300)
        
        GPIO.setup(self.button_7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_7, GPIO.FALLING, 
                callback=self.button_pressed_callback_7, bouncetime=300)
        
        GPIO.setup(self.button_8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_8, GPIO.FALLING, 
                callback=self.button_pressed_callback_8, bouncetime=300)
        
        GPIO.setup(self.button_9, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_9, GPIO.FALLING, 
                callback=self.button_pressed_callback_9, bouncetime=300)
        
        GPIO.setup(self.button_10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_10, GPIO.FALLING, 
                callback=self.button_pressed_callback_10, bouncetime=300)
        
        GPIO.setup(self.button_11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_11, GPIO.FALLING, 
                callback=self.button_pressed_callback_11, bouncetime=300)
        
    def start_motor(self, motor, target_duty):
        ''' Send pulses to motor '''
        duty = 255 * target_duty
        self.pi.set_PWM_frequency(motor,  self.freq)
        self.pi.set_PWM_dutycycle(motor, duty)
        
    def stop_motor(self, motor):
        ''' Stop motor '''
        self.pi.set_PWM_dutycycle(motor, self.min_dutycycle)

    def start_rest_of_motors(self, winner, dutycycle=0.5):
        ''' Starts all the motors at half duty cycle instead winner motor '''
        for motor in self.motors:
            if winner != motor:
                self.start_motor(motor, self.half_dutycycle)

    def start(self):
        self.pi = pigpio.pi()

    def stop(self):
        self.stop_motors()
        self.pi.stop()
        GPIO.cleanup()
