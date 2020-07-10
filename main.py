from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty
from kivy.uix.label import Label
import json
import time

class Manager(ScreenManager):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.status = {
            'point': 0,
            'attempt':0,
            'accuracy':.0,
            'sequence':[0,0],
            'best_sequence':0,
            'worst_sequence':0 
        }
        self.data = []

    def increment_point(self,*args):
        self.status['point'] += 1
        self.status['attempt'] += 1
        self.status['accuracy'] = self.status['point']/self.status['attempt']
        self.status['sequence'][0] += 1
        self.status['sequence'][1] = 0
        self.check_sequence()
        text = str(self.status['point'])+ '/' +str(self.status['attempt']) + ' -> ' + str(round(self.status['accuracy']*100,1))+ '%'
        print(self.status)
        return text

    def increment_error(self, *args):
        self.status['attempt'] += 1
        self.status['accuracy'] = self.status['point']/self.status['attempt']
        self.status['sequence'][0] = 0
        self.status['sequence'][1] += 1
        self.check_sequence()
        text = str(self.status['point'])+ '/' +str(self.status['attempt']) + ' -> ' + str(round(self.status['accuracy']*100,1))+ '%'
        print(self.status)
        return text
        
    def check_sequence(self):
            if self.status['sequence'][0] > self.status['best_sequence']:
                self.status['best_sequence'] = self.status['sequence'][0]
            if self.status['sequence'][1] > self.status['worst_sequence']:
                self.status['worst_sequence'] = self.status['sequence'][1]
        
    def reset_status(self):
        self.status['point'] = 0
        self.status['attempt'] = 0
        self.status['accuracy'] = .0
        
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
        
    def saveDrill(self, *args):
        date = time.localtime()
        saved_date = f'{date.tm_mday}/{date.tm_mon}/{date.tm_year} {date.tm_hour}:{date.tm_min}'
        path = App.get_running_app().user_data_dir+'/'
        self.data.append({'accuracy':self.status['accuracy'], 
                          'points':self.status['point'], 
                          'date':saved_date})
        with open(path + 'saved_score.json', 'w') as saved_score:
            json.dump(self.data, saved_score)
        self.reset_status()
        
    
class Menu(Screen):
    pass

class Drill(Screen):
    
    def on_pre_enter(self):
        Window.bind(on_keyboard=self.back_menu)
        # App.get_running_app().root.loadDrill()

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back_menu)
        self.ids.status.text = '0/0'

    def shot_splash(self, status):
        points_text = App.get_running_app().root.increment_point()
        status.text = str(points_text)

    def shot_wrong(self, status):
        points_text = App.get_running_app().root.increment_error()
        status.text = str(points_text)

    def back_menu(self, window, key, *args):
            if key == 27:
                App.get_running_app().root.current = 'menu'
                self.ids.status.text = '0/0'
            return True


class SavedScore(Screen):

    def on_pre_enter(self):
        self.ids.box.clear_widgets()
        sessions = App.get_running_app().root.loadDrill()
        print(sessions)
        for session in sessions:
            self.ids.box.add_widget(SessionScore(session))
    
    
class SessionScore(BoxLayout):

    def __init__(self,session,**kwargs):
        super().__init__(**kwargs)
        self.ids.accuracy.text = str(round(session['accuracy']*100,1))+"%"
        self.ids.splash.text = str(session['points'])
        self.ids.best_sequence.text = 'Nada ainda'
        self.ids.date.text = str(session['date'])

    


class Splashscore(App):

    def build(self):
        return Manager()

    
if __name__ == '__main__':
    Splashscore().run()