import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.popup import Popup
from kivy.properties import StringProperty


kivy.require('1.10.0')

class MainScreen(Screen):
    def send_username(self):
        self.ids.chatroom.text = "Username was sent"
        self.ids.chatroom.text = "Username is " + self.ids.msg_input.text

    def send_audio(self):
        pass

class ScreenManagement(ScreenManager):
    pass


sm = Builder.load_file("JamSesh.kv")

class JamSeshApp(App):
    def build(self):
        return sm

JamSeshApp().run()