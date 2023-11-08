import socket
import struct

def calculate_checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        w = (data[i] << 8) + (data[i + 1] if i + 1 < len(data) else 0)
        checksum += w
    while checksum >> 16:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    return (~checksum) & 0xFFFF

def main():
    server_address = ('localhost', 12345)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = input("Digite a mensagem a ser enviada: ")

    while True:
        packet = struct.pack('>H', calculate_checksum(message.encode())) + message.encode()

        client_socket.sendto(packet, server_address)
        response, _ = client_socket.recvfrom(1024)

        if response == b'Ack':
            print("Mensagem recebida corretamente pelo servidor.")
            break
        elif response == b'Nack':
            print("Mensagem corrompida - Reenviando pacote...")
        else:
            print("Mensagem reenviada.")

    client_socket.close()

if __name__ == "__main__":
    main()
