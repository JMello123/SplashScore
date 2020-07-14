from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.config import Config
from kivy.lang.builder import Builder

import json
import time

from controllerdrill import ControllerDrill

Config.read("config.ini")

class Manager(ScreenManager):

    data = []
     
    def loadDrill(self,*args):
        path = App.get_running_app().user_data_dir+'/'
        try:
            with open(path+'saved_score.json','r') as saved_score:
                    self.data = json.load(saved_score)
                    return self.data
        except FileNotFoundError:
            open(path+'saved_score.json','x')
            return self.data
        except json.JSONDecodeError:
            return []
        
    def saveDrill(self, savedata, *args):
        self.data = self.loadDrill()
        path = App.get_running_app().user_data_dir+'/'
        self.data.append(savedata)
        with open(path + 'saved_score.json', 'w') as saved_score:
            json.dump(self.data, saved_score)

        
class Menu(Screen):
    pass

class Drill(Screen):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.session = ControllerDrill()
        self.last_shots = [0,0,0,0,0,0,0,0,0,0]

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.back_menu)
        self.session.reset_status()
        self.draw_balls(self.last_shots)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back_menu)
        self.ids.status.text = '0/0'

    def draw_balls(self, balls:list):
        self.ids.boxBall.clear_widgets()
        for ball in balls:
            if ball == 0:
                self.ids.boxBall.add_widget(Image(source='img/grey_ball.png'))
            if ball == 1:
                self.ids.boxBall.add_widget(Image(source='img/green_ball.png'))
            if ball == 2:
                self.ids.boxBall.add_widget(Image(source='img/red_ball.png'))
    
    def shot_splash(self, status):
        points_text, self.last_shots = self.session.increment_point()
        self.draw_balls(self.last_shots)
        status.text = str(points_text)

    def shot_wrong(self, status):
        points_text, self.last_shots = self.session.increment_error()
        self.draw_balls(self.last_shots)
        status.text = str(points_text)

    def finish_session(self, *args):
        date = time.localtime()
        saved_date = f'{date.tm_mday}/{date.tm_mon}/{date.tm_year} {date.tm_hour}:{date.tm_min}'
        App.get_running_app().root.saveDrill(
            {'accuracy':self.session.status['accuracy'], 
                'points':self.session.status['point'], 
                'best_sequence':self.session.status['best_sequence'],
                'worst_sequence':self.session.status['worst_sequence'],
                'date':saved_date})

    def back_menu(self, window, key, *args):
            if key == 27:
                App.get_running_app().root.current = 'menu'
                self.ids.status.text = '0/0'
            return True



class SavedScore(Screen):

    def on_pre_enter(self):
        self.ids.box.clear_widgets()
        sessions = App.get_running_app().root.loadDrill()
        for session in sessions:
            self.ids.box.add_widget(SessionScore(session))
    
    
class SessionScore(BoxLayout):

    def __init__(self,session,**kwargs):
        super().__init__(**kwargs)
        self.ids.accuracy.text = str(round(session['accuracy']*100,1))+"%"
        self.ids.splash.text = str(session['points'])
        self.ids.best_sequence.text = str(session['best_sequence'])
        self.ids.date.text = str(session['date'])


            

    
class Splashscore(App):

    def build(self):
        # importando e lendo manualmente o arquivo kv para forçar a codificação utf-8 
        # e corrigir problemas de caracteres incompatíveis  
        Builder.load_string(open("splashscoreapp.kv", encoding="utf-8").read(), rulesonly=True)
        return Manager()

    
if __name__ == '__main__':
    Splashscore().run()