from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty
from kivy.uix.label import Label
import json
import time

class Manager(ScreenManager):

    sessions = []
    def loadDrill(self,*args):
        path = App.get_running_app().user_data_dir+'/'
        try:
            with open(path+'saved_score.json','r') as saved_score:
                self.sessions = json.load(saved_score)
                return self.sessions
        except FileNotFoundError:
            open(path+'saved_score.json','x')
        
    
class Menu(Screen):
    pass

class Drill(Screen):
    
    data = []

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.point = 0
        self.attempt = 0
        self.accuracy =.0

    def reset_status(self):
        self.point = 0
        self.attempt = 0
        self.accuracy =.0
        self.ids.status.text = '0/0'

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.back_menu)
        
        self.data = App.get_running_app().root.loadDrill()
        # print(path)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back_menu)

    def saveDrill(self, *args):
        date = time.localtime()
        saved_date = f'{date.tm_mday}/{date.tm_mon}/{date.tm_year} {date.tm_hour}:{date.tm_min}'
        path = App.get_running_app().user_data_dir+'/'
        self.data.append({'accuracy':self.accuracy, 
                          'points':self.point, 
                          'date':saved_date})
        with open(path + 'saved_score.json', 'w') as saved_score:
            json.dump(self.data, saved_score)
        self.reset_status()

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

    def back_menu(self, window, key, *args):
            if key == 27:
                App.get_running_app().root.current = 'menu'
            return True


class SavedScore(Screen):

    data = []
    def on_pre_enter(self):
        self.data = App.get_running_app().root.loadDrill()
        for session in self.data:
            self.ids.box.add_widget(SessionScore(session))
            

class SessionScore(BoxLayout):

    def __init__(self,session,**kwargs):
        super().__init__(**kwargs)
        self.ids.accuracy.text = str(round(session['accuracy']*100,1))+"%"
        self.ids.splash.text = str(session['points'])
        self.ids.best_sequence.text = 'Nada, ainda!'
        self.ids.date.text = str(session['date'])

class Splashscore(App):
    def build(self):
        return Manager()

    
if __name__ == '__main__':
    Splashscore().run()