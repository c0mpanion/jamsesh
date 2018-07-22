# Jam Sesh

Jam Sesh was written with Python 3.6 and uses the Kivy library as a GUI to provide users a virtual environment to “jam out” together with instruments such as piano, guitar, and bass along with the ability to communicate through a chat. Jam Sesh allows 10 players/audience members to communicate through the chat and as many players can jam together as wanted.


All players, including audience members and players, will connect to the server through UDP but will also have a connection through TCP for the chat portion of the application. The connection through UDP is done via the first audio message a player/audience member sends. Since the audience member does not have access to inputting audio, it will send a basic "An audience member has connected" message to the server to establish its "connection". I put connection in quotes to emphasize that UDP is connectionless, however, we need a basic list of clients along with their addresses in order to send each one UDP packets.

The chat uses TCP because we want to ensure that chat messages are received in the correct order so that users can communicate efficiently. All players and audience members can use the chat room. Clients will send text messages in the format (username + " > " + message) in order to be able to maintain a list of users that are currently connected via TCP.

# Installation

Please follow the installation steps for your operating system by visiting:
Windows: https://kivy.org/docs/installation/installation-windows.html
Mac OS X: https://kivy.org/docs/installation/installation-osx.html
Linux: https://kivy.org/docs/installation/installation-linux.html

If you are installing for Mac OS X, you may have errors with SoundLoader. This is due to Kivy not installing the correct codec for the players. You can fix this using Homebrew by running this script:

brew install gst-plugins-base --with-libvorbis


# Running Jam Sesh

First, change directories to the folder where the Jam Sesh source code is contained. Then, run Server.py first. After your server starts, you can then run each instance of Kivy.py.

