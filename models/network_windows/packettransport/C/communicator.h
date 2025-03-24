#ifndef COMMUNICATOR_H
#define COMMUNICATOR_H

#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#include <stdio.h>

#pragma comment(lib, "ws2_32.lib")

#define BUFFER_SIZE 1024
#define ID_SIZE 16
#define SEPARATOR '|'

// À adapter selon ton contexte
#define C_PORT1 4000
#define C_PORT2 4001
#define PYTHON_PORT 5000
#define EXTERNAL_PORT 6000
#define LOCALHOST_IP "127.0.0.1"
#define BROADCAST_IP "255.255.255.255"
#define SLEEP_TIME_MS 100

typedef struct {
    SOCKET sockfd;
    struct sockaddr_in listener_addr;
    struct sockaddr_in destination_addr;
    char recv_buffer[BUFFER_SIZE];
    char instance_id[ID_SIZE];
} Communicator;

Communicator* init_communicator(int listener_port, int destination_port, const char* destination_addr);
void cleanup_communicator(Communicator* comm);
int send_packet(Communicator* comm, const char* query);
char* receive_packet(Communicator* comm);
void construct_packet(Communicator* comm, const char* query, char* packet, size_t packet_size);

#endif
