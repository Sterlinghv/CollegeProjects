#!/bin/bash
gcc -o enc_server enc_server.c -lpthread -Wall
gcc -o enc_client enc_client.c -Wall
gcc -o dec_server dec_server.c -lpthread -Wall
gcc -o dec_client dec_client.c -Wall
gcc -o keygen keygen.c
