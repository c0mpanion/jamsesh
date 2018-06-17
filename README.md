# Jam Sesh

Jam Sesh provides users a virtual environment to “jam out” together with instruments such as piano, guitar, bass, and drums along with the ability to communicate through a chat. A minimum of 2 players and a maximum of 5 players can jam simultaneously, but the server can handle 10 clients at once including audience members who can watch the jam sesh or communicate to the others via the chat.


All players, including audience members and players, will connect through UDP but will also have a connection through TCP for the chat portion of the application. Each client will make a unique username (but no password, as data will not be saved from the session) in order to be able to differentiate between players. This is to improve performance for the audio and graphical portion of the application, since TCP will ensure all packets are there and will request the packets again if there is data missing. The chat will use TCP because we want to ensure that chat messages are received in the correct order so that users can communicate efficiently. In addition, if there is time, chat messages can be encrypted to ensure security between players.

Jam Sesh will use Kivy as its graphical interface.
