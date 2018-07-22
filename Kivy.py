import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
import socket, threading
import pickle
from kivy.core.audio import SoundLoader
import time
from socket import error as socket_error


kivy.require('1.10.0')
global username
global s
global u
u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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
        threading.Thread(target=self.receive_audio).start()


    def send_message(self, message_to_send):
        try:
            temp = message_to_send.split(" ")
            username = temp[0]
            msg_without_username = temp[1:]
            message_to_send_text = " ".join(msg_without_username)
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
            except EOFError:
                s.close()
                self.ids.chatroom.text += ("\nYou were disconnected from the chatroom. Log in again.")
                print("Disconnected from the chatroom.")
                break

    def send_note(self, note):
        notes = {"C": "Piano_Sounds/C.wav", "C#": "Piano_Sounds/C#.wav", "C+": "Piano_Sounds/C+.wav",
                 "D": "Piano_Sounds/D.wav", "D#": "Piano_Sounds/D#.wav",
                 "E": "Piano_Sounds/E.wav", "F": "Piano_Sounds/F.wav", "F#": "Piano_Sounds/F#.wav",
                 "G": "Piano_Sounds/G.wav", "G#": "Piano_Sounds/G#.wav",
                 "A": "Piano_Sounds/A.wav", "A#": "Piano_Sounds/A#.wav",
                 "B": "Piano_Sounds/B.wav", "B#": "Piano_Sounds/B#.wav"}

        path = notes[note]
        sound = SoundLoader.load(path)
        sound.play()
        u.sendto(path.encode('utf-8'), ('localhost', 9001))

    def receive_audio(self):
        while True:
            data, addr = u.recvfrom(1024)
            data = data.decode("utf-8")
            print("Received audio: " + data)
            sound = SoundLoader.load(data)
            time.sleep(0.2)
            sound.play()


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

    def handle_messages(self):
        while True:
            try:
                data = s.recv(1024)
                data_list = pickle.loads(data)
                self.ids.chatroom.text += str('\n' + data_list[0]) + ' > ' + str(data_list[1])
            except socket_error:
                s.close()
                self.ids.chatroom.text += ("You were disconnected from the chatroom. Log in again.")
                print("Disconnected from the chatroom.")
                break

    def send_note(self, note):
        notes={"C": "Bass_Sounds/C.wav", "C#": "Bass_Sounds/C#.wav", "C+": "Bass_Sounds/C+.wav",
               "D": "Bass_Sounds/D.wav", "D#": "Bass_Sounds/D#.wav",
               "E": "Bass_Sounds/E.wav", "F": "Bass_Sounds/F.wav", "F#": "Bass_Sounds/F#.wav",
               "G": "Bass_Sounds/G.wav", "G#": "Bass_Sounds/G#.wav",
               "A": "Bass_Sounds/A.wav", "A#": "Bass_Sounds/A#.wav",
               "B": "Bass_Sounds/B.wav", "B#": "Bass_Sounds/B#.wav"}

        path = notes[note]
        sound = SoundLoader.load(path)
        sound.play()
        u.sendto(path.encode('utf-8'), ('localhost', 9001))

    def receive_audio(self):
        while True:
            data, addr = u.recvfrom(1024)
            data = data.decode("utf-8")
            print("Received audio: " + data)
            sound = SoundLoader.load(data)
            time.sleep(0.2)
            sound.play()

class GuitarScreen(Screen):
    global s
    username = ""
    def __init__(self, **kwargs):
        super(GuitarScreen, self).__init__(**kwargs)

    def on_enter(self):
        s.connect(('localhost', 9000))
        self.ids.chatroom.text = "You are connected to the chat! \n"
        threading.Thread(target=self.handle_messages).start()
        threading.Thread(target=self.receive_audio).start()

    def send_message(self, message_to_send):
        try:
            temp = message_to_send.split(" ")
            username = temp[0]
            msg_without_username = temp[1:]
            message_to_send_text = " ".join(msg_without_username)
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
            except socket_error:
                s.close()
                self.ids.chatroom.text += "You were disconnected from the chatroom. Log in again."
                print("Disconnected from the chatroom.")
                break

    def send_note(self, note):
        notes = {"C": "Guitar_Sounds/C.wav", "C#": "Guitar_Sounds/C#.wav", "C+": "Guitar_Sounds/C+.wav",
                 "D": "Guitar_Sounds/D.wav", "D#": "Guitar_Sounds/D#.wav",
                 "E": "Guitar_Sounds/E.wav", "F": "Guitar_Sounds/F.wav", "F#": "Guitar_Sounds/F#.wav",
                 "G": "Guitar_Sounds/G.wav", "G#": "Guitar_Sounds/G#.wav",
                 "A": "Guitar_Sounds/A.wav", "A#": "Guitar_Sounds/A#.wav",
                 "B": "Guitar_Sounds/B.wav", "B#": "Guitar_Sounds/B#.wav"}

        path = notes[note]
        sound = SoundLoader.load(path)
        sound.play()
        u.sendto(path.encode('utf-8'), ('localhost', 9001))

    def receive_audio(self):
        while True:
            data, addr = u.recvfrom(1024)
            data = data.decode("utf-8")
            print("Received audio: " + data)
            sound = SoundLoader.load(data)
            time.sleep(0.2)
            sound.play()

    def handle_messages(self):
        while True:
            try:
                data = s.recv(1024)
                data_list = pickle.loads(data)
                self.ids.chatroom.text += str('\n' + data_list[0]) + ' > ' + str(data_list[1])
            except socket_error:
                s.close()
                self.ids.chatroom.text += ("You were disconnected from the chatroom. Log in again.")
                print("Disconnected from the chatroom.")
                break

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
        path = "Misc/AudienceMember.wav"
        path = path.encode("utf-8")
        u.sendto(path, ("localhost", 9001))
        threading.Thread(target=self.receive_audio).start()

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
            except socket_error:
                s.close()
                self.ids.chatroom.text += ("You were disconnected from the chatroom. Log in again.")
                print ("Disconnected from the chatroom.")
                break

    def receive_audio(self):
        while True:
            data, addr = u.recvfrom(1024)
            data = data.decode("utf-8")
            print("Received audio: " + data)
            sound = SoundLoader.load(data)
            time.sleep(1)
            sound.play()


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