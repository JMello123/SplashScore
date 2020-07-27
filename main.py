from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.config import Config
from kivy.metrics import dp
from kivy.lang.builder import Builder
from kivy.uix.popup import Popup

import json
import time

from controllerdrill import ControllerDrill


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

    def back_menu(self,window, key, *args):
            if key == 27:
                if self.current == 'drill':
                    self.get_screen('drill').exit_confirm()
                else:
                    App.get_running_app().root.current = 'menu'
                    self.transition.direction = "right"
            return True

        
class Menu(Screen):
    pass

class Drill(Screen):

    splash = NumericProperty(0)
    wrong = NumericProperty(0)
    percentage = NumericProperty(.0)

    def __init__(self,**kwargs):
        self.session = ControllerDrill()
        super().__init__(**kwargs)

    def on_pre_enter(self):
        Window.bind(on_keyboard=App.get_running_app().root.back_menu)
        self.session.reset_status()
        self.draw_balls(self.session.status['last_ten'])
        self.ids.points.text = '[size=33]0[/size]/0'
        self.ids.percentage.text = '0%'

    def on_pre_leave(self):
        Window.unbind(on_keyboard=App.get_running_app().root.back_menu)
        
    def on_splash(self,*args):
        self.ids.points.text = f"[size=33]{self.session.status['point']}[/size]"+'/'+str(self.session.status['attempt'])
        self.ids.percentage.text = str(round(self.session.status['accuracy']*100,1))+'%'

    def on_wrong(self,*args):
        self.ids.points.text = f"[size=33]{self.session.status['point']}[/size]"+'/'+str(self.session.status['attempt'])
        self.ids.percentage.text = str(round(self.session.status['accuracy']*100,1))+'%'

    def draw_balls(self, balls:list):
        self.ids.boxBall.clear_widgets()
        for ball in balls:
            if ball == 0:
                self.ids.boxBall.add_widget(Image(source='img/grey_ball.png'))
            if ball == 1:
                self.ids.boxBall.add_widget(Image(source='img/green_ball.png'))
            if ball == 2:
                self.ids.boxBall.add_widget(Image(source='img/red_ball.png'))
    
    def shot_splash(self):
        points, self.last_shots = self.session.increment_point()
        self.draw_balls(self.last_shots)
        self.splash = points['point']
        self.percentage = points['accuracy']

    def shot_wrong(self):
        points, self.last_shots = self.session.increment_error()
        self.draw_balls(self.last_shots)
        self.wrong = points['attempt']
        self.percentage = points['accuracy']

    def exit_confirm(self, *args):
        popup = PopupReturn(auto_dismiss=False)
        popup.open()

    def finish_session(self, *args):
        date = time.localtime()
        saved_date = f'{date.tm_mday}/{date.tm_mon}/{date.tm_year} {date.tm_hour}:{date.tm_min}'
        App.get_running_app().root.saveDrill(
            {'accuracy':self.session.status['accuracy'], 
                'points':self.session.status['point'], 
                'attempt':self.session.status['attempt'], 
                'best_sequence':self.session.status['best_sequence'],
                'worst_sequence':self.session.status['worst_sequence'],
                'date':saved_date})

class PopupReturn(Popup):
    pass


class SavedScore(Screen):

    def on_pre_enter(self):
        Window.bind(on_keyboard=App.get_running_app().root.back_menu)
        self.ids.box.clear_widgets()
        sessions = App.get_running_app().root.loadDrill()
        for session in sessions:
            self.ids.box.add_widget(SessionScore(session))
    
    def on_pre_leave(self):
        if App.get_running_app().root.current != 'saved_details': 
            # caso a screen mude para saved_details, não é necessario fazer o unbind do método 
            Window.unbind(on_keyboard=App.get_running_app().root.back_menu)


class SessionScore(BoxLayout):

    def __init__(self,session,**kwargs):
        super().__init__(**kwargs)
        self.ids.accuracy.text = str(round(session['accuracy']*100,1))+"%"
        self.ids.result.text = str(session['points'])+'/'+str(session['attempt'])
        self.ids.best_sequence.text = str(session['best_sequence'])
        self.ids.worst_sequence.text = str(session['worst_sequence'])
        self.ids.date.text = str(session['date'])


class SavedDetails(Screen):
    
    def on_pre_enter(self):
        self.handling_score()

    def on_pre_leave(self):
        Window.unbind(on_keyboard=App.get_running_app().root.back_menu)

    def handling_score(self):
        self.ids.averageAccuracy.text = 'Aproveitamento médio: '
        self.ids.totalPoints.text = 'Cestas feitas: '
        self.ids.totalAttempts.text = 'Aremessos feitos: '
        self.ids.bestAccuracy.text = 'Melhor aproveitamento: '
        self.ids.bestSequenceAllofTime.text = 'Maior sequência de acertos: '

        sessions = App.get_running_app().root.loadDrill()

        total_points = 0
        total_attempts = 0
        total_percentage = .0
        best_sequence = 0
        best_accuracy = .0
        
        for session in sessions:
            total_points += session['points']
            total_attempts += session['attempt']
            total_percentage += session['accuracy']
            if session['best_sequence'] > best_sequence:
                best_sequence = session['best_sequence']
            if session['accuracy'] > best_accuracy:
                best_accuracy = session['accuracy']
        average = total_percentage/len(sessions)

        self.ids.averageAccuracy.text += str(round(average*100, 1))+'%'
        self.ids.totalPoints.text += str(total_points)
        self.ids.totalAttempts.text += str(total_attempts)
        self.ids.bestAccuracy.text += str(round(best_accuracy*100,1))+'%'
        self.ids.bestSequenceAllofTime.text += str(best_sequence)


class Settings(Screen):
    pass


class Splashscore(App):

    def build(self):
        # importando e lendo manualmente o arquivo .kv para forçar a codificação utf-8 
        # e corrigir problemas de caracteres incompatíveis  
        Builder.load_string(open("splashscoreapp.kv", encoding="utf-8").read(), rulesonly=True)
        return Manager()

    
if __name__ == '__main__':
    Splashscore().run()