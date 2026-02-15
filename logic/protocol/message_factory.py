from logic.protocol.laser.s.server_hello_message import ServerHelloMessage
from logic.protocol.laser.s.login_ok_message import LoginOkMessage
from logic.protocol.laser.s.own_home_data_message import OwnHomeDataMessage

class MessageFactory:
    def __init__(self):
        self.messages = {
            20100: ServerHelloMessage,
            20104: LoginOkMessage,
            24101: OwnHomeDataMessage
        }

    def create_message_by_type(self, msg_type):
        if msg_type in self.messages:
            return self.messages[msg_type]()
        return None
