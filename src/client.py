# -*- coding: utf-8 -*-
"""
Created on Mond Oct 12 2020

@author: Yhoan Alejandro Guzman, Juan Sebastian Perez
"""

import socket
import constants
import ast
import json 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bucket_route = ""

def main():
    print("*"*40)
    print("Client is running...")
    client_socket.connect(("127.0.0.1", constants.PORT))
    local_tuple = client_socket.getsockname()
    print("Connected to the server from:", local_tuple)
    print('Enter \"quit\" to exit')
    print('Input commands: ')
    command_to_send = input()

    while  command_to_send != constants.QUIT:
        if command_to_send == '':
            print("Please input a valid command...")
            command_to_send = input()
        elif(command_to_send== constants.CREATE_B):
            data_to_send = input("Name of the bucket: ")
            command_and_data_to_send = command_to_send + ' ' + data_to_send 
            client_socket.send(bytes(command_and_data_to_send, constants.ENCODING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            print(data_received.decode(constants.ENCODING_FORMAT))
            command_to_send = input()
        elif(command_to_send== constants.LIST_B):
            command_and_data_to_send = command_to_send
            client_socket.send(bytes(command_and_data_to_send, constants.ENCODING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            bucket_list = ast.literal_eval(data_received.decode(constants.ENCODING_FORMAT))
            print(bucket_list[:-1])
            print(bucket_list[-1])
            command_to_send = input()
        elif(command_to_send== constants.DELETE_B):
            data_to_send = input("Name of the bucket that you would like to delete: ")
            command_and_data_to_send = command_to_send + ' ' + data_to_send 
            client_socket.send(bytes(command_and_data_to_send, constants.ENCODING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            print(data_received.decode(constants.ENCODING_FORMAT))
            command_to_send = input()
        elif(command_to_send==constants.UPLOAD):
            origin_directory = input("Path of the directory of the file: ")
            bucket = input("Name of the destination bucket: ")
            command_and_data_to_send = command_to_send + ' ' + origin_directory + ' ' + bucket
            client_socket.send(bytes(command_and_data_to_send, constants.ENCODING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            print(data_received.decode(constants.ENCODING_FORMAT))
            command_to_send = input()
        elif(command_to_send==constants.LIST_F):
            command_and_data_to_send = command_to_send
            client_socket.send(bytes(command_and_data_to_send, constants.ENCODING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            data_received = str(data_received.decode(constants.ENCODING_FORMAT)).replace("'", '"').replace("\\\\", '/')
            file_list = json.loads(str(data_received))
            for key in file_list:
                if (key != "response"):
                    print(key)
                    print("----> "+str(file_list[key]))
            print(file_list["response"])
            command_to_send = input()
        elif (command_to_send == constants.DOWNLOAD):
            origin_bucket = input("Name of the origin bucket: ")
            file_name = input("Name of the file: ")
            destination = input("Path of the destination: ")
            command_and_data_to_send = command_to_send + ' ' + origin_bucket + ' ' + file_name +' '+ destination
            client_socket.send(bytes(command_and_data_to_send, constants.ENCODING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            print(data_received.decode(constants.ENCODING_FORMAT))
            command_to_send = input()
        elif (command_to_send == constants.DELETE_F):
            bucket = input("Name of the bucket where you would like to delete a file: ")
            file_name = input("Name of the file: ")
            command_and_data_to_send = command_to_send + ' ' + bucket + ' ' + file_name
            client_socket.send(bytes(command_and_data_to_send, constants.ENCODING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            print(data_received.decode(constants.ENCODING_FORMAT))
            command_to_send = input()
        else:
            client_socket.send(bytes(command_to_send, constants.ENCODING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            print(data_received.decode(constants.ENCODING_FORMAT))
            command_to_send = input()
    
    client_socket.send(bytes(command_to_send, constants.ENCODING_FORMAT))
    data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
    print(data_received.decode(constants.ENCODING_FORMAT))
    client_socket.close()

if __name__ == '__main__':
    main()