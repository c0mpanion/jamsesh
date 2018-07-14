import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty


kivy.require('1.10.0')
global user

class UserInfoScreen(Screen):
    pass

class MainScreen(Screen):

    def send_username(self):
        user = self.ids.username.text

    def send_audio(self):
        pass

class ScreenManagement(ScreenManager):
    username = StringProperty("")
    audience_member = ObjectProperty(True)
    player = ObjectProperty(False)


sm = Builder.load_file("JamSesh.kv")

class JamSeshApp(App):
    def build(self):
        return sm

JamSeshApp().run()