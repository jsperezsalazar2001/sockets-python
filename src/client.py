# -*- coding: utf-8 -*-
"""
Created on Mond Oct 12 2020

@author: Yhoan Alejandro Guzman, Juan Sebastian Perez
"""

import _thread
import socket
import constants
import ast
import json 
import time
import os
import threading 
import sys
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bucket_route = ""
def upload(origin_directory, command_and_data_to_send):
    new_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_client_socket.connect(("127.0.0.1", constants.PORT))           
    new_client_socket.send(bytes(command_and_data_to_send, constants.ENCODING_FORMAT))
    new_local_tuple = new_client_socket.getsockname()
    print("Connected upload to the server from:", new_local_tuple)
    print("entra upload hilo")
    time.sleep(1)
    origin_directory = origin_directory.replace("\\", '/')
    f = open(origin_directory,'rb')
    l = f.read(1024)
    while (l):
        new_client_socket.send(l)
        l = f.read(1024)
    f.close()
    print("finished sending")
    data_received = new_client_socket.recv(constants.RECV_BUFFER_SIZE)
    print(data_received.decode(constants.ENCODING_FORMAT))
    new_client_socket.close()
    sys.exit()

def download(command_and_data_to_send, destination, file_name):
    new_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_client_socket.connect(("127.0.0.1", constants.PORT)) 
    new_client_socket.send(bytes(command_and_data_to_send, constants.ENCODING_FORMAT))
    data_received = new_client_socket.recv(constants.RECV_BUFFER_SIZE)
    file_size = data_received.decode(constants.ENCODING_FORMAT)

    try:
        f = open(destination+'\\'+file_name,'wb')
        if file_size is not "0":
            print("Receiving file...")                
            l = new_client_socket.recv(1024)
            total = len(l)
            while(len(l)>0):
                f.write(l)
                if (str(total) != file_size):
                    l = new_client_socket.recv(1024)
                    total = total + len(l)
                else:
                    break
        f.close()
    except BaseException as e:
        print("ERROR: " + str(e))  
    print("File received") 
    data_received = new_client_socket.recv(constants.RECV_BUFFER_SIZE)
    print(data_received.decode(constants.ENCODING_FORMAT))
    new_client_socket.close()
    sys.exit()

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
        elif(command_to_send == constants.HELP):
            client_socket.send(bytes(command_to_send, constants.ENCODING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            print(data_received.decode(constants.ENCODING_FORMAT))
            command_to_send = input()
        elif(command_to_send == constants.CODE_R):
            client_socket.send(bytes(command_to_send, constants.ENCODING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            print(data_received.decode(constants.ENCODING_FORMAT))
            command_to_send = input()
        elif(command_to_send == constants.CREATE_B):
            data_to_send = input("Name of the bucket: ")
            command_and_data_to_send = command_to_send + ' ' + data_to_send 
            client_socket.send(bytes(command_and_data_to_send, constants.ENCODING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            print(data_received.decode(constants.ENCODING_FORMAT))
            command_to_send = input()
        elif(command_to_send == constants.LIST_B):
            command_and_data_to_send = command_to_send
            client_socket.send(bytes(command_and_data_to_send, constants.ENCODING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            bucket_list = ast.literal_eval(data_received.decode(constants.ENCODING_FORMAT))
            print(bucket_list[:-1])
            print(bucket_list[-1])
            command_to_send = input()
        elif(command_to_send == constants.DELETE_B):
            data_to_send = input("Name of the bucket that you would like to delete: ")
            command_and_data_to_send = command_to_send + ' ' + data_to_send 
            client_socket.send(bytes(command_and_data_to_send, constants.ENCODING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            print(data_received.decode(constants.ENCODING_FORMAT))
            command_to_send = input()
        elif(command_to_send==constants.UPLOAD):
            print("entra upload")
            try:
                origin_directory = input("Path of the directory of the file: ")
                if origin_directory[-1] == '"' and origin_directory[0] == '"':
                    origin_directory = origin_directory[1:-1]
                bucket = input("Name of the destination bucket: ")
                file_name = input("What would you like the file to be saved as? (with extension): ")
                file_size = str(os.path.getsize(origin_directory))
                command_and_data_to_send = command_to_send + ' ' + bucket + ' ' + file_name + ' ' + file_size
                _thread.start_new_thread(upload, (origin_directory, command_and_data_to_send))
                command_to_send = input()
            except BaseException as e:
                print("ERROR: " + str(e)) 
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
            command_and_data_to_send = command_to_send + ' ' + origin_bucket + ' ' + file_name
            _thread.start_new_thread(download, (command_and_data_to_send, destination, file_name))
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