from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image

class Manager(ScreenManager):
    pass

class Menu(Screen):
    pass

class Drill(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.point = 0
        self.attempt = 0
        self.accuracy =.0

    def shot(self, button, status):
        if button.background_normal == 'img/splash.png':
            self.point += 1
            self.attempt += 1
            self.accuracy = self.point/self.attempt
        if button.background_normal == 'img/wrong.png':
            self.attempt += 1
            self.accuracy = self.point/self.attempt

        points = str(self.point)+'/'+str(self.attempt)+' -> '+str(round(self.accuracy*100,1))+'%'
        status.text = points

class Splashscore(App):
    def build(self):
        return Drill()
    

Splashscore().run()