import paho.mqtt.client as mqtt
from threading import Thread

BROKER = "127.0.0.1"
PORT = 1883

class Client:
    def __init__(self, id):
        self.id = id
        self.client = mqtt.Client()    
        self.client.connect(BROKER, PORT)
        self.client.on_message = self.on_message

        t = Thread(target=self.client.loop_start, args=())
        t.start()

        self.users_list = []
        self.groups_list = []
        self.chats_list = []
        self.old_received_messages = {}
        self.current_chat = None

    def connect(self):
        self.client.subscribe(f"{self.id}_Control")
        self.client.subscribe("USERS")
        self.client.subscribe("GROUPS")
        self.client.publish("USERS", payload=f'id:{self.id};status:online', qos=2, retain=True)

    def disconnect(self):
        self.client.publish("USERS", payload=f'id:{self.id};status:offline', qos=2, retain=True)

    def users(self):
        print(self.users_list)

    def groups(self):
        # TODO: deve listar somente grupos em que usuário particpa
        print(self.groups_list)

    # TODO: função para assinar tópico da conversa e definir grupo como 'current_chat

    def chats(self):
        for i in range(len(self.chats_list)):
            print(f'{i+1} - {self.chats_list[i]}')

    def new_group(self, name, members):
        # TODO: criar tópico do grupo
        self.client.publish("GROUPS", payload=f'leader:{self.id};name:{name};members:{members}', qos=2, retain=True)

    def request_chat(self, id):
        self.client.publish(f"{id}_Control", payload=f'type:request;from:{self.id};to:{id}', qos=2, retain=True)

    def on_message(self, client, userdata, msg):
        if msg.topic == "USERS":
            # TODO: se user já existir apenas atualizar status
            self.users_list.append(self.get_params(msg.payload.decode()))

        elif msg.topic == "GROUPS":
            # TODO: se grupo já existir não adcionar
            self.groups_list.append(msg.payload.decode())

        elif msg.topic == f"{self.id}_Control":
            self.start_conversation(msg.payload.decode())

        elif msg.topic == self.current_chat:
            self.print_message(msg.payload.decode())
        
        elif msg.topic != self.current_chat:
            if self.old_received_messages.get(msg.topic) is not None:
                messages = self.old_received_messages[msg.topic].append(msg.payload.decode())
            else:
                messages = [msg.payload.decode()]
            self.old_received_messages[msg.topic] = messages

    def get_params(self, data):
        return data.split(';')

    def get_dic_params(self, data):
        dic = {}
        for p in data:
            split = p.split(':')
            dic[f"{split[0]}"] = split[1]
        return dic

    def start_conversation(self, message):
        params = self.get_params(message)
        dic_params = self.get_dic_params(params)

        if dic_params["type"] == "request":
            self.client.subscribe(f'{self.id}_{dic_params["from"]}_timestamp')
            self.chats_list.append(f'{self.id}_{dic_params["from"]}_timestamp')
            self.client.publish(
                f'{dic_params["from"]}_Control',
                payload=f'type:response;from:{self.id};to:{dic_params["from"]};topic:{self.id}_{dic_params["from"]}_timestamp',
                qos=2,
                retain=True
            )

        if dic_params["type"] == "response":
            self.client.subscribe(dic_params["topic"])
            self.chats_list.append(dic_params["topic"])
            self.current_chat = dic_params["topic"]

    def send_message(self, message):
        self.client.publish(self.current_chat, payload=f'id:{self.id};message:{message}')

    def select_chat(self, key):
        self.current_chat = self.chats_list[key]
        if self.old_received_messages.get(self.current_chat) is not None:
            # TODO: Tratar impressão de mensagens antigas
            print(self.old_received_messages[self.current_chat])

    def print_message(self, message):
        params = self.get_params(message)
        dic_params = self.get_dic_params(params)
        if int(dic_params["id"]) != self.id:
            print(f'User {dic_params["id"]}: {dic_params["message"]}')