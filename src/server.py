# -*- coding: utf-8 -*-
"""
Created on Mond Oct 12 2020

@author: Yhoan Alejandro Guzman, Juan Sebastian Perez
"""

#Import libraries for networking communication
import _thread
import socket
import constants
import os
import sys
import shutil

# import thread module 
import threading 

print_lock = threading.Lock() 
bucket_route = ""

#Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def threaded(client_connection, client_address, route):
    while True:
        data_received = client_connection.recv(constants.RECV_BUFFER_SIZE)
        remote_string = str(data_received.decode(constants.ENCODING_FORMAT))
        remote_command = remote_string.split()
        command = remote_command[0]
        print(f'Data received from: {client_address[0]}:{client_address[1]}')
        print(command)
        if(command == constants.INIT):
            response = '100 OK\n'
            client_connection.sendall(response.encode(constants.ENCODING_FORMAT))
        elif(command == constants.QUIT):
            response = '200 BYE\n'
            client_connection.sendall(response.encode(constants.ENCODING_FORMAT))
            print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected.')
            break
        elif(command == constants.HELP):
            response = constants.HELP_STR
            client_connection.sendall(response.encode(constants.ENCODING_FORMAT))
        elif(command == constants.CODE_R):
            response = constants.CODE_R_STR
            client_connection.sendall(response.encode(constants.ENCODING_FORMAT))
        elif(command == constants.CREATE_B):
            try:
                name = remote_command[1]
                name = "\\" + name
                #print(route+name)
                os.mkdir(route+name)
                response = '300 BCS\n'
            except BaseException as e:
                print("ERROR: " + str(e))
                response = '350 BCF\n'
            client_connection.sendall(response.encode(constants.ENCODING_FORMAT))
        elif(command == constants.LIST_B):
            bucket_list = os.listdir(route)
            bucket_list.append("500 BLS")
            response = str(bucket_list)
            client_connection.sendall(response.encode(constants.ENCODING_FORMAT))
        elif(command == constants.DELETE_B):
            try:
                name = remote_command[1]
                name = "\\" + name
                shutil.rmtree(route+name)
                response = '600 BDS\n'
                client_connection.sendall(response.encode(constants.ENCODING_FORMAT))
            except BaseException as e:
                print("ERROR: " + str(e))
                response = '650 BDF\n'
                client_connection.sendall(response.encode(constants.ENCODING_FORMAT))
        elif(command == constants.UPLOAD):
            origin_directory = remote_command[1]
            destination = remote_command[2]
            destination = "\\" + destination
            shutil.copy2(origin_directory,route+destination)
            response = '700 FUTBS\n'
            client_connection.sendall(response.encode(constants.ENCODING_FORMAT))
        elif(command == constants.LIST_F):
            dic = {} 
            for dirName, subdirList, fileList in os.walk(route):
                array = []
                for fname in fileList:
                    array.append(fname)
                dic[dirName] = array
            dic['response'] = '800 FLS\n'
            response = str(dic)
            client_connection.sendall(response.encode(constants.ENCODING_FORMAT))
        elif (command == constants.DOWNLOAD):
            origin_bucket = remote_command[1]
            file_name = remote_command[2]
            destination = remote_command[3]
            origin_bucket = "\\" + origin_bucket + "\\" + file_name
            shutil.copy2(route + origin_bucket,destination)
            response = '900 FDFBS\n'
            client_connection.sendall(response.encode(constants.ENCODING_FORMAT))
        elif (command == constants.DELETE_F):
            try:
                bucket = remote_command[1]
                file_name = remote_command[2]
                name = "\\" + bucket + "\\" + file_name
                os.remove(route + name)
                response = '1000 FDS\n'
                client_connection.sendall(response.encode(constants.ENCODING_FORMAT))
            except BaseException as e:
                print("ERROR: " + str(e))
                response = '1050 FDF\n'
                client_connection.sendall(response.encode(constants.ENCODING_FORMAT))
        else:
            response = '400 BCMD\n'
            client_connection.sendall(response.encode(constants.ENCODING_FORMAT))
    try:
        print_lock.release()
    except BaseException:
        pass
    client_connection.close()

#Main function
def main():
    try:
        if len(sys.argv) < 2:
            raise Exception("You have to input a path for buckets creation")
        if not os.path.exists(sys.argv[1]):
            raise Exception("Invalid path")
        bucket_route = sys.argv[1]
    except BaseException as e:
        print("ERROR: " + str(e))
        sys.exit(1)
    print('*'*40)
    print('Server is running...')
    print('IP address: ', constants.SERVER_ADDRESS)
    print('Port: ', constants.PORT)
    tuple_connection = (constants.SERVER_ADDRESS, constants.PORT)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(tuple_connection)
    server_socket.listen(constants.BACKLOG)
    print('Socket is listening...', server_socket.getsockname())
    
    #Loop for waiting new conection
    while True:
        client_connection, client_address = server_socket.accept()
         
        print(f'New incoming connection is accepted. Remote IP address: {client_address[0]}')  
        # Start a new thread and return its identifier 
        _thread.start_new_thread(threaded, (client_connection,client_address, bucket_route)) 
    server_socket.close()

if __name__ == '__main__':
    main()
