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

class Drill(Screen):
    pass

class ScoreSplash(App):
    def build(self):
        self.point = 0
        self.attempt = 0
        self.accuracy =.0

        # splash = Image(source='src/splash.png')
        # wrong = Image(source='src/wrong.png')
        self.counter = Label(text='0/0', font_size=30)
        splash = Button(text='acertou', font_size=30, on_press=self.shot)
        wrong = Button(text='errou', font_size=30, on_press=self.shot)
        layoutButton = BoxLayout()
        layoutButton.add_widget(self.counter)
        layoutButton.add_widget(splash)
        layoutButton.add_widget(wrong)
        return layoutButton
    
    def shot(self, button):
        status = str(self.point)+'/'+str(self.attempt)+' -> '+str(round(self.accuracy*100,1))+'%'
        if button.text == 'acertou':
            self.point += 1
            self.attempt += 1
            self.accuracy = self.point/self.attempt
            self.counter.text = status
        if button.text == 'errou':
            self.attempt += 1
            self.accuracy = self.point/self.attempt
            self.counter.text = status


ScoreSplash().run()