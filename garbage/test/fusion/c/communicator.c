#include "communicator.h"

Communicator* init_communicator(int listener_port, int destination_port, const char* destination_addr, int REUSEADDR_FLAG, int BROADCAST_FLAG) {
    Communicator* comm = (Communicator*)malloc(sizeof(Communicator));
    if (!comm) {
        perror("Memory allocation failed");
        return NULL;
    }
    // Create socket
    if ((comm->sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Socket creation failed");
        free(comm);
        return NULL;
    }
    //Non-blocking mode
    int flags = fcntl(comm->sockfd, F_GETFL, 0);
    if (fcntl(comm->sockfd, F_SETFL, flags | O_NONBLOCK) < 0) {
        perror("Failed to set socket to non-blocking mode");
        close(comm->sockfd);
        free(comm);
        return NULL;
    }
    
    if (setsockopt(comm->sockfd, SOL_SOCKET, SO_REUSEADDR, &REUSEADDR_FLAG, sizeof(REUSEADDR_FLAG)) < 0) {
        perror("setsockopt SO_REUSEADDR failed");
        close(comm->sockfd);
        free(comm);
        return NULL;
    }
    if (setsockopt(comm->sockfd, SOL_SOCKET, SO_BROADCAST, &BROADCAST_FLAG, sizeof(BROADCAST_FLAG)) < 0) {
        perror("setsockopt SO_BROADCAST failed");
        close(comm->sockfd);
        free(comm);
        return NULL;
    }
    //Receiving address
    memset(&comm->listener_addr, 0, sizeof(comm->listener_addr));
    comm->listener_addr.sin_family = AF_INET;
    comm->listener_addr.sin_port = htons(listener_port);
    comm->listener_addr.sin_addr.s_addr = INADDR_ANY;
    
    //Destination address
    memset(&comm->destination_addr, 0, sizeof(comm->destination_addr));
    comm->destination_addr.sin_family = AF_INET;
    comm->destination_addr.sin_port = htons(destination_port);
    comm->destination_addr.sin_addr.s_addr = inet_addr(destination_addr);
    // Bind socket for receiving
    if (bind(comm->sockfd, (struct sockaddr*)&comm->listener_addr, sizeof(comm->listener_addr)) < 0) {
        perror("Binding socket failed");
        close(comm->sockfd);
        free(comm);
        return NULL;
    }
    printf("[+] Initialized communicator (listener %s:%d, destination %s:%d)\n",inet_ntoa(comm->listener_addr.sin_addr), ntohs(comm->listener_addr.sin_port), inet_ntoa(comm->destination_addr.sin_addr), ntohs(comm->destination_addr.sin_port));
    return comm;
}

int send_query(Communicator* comm, const char* query) {
    int result = sendto(comm->sockfd, query, strlen(query), 0, (struct sockaddr*)&comm->destination_addr, sizeof(comm->destination_addr));
    if (result < 0) {
        if (errno != EAGAIN && errno != EWOULDBLOCK) {
            perror("Send failed");
        }
        return -1;
    }
    printf("[+] Sent: %s\n", query);
    return result;
}

char* receive_query(Communicator* comm) {
    struct sockaddr_in sender_addr;
    socklen_t addr_len = sizeof(sender_addr);
    memset(comm->recv_buffer, 0, BUFFER_SIZE);
    

    int recv_len = recvfrom(comm->sockfd, comm->recv_buffer, BUFFER_SIZE - 1, 0, (struct sockaddr*)&sender_addr, &addr_len);
    const char* sender_ip = inet_ntoa(sender_addr.sin_addr);

    if (recv_len > 0 && strcmp(sender_ip, "127.0.0.1") != 0){
        comm->recv_buffer[recv_len] = '\0';  // Null-terminate the received data
        printf("[+] Received: %s from %s:%d\n", comm->recv_buffer, inet_ntoa(sender_addr.sin_addr), ntohs(sender_addr.sin_port));
        return comm->recv_buffer;  // Correct return value
    
    } else if (recv_len == -1 && errno != EAGAIN && errno != EWOULDBLOCK) {
        perror("Receive failed");
    }
    return NULL;
}

void cleanup_communicator(Communicator* comm) {
    if (comm) {
        close(comm->sockfd);
        free(comm);
        printf("[+] Communicator cleaned up\n");
    }
}