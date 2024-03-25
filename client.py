import socket

SERVER_HOST = "127.0.0.1"  # Endereço IP do servidor
SERVER_PORT = 8080      # Porta do servidor

# Cria o socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Tenta se conectar ao servidor
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("Conexão estabelecida com sucesso!")

    # Requisição simples para o servidor
    message = "GET index.html HTTP/1.1"
    client_socket.sendall(message.encode())

    # Recebe a resposta do servidor
    response = client_socket.recv(2048)
    print("Resposta do servidor:", response.decode())

except Exception as e:
    print("Erro ao se conectar ao servidor:", e)

finally:
    # Fecha o socket do cliente
    client_socket.close()