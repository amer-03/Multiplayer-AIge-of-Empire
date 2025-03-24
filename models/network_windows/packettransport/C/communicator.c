#include "communicator.h"
#include <time.h>


void generate_instance_id(Communicator* comm) {
    srand((unsigned int)(time(NULL) ^ GetCurrentProcessId()));
    snprintf(comm->instance_id, ID_SIZE, "%08X", rand() % 0xFFFFFFFF);
}

Communicator* init_communicator(int listener_port, int destination_port, const char* destination_addr) {
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);

    Communicator* comm = (Communicator*)malloc(sizeof(Communicator));
    if (!comm) {
        fprintf(stderr, "Memory allocation failed\n");
        return NULL;
    }

    generate_instance_id(comm);

    comm->sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (comm->sockfd == INVALID_SOCKET) {
        fprintf(stderr, "Socket creation failed: %d\n", WSAGetLastError());
        free(comm);
        return NULL;
    }

    u_long mode = 1;
    ioctlsocket(comm->sockfd, FIONBIO, &mode);

    BOOL opt = TRUE;
    setsockopt(comm->sockfd, SOL_SOCKET, SO_REUSEADDR, (char*)&opt, sizeof(opt));
    setsockopt(comm->sockfd, SOL_SOCKET, SO_BROADCAST, (char*)&opt, sizeof(opt));

    int recv_buff = 65536;
    int send_buff = 65536;
    setsockopt(comm->sockfd, SOL_SOCKET, SO_RCVBUF, (char*)&recv_buff, sizeof(recv_buff));
    setsockopt(comm->sockfd, SOL_SOCKET, SO_SNDBUF, (char*)&send_buff, sizeof(send_buff));

    memset(&comm->listener_addr, 0, sizeof(comm->listener_addr));
    comm->listener_addr.sin_family = AF_INET;
    comm->listener_addr.sin_addr.s_addr = INADDR_ANY;
    comm->listener_addr.sin_port = htons(listener_port);

    memset(&comm->destination_addr, 0, sizeof(comm->destination_addr));
    comm->destination_addr.sin_family = AF_INET;
    comm->destination_addr.sin_port = htons(destination_port);
    comm->destination_addr.sin_addr.s_addr = inet_addr(destination_addr);

    if (bind(comm->sockfd, (struct sockaddr*)&comm->listener_addr, sizeof(comm->listener_addr)) == SOCKET_ERROR) {
        fprintf(stderr, "Bind failed: %d\n", WSAGetLastError());
        closesocket(comm->sockfd);
        free(comm);
        return NULL;
    }

    printf("[+] Communicator initialized (ID: %s, listening on %d, destination: %d)\n",
        comm->instance_id, listener_port, destination_port);
    return comm;
}

void cleanup_communicator(Communicator* comm) {
    if (comm) {
        closesocket(comm->sockfd);
        free(comm);
        WSACleanup();
        printf("[+] Communicator cleaned up\n");
    }
}

void construct_packet(Communicator* comm, const char* query, char* packet, size_t packet_size) {
    if (ntohs(comm->destination_addr.sin_port) != PYTHON_PORT) {
        snprintf(packet, packet_size, "%s%c%s", comm->instance_id, SEPARATOR, query);
    } else {
        strncpy(packet, query, packet_size - 1);
        packet[packet_size - 1] = '\0';
    }
}

int send_packet(Communicator* comm, const char* query) {
    char packet[BUFFER_SIZE];
    construct_packet(comm, query, packet, BUFFER_SIZE);
    int result = sendto(comm->sockfd, packet, (int)strlen(packet), 0,
                        (struct sockaddr*)&comm->destination_addr, sizeof(comm->destination_addr));
    if (result == SOCKET_ERROR) {
        int err = WSAGetLastError();
        if (err != WSAEWOULDBLOCK) {
            fprintf(stderr, "Send failed: %d\n", err);
        }
        return -1;
    }
    return result;
}

char* receive_packet(Communicator* comm) {
    struct sockaddr_in sender_addr;
    int addr_len = sizeof(sender_addr);

    int recv_len = recvfrom(comm->sockfd, comm->recv_buffer, BUFFER_SIZE - 1, 0,
                            (struct sockaddr*)&sender_addr, &addr_len);
    if (recv_len == SOCKET_ERROR) {
        int err = WSAGetLastError();
        if (err != WSAEWOULDBLOCK) {
            fprintf(stderr, "Receive failed: %d\n", err);
        }
        return NULL;
    }

    comm->recv_buffer[recv_len] = '\0';

    // Extract packet ID
    char* separator = strchr(comm->recv_buffer, SEPARATOR);
    if (!separator) return comm->recv_buffer;

    size_t id_len = separator - comm->recv_buffer;
    char packet_id[ID_SIZE];
    strncpy(packet_id, comm->recv_buffer, id_len);
    packet_id[id_len] = '\0';

    if (strcmp(packet_id, comm->instance_id) == 0) {
        return NULL; // Self-sent
    }

    return separator + 1;
}
