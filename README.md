# kingofthehill
Python Chess AI

TU Berlin Projekt KI - Eric Benschneider, Christoph Scherer, Alex Calli


Installation und Dependencies:


You need to have Python 3 (Prefarable 3.8) installed to run this code.

Also be sure to install numpy via

pip install numpy

if you havent already.



Play with and against the AI:


To play against the AI via GUI you need to start game.py and set single to True ("single=True")

That should launch the GUI and start the server.

Afterwards start client.py to set the AI.

Now you should be ready to play by clicking on the token you want to move and then on the field you want it to be.

To watch AI play against itself you need to start game.py with single set to False

Afterwards start client.py 2 times and have fun watching.


Watching the AI play against itself is also possible over the gameserver functionality provided over https://chess.df1ash.de/fen-viewer/spectate/

Therefore start tournament.py one time with 

asyncio.run(hello("ws://chess.df1ash.de:8025",0,True))

and another time with 

asyncio.run(hello("ws://chess.df1ash.de:8025",1,True)) 

If that dont work try using "koth" instead of "chess" in the URL


Finally you can join a tournament started by someone else at koth.df1ash.de via tournament.py

Therefore you need to change the last line to

#asyncio.run(hello("ws://koth.df1ash.de:8026",0))


At last you can test what moves the AI would make based on a FEN via test.py

just insert the FEN in FEN="" and start test.py

Also try adjusting the parameters for diffrent time limit or Quantity of best moves.




Geistiges Eigentum der Technischen Universität Berlin