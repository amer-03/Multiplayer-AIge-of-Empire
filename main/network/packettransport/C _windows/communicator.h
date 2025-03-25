#ifndef COMMUNICATOR_H
#define COMMUNICATOR_H

#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#pragma comment(lib, "ws2_32.lib")

#define TRUE 1
#define FALSE 0
#define BUFFER_SIZE 15000
#define ID_SIZE 10
#define SEPARATOR '~'

#define RCVBUF_SIZE 10485760
#define SNDBUF_SIZE 10485760

#define SLEEP_TIME_MS 1000

#define PYTHON_PORT 60000
#define C_PORT1 40001
#define C_PORT2 50002
#define EXTERNAL_PORT 50002

#define LOCALHOST_IP "127.0.0.1"
#define BROADCAST_IP "172.20.10.15"

typedef struct {
    SOCKET sockfd;
    struct sockaddr_in destination_addr;
    struct sockaddr_in listener_addr;
    char recv_buffer[BUFFER_SIZE];
    char instance_id[ID_SIZE];
} Communicator;

void generate_instance_id(Communicator* comm);
Communicator* init_communicator(int listener_port, int destination_port, const char* destination_addr);
void construct_packet(Communicator* comm, const char* query, char* packet, size_t packet_size);
int send_packet(Communicator* comm, const char* message);
char* process_packet(char* packet, char* packet_id, size_t id_size);
char* receive_packet(Communicator* comm);
void cleanup_communicator(Communicator* comm);

#endif
