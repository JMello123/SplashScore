from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
import json
import time

class Manager(ScreenManager):
    pass

class Menu(Screen):
    pass

class Drill(Screen):
    
    data = []
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.point = 0
        self.attempt = 0
        self.accuracy =.0

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.back)
        self.loadDrill()

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back)

    def back(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'menu'
        return True

    def shot_splash(self, status):
        self.point += 1
        self.attempt += 1
        self.accuracy = self.point/self.attempt
        points = str(self.point)+'/'+str(self.attempt)+' -> '+str(round(self.accuracy*100,1))+'%'
        status.text = points

    def shot_wrong(self, status):
        self.attempt += 1
        self.accuracy = self.point/self.attempt
        points = str(self.point)+'/'+str(self.attempt)+' -> '+str(round(self.accuracy*100,1))+'%'
        status.text = points

    def loadDrill(self,*args):
        with open('saved_score.json','r') as saved_score:
            self.data = json.load(saved_score)

    def saveDrill(self, *args):
        date = time.localtime()
        saved_date = f'{date.tm_mday}/{date.tm_mon}/{date.tm_year}'
        self.data.append({'accuracy':self.accuracy, 'points':self.point, 'date':saved_date})
        with open('saved_score.json', 'w') as saved_score:
            json.dump(self.data, saved_score)


class SavedScore(Screen):
    pass

class Splashscore(App):
    def build(self):
        return Manager()
    

Splashscore().run()