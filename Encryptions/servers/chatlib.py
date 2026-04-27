# Protocol Constants

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "get_score_msg": "MY_SCORE",
    "get_highscore_msg": "HIGHSCORE",
    'logged_msg': 'LOGGED',
    'get_question_msg': 'GET_QUESTION',
    'send_answer_msg': 'SEND_ANSWER',
    'register_msg': 'REGISTER'
}  # .. Add more commands if needed

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR",
    "score_msg": "YOUR_SCORE",
    "highscore_msg": "ALL_SCORE",
    'logged_answer_msg': 'LOGGED_ANSWER',
    'question_msg': "YOUR_QUESTION",
    'correct_answer_msg': 'CORRECT_ANSWER',
    'wrong_answer_msg': 'WRONG_ANSWER',
    'all_score_msg': 'ALL_SCORE',
    "error_msg": 'ERROR',
    'no_questions_msg': 'NO_QUESTIONS',
    'register_ok_msg': 'REGISTER_OK',
    'register_failed_msg' : 'ERROR'
}  # ..  Add more commands if needed

# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    if len(cmd) < CMD_FIELD_LENGTH and len(data) <= MAX_DATA_LENGTH:
        length_data = str(str((LENGTH_FIELD_LENGTH - int(len(str(len(data))))) * '0')) + str(len(data))
        full_msg = cmd + (CMD_FIELD_LENGTH - len(cmd) )*' ' + DELIMITER+length_data+DELIMITER + data
        return full_msg
    else:
        return ERROR_RETURN
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occured
    """
    # Implement code ...






def parse_message(data):
    dict_data = str(data).split(DELIMITER)
    if len(dict_data) == 3:
        cmd = (dict_data[0]).replace(" ", "")
        msg = dict_data[2]
        if ((dict_data[1]).replace(' ','')).isdigit() and int(dict_data[1]) >= 0 and len(dict_data[1]) == 4 and len(msg) == int(dict_data[1]):
            return cmd, msg
        else:
            return ERROR_RETURN,ERROR_RETURN
    else:
        return ERROR_RETURN, ERROR_RETURN
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """
    # Implement code ...

    # The function should return 2 values





def split_data(msg, expected_fields):
    divider_count = msg.count(DATA_DELIMITER)
    if divider_count == expected_fields:
        return msg.split(DATA_DELIMITER)
    else:
        return ["none"]

"""
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
"""
# Implement code ...



def join_data(msg_fields):
    return DATA_DELIMITER.join(map(str, msg_fields))
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
# Implement code ...
users_dict = {}
with open(r'your_file.txt', 'r') as file:
    for line in file:
        print(line)
        key, value = line.strip().split(':')
        users_dict[key.strip()] = value.strip()

