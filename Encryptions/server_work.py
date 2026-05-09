import chatlib
import socket
import select

questions = {}
logged_users = {}
ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"
text_file = r'your_file.txt'
users_dict = {}
default_score = "0"
def build_and_send_message(conn, code, msg):
    ## copy from client
    full_msg =  chatlib.build_message(code, msg)
    conn.send(full_msg.encode())
    print("[SERVER] ", full_msg)  # Debug print


def recv_message_and_parse(conn):
    ## copy from client
    full_msg = conn.recv(1024).decode()
    print("[CLIENT] ", full_msg)  # Debug print
    if full_msg == "":
        print("Connection closed by server")
        return None, None
    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data







def load_user_database():
    with open(text_file, 'r') as file:
        for line in file:
            values = line.strip().split(':')
            if len(values) == 2:
                key,value = values[0],values[1]
                password,score = value.split(',')
                users_dict[key.strip()] = password.strip(),score.strip()
            else:
                continue
    return users_dict

def add_users(username,password):
    try:
        with open('your_file.txt', 'a') as file:
            file.write(username+":"+password+","+default_score+'\n')
        print("Content appended successfully.")
    except FileNotFoundError:
        print(f"Error: The file 'your_file.txt' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# SOCKET CREATOR

def setup_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen()
    """
    Creates new listening socket and returns it
    Recieves: -
    Returns: the socket object
    """
    # Implement code ...

    return sock




def send_error(conn, error_msg):
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER['error_msg'], error_msg)

    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
# Implement code ...




##### MESSAGE HANDLING


def handle_getscore_message(conn, username):
    global file
    global users_dict
    if username in users_dict:
        score = users_dict[username][1]
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER['score_msg'], str(score))
    else:
        send_error(conn, "User not found")

def handle_highscore_message(conn):
    global file
    global users_dict
    scores = {}
    print(scores)
    for item in users_dict:
        score = int((users_dict[item])[1])
        scores[item] = score
    sort_scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    print(sort_scores)
    msg = ""
    for i, (name, score) in enumerate(sort_scores.items(), 1):
        msg += f"{i}. {name} - {score}\n"
    print(msg)
    build_and_send_message(conn,chatlib.PROTOCOL_SERVER['highscore_msg'],msg)

def add_score(conn,username):
    global file
    global users_dict
    score = int(users_dict[username][1])
    new_score = score + 1
    users_dict[username][1] = new_score

def handle_logout_message(conn,client_sockets):

    global logged_users
    if conn in logged_users:
        username = logged_users[conn]
        print(f"User '{username}' logged out.")
        del logged_users[conn]
    conn.close()
    if conn in client_sockets:
        client_sockets.remove(conn)
    conn.close()



def handle_login_message(conn, data):
    global users_dict  # This is needed to access the same users dictionary from all functions
    global logged_users	 # To be used later
    users = load_user_database()
    msg,num,details = data.split("|")
    username, password = details.split("#")
    print("the username and password is"+username,password)
    if username in users:
        print('username in users')
        print((users_dict[username])[0])
        if password == ((users_dict[username])[0]):
            print('password is correct')
            logged_users[conn] = username
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER['login_ok_msg'], '')
        else:
            print('Password does not match!')
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER['error_msg'], 'Password does not match!')
    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER['error_msg'], 'Username does not exist!')

def handle_register_message(conn, data):
    global users_dict  # This is needed to access the same users dictionary from all functions
    global logged_users	 # To be used later
    users = load_user_database()
    msg,num,details = data.split("|")
    username, password = details.split("#")
    if username not in users_dict:
        print('registration approved')
        add_users(username,password)
        users_dict[username] = password
        print('added the data')
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER['register_ok_msg'], '')
        logged_users[conn] = username
    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER['error_msg'], 'Username/password already exist!')


def handle_client_message(conn, cmd, data):
    print("handling messages")
    if cmd == chatlib.PROTOCOL_CLIENT['login_msg']:
        print("you chose to login")
        handle_login_message(conn,data)
    elif cmd == chatlib.PROTOCOL_CLIENT['register_msg']:
        print("you chose to register")
        handle_register_message(conn,data)
    else:
        send_error(conn,'unknown command')


def change_score(username, new_score):
    with open('your_file.txt', 'r') as file:
        lines = file.readlines()

    with open('your_file.txt', 'w') as file:
        for line in lines:
            parts = line.strip().split(':')
            if parts[0] == username:
                password, score = parts[1].split(',')
                if new_score > int(score):
                    line = f"{username}:{password},{new_score}\n"
            file.write(line)
change_score(username="test", new_score=3)

def main():
    # Initializes global users and questions dicionaries using load functions, will be used later
    global users_dict
    global questions
    global logged_users
    conn = setup_socket()
    print("Welcome to Trivia Server!")
    client_sockets = []

    while True:
        ready_to_read, ready_to_write, in_error = select.select([conn] + client_sockets, [], [])
        for current_socket in ready_to_read:
            if current_socket is conn:
                (client_socket, client_address) = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(client_socket)
            else:
                try:
                    print("New data from client")
                    data = current_socket.recv(1024).decode()
                    if not data:
                        print("Client disconnected unexpectedly")
                        handle_logout_message(current_socket,client_sockets)
                        continue
                    cmd , msg = chatlib.parse_message(data)
                    print(cmd,msg)
                    if cmd == chatlib.PROTOCOL_CLIENT['logout_msg']:
                        print("Client requested logout")
                        handle_logout_message(current_socket,client_sockets)
                    elif cmd == chatlib.PROTOCOL_CLIENT['get_score_msg']:
                        if current_socket in logged_users:
                            username = logged_users[current_socket]
                            print(username)
                            handle_getscore_message(current_socket, username)
                        else:
                            send_error(current_socket, "You must be logged in to get a score.")
                    elif cmd == chatlib.PROTOCOL_CLIENT['get_highscore_msg']:
                        print("getting highscore")
                        handle_highscore_message(current_socket)
                    else:
                        print("logging in or registering")
                        handle_client_message(current_socket,cmd,data)
                except (ConnectionResetError, ConnectionAbortedError):
                    print("⚠️ Client connection aborted")
                    client_sockets.remove(current_socket)
                    current_socket.close()






