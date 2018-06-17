import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.popup import Popup
from kivy.properties import StringProperty


kivy.require('1.10.0')

class UserInfoScreen(Screen):
    def input_username(self, text):
        if not text:
            popup = Popup(title='Error: no username', content=Label(text='Please enter a username'),
                  size=(200, 200))
            popup.open()
        else:
            text = StringProperty()

class MainScreen(Screen):
    def send_message(self):
        pass

    def send_audio(self):
        pass

class ScreenManagement(ScreenManager):
    pass


sm = Builder.load_file("JamSesh.kv")

class JamSeshApp(App):
    def build(self):
        return sm

JamSeshApp().run()