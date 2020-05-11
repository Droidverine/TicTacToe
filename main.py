import os
import time
import uuid
from firebase  import firebase
from flask import Flask,render_template,url_for,request,redirect

ct=0

firebase=firebase.FirebaseApplication('https://tictactoe-eac99.firebaseio.com/',None)

app= Flask(__name__)
@app.route('/')
def hello():
    pl=request.args.get("turn")



    data=firebase.get('/game/','')
    if(data!=None):
        board=list(data)
    else:
        data={
            '0':' ',
            '1':' ',
            '2':' ',
            '3':' ',
            '4':' ',
            '5':' ',
            '6':' ',
            '7':' ',
            '8':' ',
            '9':' ',
        }
        firebase.put('/game/','/',data)
        print('init')
        data=firebase.get('/game/','')
        board=list(data)
    print(board)
    player = 1
    if(pl!=None):
        player=int(pl)


    ########win Flags##########
    Win = 1
    Draw = -1
    Running = 0
    Stop = 1
    ###########################
    Game = Running
    Mark = 'X'
    global Game
    status=''

    if(board[0]== ' ' and board[1]==' ' and board[2]==' ' and board[3]==' ' and board[4]==' ' and board[5]==' ' and board[6]==' ' and board[7]==' ' and board[8]==' ' and board[9]==' '):
        data={
            '0':' ',
            '1':' ',
            '2':' ',
            '3':' ',
            '4':' ',
            '5':' ',
            '6':' ',
            '7':' ',
            '8':' ',
            '9':' ',
        }
        firebase.put('/game/','/',data)
        print('init')
    elif(board[0] !=' ' or board[1]!=' ' or board[2]!=' ' or board[3]!=' ' or board[4]!=' ' or board[5]!=' ' or board[6]!=' ' or board[7]!=' ' or board[8]!=' ' or board[9]!=' '):
        print('noint')
        #Horizontal winning condition
        if(board[1] == board[2] and board[2] == board[3] and board[1] != ' '):
            Game = Win
        elif(board[4] == board[5] and board[5] == board[6] and board[4] != ' '):
            Game = Win
        elif(board[7] == board[8] and board[8] == board[9] and board[7] != ' '):
            Game = Win
        #Vertical Winning Condition
        elif(board[1] == board[4] and board[4] == board[7] and board[1] != ' '):
            Game = Win
        elif(board[2] == board[5] and board[5] == board[8] and board[2] != ' '):
            Game = Win
        elif(board[3] == board[6] and board[6] == board[9] and board[3] != ' '):
            Game=Win
        #Diagonal Winning Condition
        elif(board[1] == board[5] and board[5] == board[9] and board[5] != ' '):
            Game = Win
        elif(board[3] == board[5] and board[5] == board[7] and board[5] != ' '):
            Game=Win
        #Match Tie or Draw Condition
        elif(board[1]!=' ' and board[2]!=' ' and board[3]!=' ' and board[4]!=' ' and board[5]!=' ' and board[6]!=' ' and board[7]!=' ' and board[8]!=' ' and board[9]!=' '):
            Game=Draw
        else:
            Game=Running

        if(Game == Running):
            if(player % 2 != 0):
                print("Player 1's chance")
                Mark = 'X'
            else:
                print("Player 2's chance")
                Mark = 'O'
        #    choice = int(input("Enter the position between [1-9] where you want to mark : "))


        if(Game==Draw):
            status='draw'
        elif(Game==Win):
            if(player%2!=0):
                print("Player 0 Won")
                status="Player 0 Won"
            else:
                print("Player X Won")
                status="Player X Won"


        print(Game)
    return render_template('board.html',boardm=board,player=player,status=status)

#id = str(uuid.uuid1())

@app.route('/move')
def move():
    data=firebase.get('/game/','')
    board=list(data)
    Mark='X'
    l=request.args.get("block")
    player=int(request.args.get("turn"))
    l=int(l)
    print(l)
    if(player % 2 != 0):
        print("Player 1's chance")
        Mark = 'X'
    else:
        print("Player 2's chance")
        Mark = 'O'
    if(board[l]== ' '):
        firebase.put('/game/','/'+str(l),''+str(Mark))
        player=player+1
        data=firebase.get('/game/','')
    return redirect(url_for('.hello', turn=player))
     #return render_template('board.html',boardm=data,player=player)


if __name__=="__main__":
     app.run(debug=True)
