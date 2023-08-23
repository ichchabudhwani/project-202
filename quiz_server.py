import socket
from threading import Thread
import random
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address='127.0.0.1'
port=8000
server.bind((ip_address,port))
server.listen()
print("server is running....")
nicknames=[]
clients=[]
questions=[
    "1.What is an italian word for pie?\n a.mozarella\n b.pastry\n c.pizza\n d.patty"
    "2.water boils at 212 units at which scale? \n a.celcius\n b.farenhiet\n c. kelvin\n d.rakine"
    "3.which sea creatures has three hearts ?\n a.dolphin\n b.octopus\n c.seal\n d.walrus"
    "4.who was the famous character in our childhood rhyme associated with lamb? \n a.jack \n b.jonny\n c. marry \n d.mukesh"
    "5.how many bones does adult human have?\n a.209\n b.196 \n c.206\n.708"
    "6.how many wonders are there in world?\n a. 8 \n b. 9\n c. 7 \n d.1"
    "7.what element does not exist?\n a. Xf\n b. Re \n c.Se\n d. Pa"
    "8.how many states are there in India?\n a.29\n b. 28\n c. 26\n d.24"
    "9.who invented the bulb?\n a. A.G Bell \n b.Jhon Wick\n c. Thomas Edison\n d.G. Macroni"
    "10.who was the first Indian female astronout?\n a.Sunita Williams\n b. kalpana chawla\n c.both of them\n d.none of them"
    "11.what is the smallest continent?\n a.asia\n b. africa\n c. antartic\n d.australia"
    "12.how many players are in the field of base ball?\n a.6\n b.7\n c.9\n d. 8"
    "13.Hg stands for? \n a.mercury\n b.hulgerium\n c.Argenine\n d.Halfnium"
    "14.who gifted statue of liberty to US?\n a.Brazil\n b. france\n c.Wales\n d.germany"
    "15.which planet is closest to sun?\n a.Mercury\n b.pluto\n c.Earth\n d.jupiter"


]
answer=['c','b','b','c','c','c','a','a','a','b','d','d','a','b','a']

list_of_clients=[]
def broadcast(message,connection):
    for clients in list_of_clients:
        if clients !=connection:
            try:
                clients.send(message.encode("utf-8"))
            except:
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

    
def remove_question(index):
    questions.pop(index)
    answer.pop(index)
    
def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions)-1)
    random_questions=questions[random_index]
    random_answer=answer[random_index]
    conn.send(random_questions.encode('utf-8'))
    return random_index,random_questions,random_answer
def clientthread(conn, addr):
    score=0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("you will recieve a question.the answer to that question would be one of the a,b,c or d\n".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index,question,answer=get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                 if message.lower()== answer:
                    score+=1
                    conn.send(f"bravo!Your score is{score}\n\n".encode('utf-8'))
             
                 else:
                    conn.send("Incorrect answer! better luck next time!\n\n".encode('utf-8'))
                    remove_question(index)
                    index,question,answer=get_random_question_answer(conn)
            else:
                remove(conn)
        except:
            continue

while True:
    conn,addr=server.accept()
    list_of_clients.append(conn)
    print(addr[0]+"connected")
    new_thread = Thread(target= clientthread,args=(conn,addr))
    new_thread.start()
     
    conn.send("NICKNAME".encode("utf-8"))
    nickname=conn.recv(2048).decode("utf-8")
    nicknames.append(nickname)
  
    message="{} joined".format(nickname)

    broadcast(message,conn)
   