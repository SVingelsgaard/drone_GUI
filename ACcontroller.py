import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.progressbar import ProgressBar
from kivy.lang.builder import Builder
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.core.text import Label as CoreLabel
from collections.abc import Iterable
from math import ceil
from kivy.core.text import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from cheats.joystick.joystick import Joystick

import pyfirmata
import cheats.circularProgressBar
import keyboard

#windowsize
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '669')
Config.set('graphics', 'height', '737')

#root class
class WindowManager(ScreenManager):
    pass

class StartScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class Home(Widget):
    pass

class ControlPanel(FloatLayout):
    pass

#henter kv fil
kv = Builder.load_file("graphics.kv")
class GUI(App):

    #variabels
    #for system
    setCYCLETIME = 0.02 #sec
    readCYCLETIME = 0

    #status
    online = False
    controlUnit = 'sliders' #same shit


    manX = 0
    manY = 0

    manLF = 0
    manRF = 0
    manLB = 0
    manRB = 0

    LFout = 0
    LBout = 0
    RFout = 0
    RBout = 0
    LFoutGui = 0
    LBoutGui = 0
    RFoutGui = 0
    RBoutGui = 0
    try:
        controller = pyfirmata.ArduinoNano('COM4')
        print("running in online mode")
        online = True
    except:
        print("no board connected on COM4 \nrunning inn offline mode")
        online = False




    if online:
        #map motors
        LF = controller.digital[5]
        RF = controller.digital[6]
        LB = controller.digital[4]
        RB = controller.digital[3]

        #configure motors
        LF.mode = pyfirmata.SERVO
        RF.mode = pyfirmata.SERVO
        LB.mode = pyfirmata.SERVO
        RB.mode = pyfirmata.SERVO

    #activating ich progressbars. prooly hella shit way,,, but okay.
    kv.ids.mScreen.ids.LFoutGui.value = 1
    kv.ids.mScreen.ids.RFoutGui.value = 1
    kv.ids.mScreen.ids.LBoutGui.value = 1
    kv.ids.mScreen.ids.RBoutGui.value = 1
    #cycle function. runs countniusly
    def cycle(self, readCYCLETIME):
        #init GUI variable (sliders, joystick, )
        self.manLF = self.root.ids.mScreen.ids.manLF.value
        self.manRF = self.root.ids.mScreen.ids.manRF.value
        self.manLB = self.root.ids.mScreen.ids.manLB.value
        self.manRB = self.root.ids.mScreen.ids.manRB.value

        self.manX = int(self.root.ids.mScreen.ids.joystick.pad[0] * 100)
        self.manY = int(self.root.ids.mScreen.ids.joystick.pad[1] * 100)

        #set HW variables (output, )
        if self.controlUnit == 'sliders':
            self.LFout = self.manLF
            self.RFout = self.manRF
            self.LBout = self.manLB
            self.RBout = self.manRB
        elif self.controlUnit == 'joystick':
            #50 will be "konstantledd" from separate hight output(prolly own pid idk)
            self.LFout = self.clamp((50 + ((self.manX/2)-(self.manY/2))*.5), 0, 100)
            self.RFout = self.clamp((50 - ((self.manX/2)+(self.manY/2))*.5), 0, 100)
            self.LBout = self.clamp((50 + ((self.manX/2)+(self.manY/2))*.5), 0, 100)
            self.RBout = self.clamp((50 - ((self.manX/2)-(self.manY/2))*.5), 0, 100)

        if self.online:
            #write HW variabels to HW (output, ) use int funtion maybe?
            self.LF.write(self.LFout*0.395 + 50)
            self.RF.write(self.RFout*0.395 + 50)
            self.LB.write(self.LBout*0.395 + 50)
            self.RB.write(self.RBout*0.395 + 50)

        #set GUI variabels
        self.root.ids.mScreen.ids.LFoutGui.value = int(self.LFout)
        self.root.ids.mScreen.ids.RFoutGui.value = int(self.RFout)
        self.root.ids.mScreen.ids.LBoutGui.value = int(self.LBout)
        self.root.ids.mScreen.ids.RBoutGui.value = int(self.RBout)

    #setts manual thurst / slider value to zero
    def turnOffThruster(self, id):
        if id == "LF":
            self.root.ids.mScreen.ids.manLF.value = 0
        elif id == "RF":
            self.root.ids.mScreen.ids.manRF.value = 0
        elif id == "LB":
            self.root.ids.mScreen.ids.manLB.value = 0
        elif id == "RB":
            self.root.ids.mScreen.ids.manRB.value = 0

    def setControllUnit(self, unit):
        self.controlUnit = unit

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    #runns cycle
    def runApp(self):
        Clock.schedule_interval(self.cycle, self.setCYCLETIME)

    #runs myApp(graphics)
    def build(self):
        return kv

#runs program and cycle
if __name__ == '__main__':
    GUI().run()
