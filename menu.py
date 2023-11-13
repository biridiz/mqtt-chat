import time
import os

def menu(client):
  EXIT = False

  while not EXIT:
    print("1 - Listar usuários")
    print("2 - Criar grupo")
    print("3 - Listar grupos")
    print("4 - Iniciar bate papo")
    print("5 - Minhas conversas")
    print("6 - Sair")

    opt = int(input())
    
    if opt == 1:
      os.system("clear")
      client.users()

      select = input()

      if select == "sair":
        os.system("clear")
        menu(client)

    elif opt == 2:
      name = input('Insira o nome do grupo: ')
      members = input("Insira o id dos integrantes: ")
      client.new_group(name, members)

      os.system("clear")
      menu(client)

    elif opt == 3:
      os.system("clear")
      client.groups()

      select = input()

      if select == "sair":
        os.system("clear")
        menu(client)

      client.select_group(int(select)-1)
      EXIT_CONVERSATION = False

      print("Digite algo")
      while not EXIT_CONVERSATION:
        message = input()
        if message == "sair":
          os.system("clear")
          EXIT_CONVERSATION = True
        else:
          client.send_message(message)

    elif opt == 4:
      os.system("clear")
      id = input('Insira o id com quem deseja conversar: ')

      client.request_chat(id)
      EXIT_CONVERSATION = False

      print("Digite algo")
      while not EXIT_CONVERSATION:
        message = input()
        if message == "sair":
          EXIT_CONVERSATION = True
          os.system("clear")
        else:
          client.send_message(message)

    elif opt == 5:
      os.system("clear")
      client.chats()

      select = input()

      if select == "sair":
        os.system("clear")
        menu(client)

      client.select_chat(int(select)-1)
      EXIT_CONVERSATION = False

      print("Digite algo")
      while not EXIT_CONVERSATION:
        message = input()
        if message == "sair":
          os.system("clear")
          EXIT_CONVERSATION = True
        else:
          client.send_message(message)

    elif opt == 6:
      client.disconnect()
      EXIT = True
      time.sleep(3)

    else:
      print("Opção inválida!")