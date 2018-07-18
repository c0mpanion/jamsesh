import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
import socket, threading
import pickle



kivy.require('1.10.0')
global username
global s

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



class UserInfoScreen(Screen):
    pass

class MainScreen(Screen):

    global s
    username = ""

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        #self.messages = self.ids["messages"]

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

if __name__ == "__main__":
    JamSeshApp().run()