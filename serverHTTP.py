import socket
from abc import ABC, abstractmethod
from typing import Union, Optional, Dict

class HttpMetodo: # Classe que representa o tipo Método de HTTP
  GET = 'GET'
  POST = 'POST'
  PUT = 'PUT'
  DELETE = 'DELETE'
  PATCH = 'PATCH'
  HEAD = 'HEAD'
  OPTIONS = 'OPTIONS'

class RequisicaoHTTP: # Classe que representa o tipo Requisição HTTP
    def __init__(self, method: str | None, path: str | None, headers: Optional[Dict[str, str]] = None, body: Optional[str] = None):
      if method not in HttpMetodo.__dict__.values():
          raise ValueError("Método de requisição inválido.")
      else: 
        self.method = getattr(HttpMetodo, method.upper())
        self.path = path
        self.headers = headers
        self.body = body

def parse_http_request(mensagem): # Função utilizada para tratar a mensagem enviada pelo cliente
    lines = mensagem.split("\n")
    method, path, _ = lines[0].split()
    headers = {}
    body = ""
    for line in lines[1:]:
        if line.strip():
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
        else:
            break
    if len(lines) > len(headers) + 1:
        body = "\n".join(lines[len(headers) + 1:])
    return RequisicaoHTTP(method, path, headers, body)

def Func_to_request(socketConnection ,request: RequisicaoHTTP) -> None:
    #Nesta função você pode implementar a função do seu servidor: Fornecer uma página web ou enviar uma mensagem
    print("Método:", request.method)
    print("Caminho:", request.path)
    print("Cabeçalhos:", request.headers)
    print("Corpo:", request.body)

    if request.method == HttpMetodo.GET:
        if request.path == '/':
            request.path = "index.html"
        arq = open(f"{request.path}","r")
        content = arq.read()
        arq.close()
    response = f"HTTP/1.1 200 OK\n\n{content}\n\n"
    socketConnection.send(response.encode('utf-8'))


#----------------Server Monad--------------------------------------------
class Monad(ABC): # Estrutura base de uma monada
    @abstractmethod
    def bind(self, func):
        pass

    @abstractmethod
    def return_(self, value):
        pass

class ServerMonad(Monad):  # Servidor
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None

    def bind(self, func):
        if self.server_socket is None:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            print("O servidor está ouvindo...")
        return func(self.server_socket)

    def return_(self, value):
        return value

#-----------------------------------------------------------------------------

def msg_of_client(client_socket): # Função para receber uma mensagem do cliente
    request = client_socket.recv(1024).decode()
    request = parse_http_request(request)
    Func_to_request(client_socket,request)
    

def main():
    server = ServerMonad('', 8080)
    server.bind(lambda socket: msg_of_client(socket.accept()[0]))

if __name__ == "__main__":
    main()
