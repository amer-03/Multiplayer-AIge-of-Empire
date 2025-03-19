#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <time.h>

#define BUFFER_SIZE 1024
#define FLAGS 0
#define MESSAGE_INTERVAL 0 // seconds between messages

typedef struct {
    int sockfd;                     // Socket file descriptor
    struct sockaddr_in send_addr;   // Address to send to
    struct sockaddr_in recv_addr;   // Address to receive on
    char recv_buffer[BUFFER_SIZE];  // Buffer for receiving messages
    int recv_port;                  // Port to listen on
    int send_port;                  // Port to send to
    char* send_ip;                  // IP to send to
    time_t last_send_time;          // Time of last message sent
} CythonCommunicator;

// Initialize the communicator
CythonCommunicator* init_communicator(int recv_port, int send_port, const char* send_ip) {
    CythonCommunicator* comm = (CythonCommunicator*)malloc(sizeof(CythonCommunicator));
    if (!comm) {
        perror("Memory allocation failed");
        return NULL;
    }

    // Store configuration
    comm->recv_port = recv_port;
    comm->send_port = send_port;
    comm->send_ip = strdup(send_ip);
    comm->last_send_time = 0;

    // Create socket
    if ((comm->sockfd = socket(AF_INET, SOCK_DGRAM, FLAGS)) < 0) {
        perror("Socket creation failed");
        free(comm->send_ip);
        free(comm);
        return NULL;
    }

    // Set socket to non-blocking mode
    int flags = fcntl(comm->sockfd, F_GETFL, 0);
    if (fcntl(comm->sockfd, F_SETFL, flags | O_NONBLOCK) < 0) {
        perror("Failed to set socket to non-blocking mode");
        close(comm->sockfd);
        free(comm->send_ip);
        free(comm);
        return NULL;
    }

    // Configure receiving address
    memset(&comm->recv_addr, 0, sizeof(comm->recv_addr));
    comm->recv_addr.sin_family = AF_INET;
    comm->recv_addr.sin_addr.s_addr = INADDR_ANY;
    comm->recv_addr.sin_port = htons(recv_port);

    // Configure sending address
    memset(&comm->send_addr, 0, sizeof(comm->send_addr));
    comm->send_addr.sin_family = AF_INET;
    comm->send_addr.sin_addr.s_addr = inet_addr(send_ip);
    comm->send_addr.sin_port = htons(send_port);

    // Bind socket for receiving
    if (bind(comm->sockfd, (struct sockaddr*)&comm->recv_addr, sizeof(comm->recv_addr)) < 0) {
        perror("Binding socket failed");
        close(comm->sockfd);
        free(comm->send_ip);
        free(comm);
        return NULL;
    }

    printf("[+] Initialized communicator (recv_port: %d, send_port: %d, send_ip: %s)\n",
           recv_port, send_port, send_ip);
    return comm;
}

// Send a message
int send_message(CythonCommunicator* comm, const char* message) {
    int result = sendto(comm->sockfd, message, strlen(message), 0,
                       (struct sockaddr*)&comm->send_addr, sizeof(comm->send_addr));
    if (result < 0) {
        if (errno != EAGAIN && errno != EWOULDBLOCK) {
            perror("Send failed");
        }
        return -1;
    }
    printf("[+] Sent: %s\n", message);
    return result;
}

// Receive a message (non-blocking)
int receive_message(CythonCommunicator* comm) {
    struct sockaddr_in sender_addr;
    socklen_t addr_len = sizeof(sender_addr);

    int recv_len = recvfrom(comm->sockfd, comm->recv_buffer, BUFFER_SIZE - 1, 0,
                           (struct sockaddr*)&sender_addr, &addr_len);

    if (recv_len > 0) {
        comm->recv_buffer[recv_len] = '\0';
        printf("[+] Received: %s from %s:%d\n", comm->recv_buffer,
               inet_ntoa(sender_addr.sin_addr), ntohs(sender_addr.sin_port));
        return recv_len;
    } else if (errno != EAGAIN && errno != EWOULDBLOCK) {
        perror("Receive failed");
    }

    return -1;
}

// Check if it's time to send a new message
int should_send_message(CythonCommunicator* comm) {
    time_t current_time = time(NULL);
    if (current_time - comm->last_send_time >= MESSAGE_INTERVAL) {
        comm->last_send_time = current_time;
        return 1;
    }
    return 0;
}

// Clean up resources
void cleanup_communicator(CythonCommunicator* comm) {
    if (comm) {
        close(comm->sockfd);
        free(comm->send_ip);
        free(comm);
        printf("[+] Communicator cleaned up\n");
    }
}

// Main function
int main() {
    // Initialize communicator (listening on 50001, sending to 50000)
    CythonCommunicator* comm = init_communicator(50001, 50000, "127.0.0.1");
    if (!comm) {
        fprintf(stderr, "Failed to initialize communicator\n");
        return EXIT_FAILURE;
    }

    printf("[+] Starting communication loop (Press Ctrl+C to exit)\n");

    // Main loop
    while (1) {
        // Check for received messages
        receive_message(comm);

        // Send periodic message
        if (should_send_message(comm)) {
            send_message(comm, "message from C");
        }

        // Sleep a little to prevent CPU hogging
        usleep(10000);  // 10ms
    }

    // Clean up (this part won't be reached due to infinite loop)
    cleanup_communicator(comm);
    return EXIT_SUCCESS;
}
