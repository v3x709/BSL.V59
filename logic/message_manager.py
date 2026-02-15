from protocol.laser.s.messages import LoginOkMessage, OwnHomeDataMessage

class MessageManager:
    def __init__(self, messaging):
        self.messaging = messaging

    def receive_message(self, message):
        t = message.get_message_type()
        if t == 10101:
            return self.handle_login(message)
        return 1

    def handle_login(self, login_msg):
        login_msg.decode()
        if login_msg.client_major_version != 59:
            return -1488

        db = self.messaging.db_manager
        id_low = login_msg.account_id_low
        if id_low == 0:
            id_low = db.get_max_id_low() + 1
            import secrets
            token = secrets.token_hex(16)
            db.create_player(0, id_low, token)

        player_data = db.get_player(0, id_low)
        if not player_data:
            db.create_player(0, id_low, "token")
            player_data = db.get_player(0, id_low)

        self.messaging.player_data = player_data
        self.messaging.send(LoginOkMessage())
        self.messaging.send(OwnHomeDataMessage(player_data))
        return 1
