# Sockets in python

## Description 📄

_This projects use sockets in python to stablish a communication between a server socket and a client socket._\n
Sockets and the socket API are used to send messages across a network. They provide a form of inter-process communication (IPC). The network can be a logical, local network to the computer, or one that’s physically connected to an external network, with its own connections to other networks.\n

## Messages vocabulary 📖

### Commands description ℹ️

**help:** Use it to _get information about commands._\n
**code_r: ** Use it to _get information about response code meaning._
**quit: ** Use it to _close client connection._
**delete_b: ** Use it to _delete a bucket with the defined name._
**sintax: ** 
```delete_b <name of the bucket>```
**create_b: ** Use it to _create a bucket with the defined name._
**sintax: ** 
```create_b <name of the bucket>```
**ls_b: ** Use it to _list the existing buckets._
**upload_f: ** Use it to _upload a file to the defined bucket._
**sintax: ** 
```upload <path of the file> <name of file> <name of bucket>```
**delete_f: ** Use it to _delete a file from the defined bucket._
**sintax: ** 
```delete_f <name of bucket> <name of file>```
**ls_f: ** Use it to _list the files in each bucket._
**download: ** Use it to _download a file from the defined bucket._
**sintax: ** 
```download <name of bucket> <name of file> <path of destination>```

### Code response meaning 📓

**300 BCS** Stands for _Bucket Created Successfully._
**350 BCF**  Stands for _Bucket Creation Fails._
**400 BCMD** Stands for _Bad Command._
**500 BLS**  Stands for _Bucket Listed Successfully._
**600 BDS**  Stands for _Bucket Deleted Successfully._
**650 BDF**  Stands for _Bucket Deletion Fails._
**700 FUTB** Stands for _File Uploaded To Bucket Successfully._
**800 FLS**  Stands for _Files Listed Successfully._
**900 FDFBS**  Stands for _File Downloaded From Bucket Successfully._
**1000 FDS**  Stands for _File Deleted Successfully._
**1050 FDF**  Stands for _File Deletion Fails._

