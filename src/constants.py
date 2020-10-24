# -*- coding: utf-8 -*-
"""
Created on Mond Oct 12 2020

@author: Yhoan Alejandro Guzman, Juan Sebastian Perez
"""

SERVER_ADDRESS = "127.0.0.1"
PORT = 4567
BACKLOG = 5
RECV_BUFFER_SIZE = 1024 #100
ENCODING_FORMAT = "utf-8"
INIT = "init"
HELP = "help"
CODE_R = "code_r"
QUIT = "quit"
DATA = "data"
DELETE_B ="delete_b"
CREATE_B ="create_b"
LIST_B = "ls_b"
UPLOAD = "upload"
DELETE_F ="delete_f"
LIST_F = "ls_f"
DOWNLOAD = "download"
DEF_ROUTE = "def_route"
UPLOADING = "uploading"
HELP_STR = ("-> help : Use it to get information about commands.\n"
            "-> code_r : Use it to get information about response code meaning.\n"
            "-> quit : Use it to close client connection.\n"
            "-> delete_b : Use it to delete a bucket with the defined name.\n"
            "--> sintax: delete_b <name of the bucket> \n"
            "-> create_b : Use it to create a bucket with the defined name.\n"
            "--> sintax: create_b <name of the bucket> \n"
            "-> ls_b : Use it to list the existing buckets.\n"
            "-> upload_f : Use it to upload a file to the defined bucket.\n"
            "--> sintax: upload <path of the file> <name of file> <name of bucket>\n"
            "-> delete_f : Use it to delete a file from the defined bucket.\n"
            "--> sintax: delete_f <name of bucket> <name of file>\n"
            "-> ls_f : Use it to list the files in each bucket.\n"
            "-> download : Use it to download a file from the defined bucket.\n"
            "--> sintax: download <name of bucket> <name of file> <path of destination>\n")
CODE_R_STR = ("-> 300 BCS : Stands for Bucket Created Successfully.\n"
              "-> 350 BCF : Stands for Bucket Creation Fails.\n"
              "-> 400 BCMD : Stands for Bad Command.\n"
              "-> 500 BLS : Stands for Bucket Listed Successfully.\n"
              "-> 600 BDS : Stands for Bucket Deleted Successfully.\n"
              "-> 650 BDF : Stands for Bucket Deletion Fails.\n"
              "-> 700 FUTBS : Stands for File Uploaded To Bucket Successfully.\n"
              "-> 800 FLS : Stands for Files Listed Successfully.\n"
              "-> 900 FDFBS : Stands for File Downloaded From Bucket Successfully.\n"
              "-> 1000 FDS : Stands for File Deleted Successfully.\n"
              "-> 1050 FDF : Stands for File Deletion Fails.\n")
ERROR_DATA = "There is an error in the given data."