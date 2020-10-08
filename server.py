import socket 
import select 
import sys 
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = '127.0.0.1'
  
Port = 65432

server.bind((IP_address, Port)) 
server.listen(100) 
  
list_of_clients = [] 
  
def clientthread(conn, addr): 
  conn.send("Bem-vindo ao bate-papo.\nComandos:\n/users: Lista os usuarios online\n ") 

  while True: 
    try: 
      message = conn.recv(2048) 
      if message: 

        if ('/users' in str(message)):
          conn.send('<server>Usuarios online:')
          for client in list_of_clients:
            client_addr = client['addr']
            if (client['conn'] == conn):
              conn.send('\n<server>' + client_addr[0] + ':' + str(client_addr[1]) + '(Local)')
            else:
              conn.send('\n<server>' + client_addr[0] + ':' + str(client_addr[1]))
          
        elif ('/msg' == str(message).split(' ')[0]):
          words = (str(message)).split(' ')
          to = words[1]
          true_message = ' '.join(words[2:]) 

          message_to_send = "<" + addr[0] + ":" + str(addr[1]) + "> " + true_message
          send_message(message_to_send, to) 

      else: 
        remove(conn) 

    except: 
        continue
  

def send_message(message, to): 
  for clients in list_of_clients: 
    if ((clients['addr'][0] + ':' + str(clients['addr'][1])) == to): 
      try: 
        print('Enviando mensagem')
        clients['conn'].send(message) 
      except: 
        clients.conn.close() 
        remove(clients) 

def remove(connection): 
  for client in list_of_clients:
    if client.conn == connection:
      list_of_clients.remove(client)

while True: 
  
    conn, addr = server.accept() 
  
    list_of_clients.append({'conn': conn, 'addr': addr}) 
  
    print (addr[0] + ":" + str(addr[1]) + " connected")
  
    threading.Thread(target=clientthread, args=(conn,addr)).start()
  
conn.close() 
server.close() 