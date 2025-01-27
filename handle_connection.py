import time
import board
import digitalio
import rotaryio
from analogio import AnalogIn
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from usb_hid import devices
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

cc = ConsumerControl(usb_hid.devices)
kbd = Keyboard(devices)

class Button:
    def __init__(self, pin, keycode):
        self.pin = pin
        self.button = digitalio.DigitalInOut(pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP
        self.keycode = keycode
        self.pressed = False

    def update(self):
        if not self.button.value and not self.pressed:
            self.press()
            self.release()
            self.pressed = True
        elif self.button.value and self.pressed:
            self.release()
            self.pressed = False

    def press(self):
        print(f"Button {self.pin} pressed.")
        kbd.press(self.keycode)

    def release(self):
        print(f"Button {self.pin} released.")
        kbd.release(self.keycode)

class Potentiometer:
    def __init__(self, pin, name, min_value=400, max_value=63695, threshold=1000):
        self.analog = AnalogIn(pin)
        self.last_value = None
        self.min_value = min_value
        self.max_value = max_value
        self.threshold = threshold
        self.name = name

    def update(self):
        current_value = self.analog.value
        normalized_value = self.normalize(current_value)
        if self.last_value is None or abs(current_value - self.last_value) > self.threshold:
            self.handle_change(normalized_value)
            self.last_value = current_value

    def normalize(self, value):
        clamped_value = max(self.min_value, min(value, self.max_value))
        normalized_value = (clamped_value - self.min_value) / (self.max_value - self.min_value) * 100
        return normalized_value


    def handle_change(self, value):
        print(f"{self.name} normalized value: {int(value)}") 


class Encoder:
    def __init__(self, pin_a, pin_b, name, volume_step=60):
        self.encoder = rotaryio.IncrementalEncoder(pin_a, pin_b)
        self.last_position = None
        self.name = name
        self.volume_step = volume_step
        
    def update(self):
        position = self.encoder.position
        if self.last_position is None or position != self.last_position:
            self.handle_change(position)
            self.last_position = position

    def handle_change(self, position):
        changed_value = position - self.last_position if self.last_position is not None else 0
        if self.name == "EncoderA":
            if changed_value > 0:
                self.increase_volume()
            elif changed_value < 0:
                self.decrease_volume()
        else:
            if changed_value > 0:
                #print("Value increased")
                kbd.press(Keycode.PERIOD)
                time.sleep(0.2)
                kbd.release(Keycode.PERIOD)
            elif changed_value < 0:
                #print("Value decreased")
                kbd.press(Keycode.COMMA)
                time.sleep(0.2)
                kbd.release(Keycode.COMMA)

    def increase_volume(self):
        print("Increasing volume.")
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)  

    def decrease_volume(self):
        print("Decreasing volume.")
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)  


#buttons on fret
button_A = Button(board.GP0, Keycode.A) #1
button_S = Button(board.GP2, Keycode.S) #2
button_D = Button(board.GP3, Keycode.D) #3
button_F = Button(board.GP1, Keycode.F) #4
button_G = Button(board.GP6, Keycode.G) #5
button_H = Button(board.GP7, Keycode.H) #6
button_J = Button(board.GP5, Keycode.J) #7
button_K = Button(board.GP4, Keycode.K) #8
button_L = Button(board.GP9, Keycode.L) #9
button_Z = Button(board.GP8, Keycode.Z) #10
button_X = Button(board.GP10, Keycode.X) #11
button_C = Button(board.GP11, Keycode.C) #12

#buttons on box
button_1 = Button(board.GP21, Keycode.ONE) 
button_2 = Button(board.GP20, Keycode.TWO)
button_3 = Button(board.GP18, Keycode.THREE) 
button_4 = Button(board.GP19, Keycode.FOUR)
button_5 = Button(board.GP17, Keycode.FIVE)
button_6 = Button(board.GP16, Keycode.SIX)

#potenciometers
potentiometer_a = Potentiometer(board.GP26, "PotA")
potentiometer_b = Potentiometer(board.GP27, "PotB")
potentiometer_c = Potentiometer(board.GP28, "PotC")

#encoders
encoder_a = Encoder(board.GP15, board.GP14, "EncoderA") 
encoder_b = Encoder(board.GP13, board.GP12, "EncoderB")
encoder_button = Button(board.GP22, Keycode.ZERO)

while True:
    #update buttons on fret
    button_A.update()
    button_S.update()
    button_D.update()
    button_F.update()
    button_G.update()
    button_H.update()
    button_J.update()
    button_K.update()
    button_L.update()
    button_Z.update()
    button_X.update()
    button_C.update()
    
    #update buttons on box
    button_1.update()
    button_2.update()
    button_3.update()
    button_4.update()
    button_5.update()  
    button_6.update()
    
    #update potenciometers
    potentiometer_a.update()
    potentiometer_b.update()
    potentiometer_c.update()
   
    #update encoders
    encoder_a.update()
    encoder_b.update()
    encoder_button.update()

    time.sleep(0.05)
#