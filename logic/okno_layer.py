from protocol.laser.c.messages import ClientHelloMessage, LoginMessage

class LogicLaserMessageFactory:
    @staticmethod
    def create_message_by_type(msg_type, payload=None):
        if msg_type == 10100: return ClientHelloMessage(payload)
        if msg_type == 10101: return LoginMessage(payload)
        return None

class MessageManager:
    def __init__(self, messaging):
        self.messaging = messaging

    def receive_message(self, message):
        msg_type = message.get_message_type()
        if msg_type == 10101:
            return self.handle_login(message)
        return 1

    def handle_login(self, login_msg):
        login_msg.decode()
        # logic for login...
        return 1
