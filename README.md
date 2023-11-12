Arquitetura do sistema:


Definição e formato dos tópicos de controle:
Os tópicos de controle são usados para trocar informações de controle entre os clientes e o servidor, como o status dos usuários, as solicitações e respostas de sessões, as informações dos grupos, etc. Os tópicos de controle são definidos da seguinte forma:

- USERS: é um tópico de controle global, onde são publicados o status (online ou offline) de cada usuário. Cada cliente deve assinar esse tópico para receber as atualizações de status dos demais usuários. Cada cliente deve publicar seu próprio status nesse tópico quando iniciar ou encerrar o aplicativo. O formato da mensagem publicada nesse tópico é:

{
  "id": "ID do usuário",
  "status": "online ou offline"
}

- GROUPS: é um tópico de controle global, onde são publicadas informações de cada grupo: nome do grupo, nome do usuário que é líder do grupo e lista dos demais membros. Cada cliente deve assinar esse tópico para receber as atualizações dos grupos existentes. O líder de cada grupo deve publicar as informações do seu grupo nesse tópico quando criar, alterar ou excluir o grupo. O formato da mensagem publicada nesse tópico é:

{
  "name": "Nome do grupo",
  "leader": "Nome do líder do grupo",
  "members": ["Nome do membro 1", "Nome do membro 2", ...]
}

- <ID>_Control: é um tópico de controle individual, onde são trocadas informações de controle entre o cliente e o servidor, como a solicitação e a resposta de uma nova sessão, a confirmação de recebimento de uma mensagem, etc. Cada cliente deve assinar e publicar no seu próprio tópico de controle, usando o seu ID como parte do nome do tópico. Por exemplo, para um usuário com ID = X, o tópico será X_Control. Os demais usuários só podem publicar nesse tópico, mas não assiná-lo. O formato da mensagem publicada nesse tópico depende do tipo de informação de controle, mas deve conter um campo "type" para identificar o tipo. Por exemplo, para solicitar uma nova sessão, o formato da mensagem é:

{
  "type": "request",
  "from": "ID do usuário solicitante",
  "to": "ID do usuário solicitado"
}

Para responder a uma solicitação de sessão, o formato da mensagem é:

{
  "type": "response",
  "from": "ID do usuário solicitado",
  "to": "ID do usuário solicitante",
  "session": "ID da sessão criada",
  "topic": "Nome do tópico da sessão"
}

Para confirmar o recebimento de uma mensagem, o formato da mensagem é:

{
  "type": "ack",
  "from": "ID do usuário que recebeu a mensagem",
  "to": "ID do usuário que enviou a mensagem",
  "session": "ID da sessão da mensagem",
  "message": "ID da mensagem recebida"
}

<ID1>_<ID2>_TIMESTAMP: Este é o tópico dedicado para o bate-papo um a um entre dois usuários. O formato do tópico é criado concatenando os IDs dos dois usuários envolvidos na conversa, juntamente com um timestamp para garantir a unicidade da sessão.

{
  "from": "ID do usuário remetente",
  "to": "ID do usuário destinatário",
  "message": "Conteúdo da mensagem",
  "timestamp": "Timestamp da mensagem",
  "type": "text"  // Pode ser "text", "image", "file", etc., dependendo do tipo de mensagem
}

<ID>_GROUP_CHAT: Este é um tópico dedicado para uma conversa em grupo. Quando um grupo é criado, um tópico específico é estabelecido para a comunicação dentro desse grupo. Cada cliente que é membro do grupo deve assinar este tópico para receber mensagens do grupo. O formato da mensagem publicada neste tópico pode ser:

{
  "from": "ID do usuário remetente",
  "to": "ID do grupo ou tópico",
  "message": "Conteúdo da mensagem",
  "timestamp": "Timestamp da mensagem"
}