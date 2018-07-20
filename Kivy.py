import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
import socket, threading
import pickle
import os



kivy.require('1.10.0')
global username
global s
global u

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class UserInfoScreen1(Screen):

    def decide_player_or_audience(self, value, value2):
        print ("Player: " + str(value))
        print ("Audience: " + str(value2))
        if value == True:
            return "UserInfoScreen2"
        else:
            return "MainScreenAudience"

    player = ObjectProperty(True)
    audience_member = ObjectProperty(False)


class UserInfoScreen2(Screen):
    def decide_instrument(self, value, value2, value3):
        if value == True:
            return "PianoScreen"
        elif value2 == True:
            return "GuitarScreen"
        elif value3 == True:
            return "BassScreen"

class PianoScreen(Screen):
    global s
    username = ""

    def __init__(self, **kwargs):
        super(PianoScreen, self).__init__(**kwargs)

    def on_enter(self):
        s.connect(('localhost', 9000))
        self.ids.chatroom.text = "You are connected to the chat! \n"
        threading.Thread(target=self.handle_messages).start()

    def send_message(self, message_to_send):
        try:
            temp = message_to_send.split(" ")
            username = temp[0]
            msg_without_username = temp[1:]
            print(msg_without_username)
            message_to_send_text = " ".join(msg_without_username)
            print(message_to_send_text)
            user_and_message = [username, message_to_send_text]

            total_data = pickle.dumps(user_and_message)
            s.sendto(total_data, ('localhost', 9000))
            self.ids.chatroom.text += '\n' + username + " > " + message_to_send_text

        except Exception as e:
            print("Error sending: ", e)

    def handle_messages(self):
        while True:
            try:
                data = s.recv(1024)
                data_list = pickle.loads(data)
                self.ids.chatroom.text += str('\n' + data_list[0]) + ' > ' + str(data_list[1])
            except Exception as e:
                print(e)

    def send_note(self, note):
        if note == 'C':
            print ("C was pressed")
        elif note == "C#":
            print("C# was pressed")
        elif note == 'D':
            print("D was pressed")
        elif note == 'D#':
            print("D# was pressed")
        elif note == 'E':
            print("E was pressed")
        elif note == 'F':
            print("F was pressed")
        elif note == "F#":
            print("F# was pressed")
        elif note == 'G':
            print("G was pressed")
        elif note == 'G#':
            print("G# was pressed")
        elif note == 'A':
            print("A was pressed")
        elif note == 'A#':
            print("A# was pressed")
        else:
            print("C+ was pressed")




class BassScreen(Screen):
    global s
    username = ""

    def __init__(self, **kwargs):
        super(BassScreen, self).__init__(**kwargs)

    def on_enter(self):
        s.connect(('localhost', 9000))
        self.ids.chatroom.text = "You are connected to the chat! \n"
        threading.Thread(target=self.handle_messages).start()

    def send_message(self, message_to_send):
        try:
            temp = message_to_send.split(" ")
            username = temp[0]
            msg_without_username = temp[1:]
            print(msg_without_username)
            message_to_send_text = " ".join(msg_without_username)
            print(message_to_send_text)
            user_and_message = [username, message_to_send_text]

            total_data = pickle.dumps(user_and_message)
            s.sendto(total_data, ('localhost', 9000))
            self.ids.chatroom.text += '\n' + username + " > " + message_to_send_text

        except Exception as e:
            print("Error sending: ", e)

class GuitarScreen(Screen):
    global s
    username = ""

    def __init__(self, **kwargs):
        super(GuitarScreen, self).__init__(**kwargs)

    def on_enter(self):
        s.connect(('localhost', 9000))
        self.ids.chatroom.text = "You are connected to the chat! \n"
        threading.Thread(target=self.handle_messages).start()

    def send_message(self, message_to_send):
        try:
            temp = message_to_send.split(" ")
            username = temp[0]
            msg_without_username = temp[1:]
            print(msg_without_username)
            message_to_send_text = " ".join(msg_without_username)
            print(message_to_send_text)
            user_and_message = [username, message_to_send_text]

            total_data = pickle.dumps(user_and_message)
            s.sendto(total_data, ('localhost', 9000))
            self.ids.chatroom.text += '\n' + username + " > " + message_to_send_text

        except Exception as e:
            print("Error sending: ", e)


    def handle_messages(self):
        while True:
            try:
                data = s.recv(1024)
                data_list = pickle.loads(data)
                self.ids.chatroom.text += str('\n' + data_list[0]) + ' > ' + str(data_list[1])
            except Exception as e:
                print(e)

    def send_audio(self, note):
        pass

class MainScreenAudience(Screen):

    global s
    username = ""

    def __init__(self, **kwargs):
        super(MainScreenAudience, self).__init__(**kwargs)

    def on_enter(self):
        s.connect(('localhost', 9000))
        self.ids.chatroom.text = "You are connected to the chat! \n"
        threading.Thread(target=self.handle_messages).start()

    def send_message(self, message_to_send):
        try:
            temp = message_to_send.split(" ")
            username = temp[0]
            msg_without_username = temp[1:]
            print(msg_without_username)
            message_to_send_text = " ".join(msg_without_username)
            print(message_to_send_text)
            user_and_message = [username, message_to_send_text]

            total_data = pickle.dumps(user_and_message)
            s.sendto(total_data, ('localhost', 9000))
            self.ids.chatroom.text += '\n' + username + " > " + message_to_send_text

        except Exception as e:
            print("Error sending: ", e)


    def handle_messages(self):
        while True:
            try:
                data = s.recv(1024)
                data_list = pickle.loads(data)
                self.ids.chatroom.text += str('\n' + data_list[0]) + ' > ' + str(data_list[1])
            except Exception as e:
                print(e)

class ScreenManagement(ScreenManager):
    username = StringProperty("")
    audience_member = ObjectProperty(True)
    player = ObjectProperty(False)
    instrument = StringProperty("")


sm = Builder.load_file("JamSesh.kv")

class JamSeshApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    JamSeshApp().run()