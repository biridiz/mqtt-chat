from menu import menu 
from client import Client

id = int(input('ID: '))

client = Client(id)
client.connect()

menu(client)