import socket
import chatlib

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


def build_and_send_message(conn, code, data):
    protocol_msg =  chatlib.build_message(code, data)
    conn.send(protocol_msg.encode())
    print("[CLIENT] Sent:", protocol_msg)



def recv_message_and_parse(conn):
    full_msg = conn.recv(1024).decode()
    if full_msg == "":
        print("Connection closed by server")
        return None, None
    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data




def connect(server_ip,server_port):
    # Implement Code
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((server_ip, server_port))
    print("client connected to the server")
    return my_socket


def error_and_exit(error_msg):
    # Implement code
    print("Error:", error_msg)
    exit()


def login(conn):
    while True:
        start = input("login or register")
        if start.upper() == "L":
            print('you chose login')
            username = input("Please enter username: \n")
            password = input("Please enter password: \n")
            data = chatlib.join_data([username, password])
            build_and_send_message(conn, chatlib.PROTOCOL_CLIENT['login_msg'], data)
            cmd, msg = recv_message_and_parse(conn)
            print(username,password)
            if cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
                print("Login successful!")
                return
            elif cmd == chatlib.PROTOCOL_SERVER["login_failed_msg"]:
                print("Login failed:", msg)
                print("Please try again...\n")
            else:
                print("Unexpected response from server:", cmd, msg)
        elif start.upper() == "R":
            print('you chose register')
            username = input("Please enter username: \n")
            password = input("Please enter password: \n")
            data = chatlib.join_data([username, password])
            build_and_send_message(conn, chatlib.PROTOCOL_CLIENT['register_msg'], data)
            cmd, msg = recv_message_and_parse(conn)
            if cmd == chatlib.PROTOCOL_SERVER["register_ok_msg"]:
                print("register successful!")
                success = True
                return
            elif cmd == chatlib.PROTOCOL_SERVER["login_failed_msg"]:
                print("Login failed:", msg)
                print("Please try again...\n")
            else:
                print("Unexpected response from server:", cmd, msg)
        else:
            print("Invalid choice. Please type L or R.")




def logout(conn):
    # Implement code
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], '')
    print("Logged out.")

def build_send_recv_parse(conn,code,data):
    build_and_send_message(conn,code,data)
    msg_code,data = recv_message_and_parse(conn)
    return msg_code,data
def get_score(conn):
    msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_score_msg"], "")
    if msg_code == chatlib.PROTOCOL_SERVER["score_msg"]:
        print("\nyour score:\n" + data + "\n")
    else:
        print("Error: unexpected server response:", msg_code, data)

def get_highscore(conn):
    msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_highscore_msg"], "")
    if msg_code == chatlib.PROTOCOL_SERVER["highscore_msg"]:
        print('High-Score table:\n', data)
    else:
        print("Error: unexpected server response:", msg_code, data)


def get_logged_users(conn):
    users_logged,data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT['logged_msg'], '')
    print(data)



def main():
    conn = connect(SERVER_IP,SERVER_PORT)
    login(conn)
    code = ''
    while code.upper() != 'LOGOUT':
        code = input("what do you want to do:\nQuit=q\nGet my score=s\nGet high score=h\n")
        if code.lower() == "s":
            get_score(conn)
        elif code.lower() == 'h':
            get_highscore(conn)
        elif code.lower() == 'q':
            logout(conn)
            break
        elif code.lower() == 'l':
            get_logged_users(conn)
        else:
            print("Invalid command, please try again.")

if __name__ == "__main__":
    main()




