import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.progressbar import ProgressBar
from kivy.lang.builder import Builder
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.text import Label as CoreLabel
from collections.abc import Iterable
from math import ceil
from kivy.core.text import Label

#windowsize
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '771')

class myApp(Widget):
    pass

class StartScreen(Button):
    pass

class Home(Widget):
    pass

class ControlPanel(FloatLayout):
    pass

class manualPowerInput(Slider):
    pass

#everythiong under i think i need.

#no clue wtf happening


class GUI(App):
    #variabels
    setCYCLETIME = 0.02 #sec
    readCYCLETIME = 0

    manLF = 0
    manRF = 0
    manLB = 0
    manRB = 0

    #cycle function. runs countniusly
    def cycle(self, readCYCLETIME):
        self.manLF = self.root.ids.manLF
        self.manRF = self.root.ids.manRF
        self.manLB = self.root.ids.manLB
        self.manRB = self.root.ids.manRB

    #setts manual thurst / slider value to zero
    def turnOffThruster(self, id):
        if id == "LF":
            self.manLF.value = 0
        elif id == "RF":
            self.manRF.value = 0
        elif id == "LB":
            self.manLB.value = 0
        elif id == "RB":
            self.manRB.value = 0

    #runns cycle
    def runApp(self):
        Clock.schedule_interval(self.cycle, self.setCYCLETIME)

    #runs myApp(graphics)
    def build(self):
        return myApp()

#runs program and cycle
if __name__ == '__main__':
    GUI().run()
