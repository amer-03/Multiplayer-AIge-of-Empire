// testudp.c - compile with gcc testudp.c -o testudp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(int argc, char* argv[]) {
    if (argc != 4) {
        printf("Usage: %s <mode:send|recv> <ip> <port>\n", argv[0]);
        return 1;
    }

    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    if (!strcmp(argv[1], "recv")) {
        struct sockaddr_in addr;
        addr.sin_family = AF_INET;
        addr.sin_port = htons(atoi(argv[3]));
        addr.sin_addr.s_addr = INADDR_ANY;

        if (bind(sockfd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
            perror("bind failed");
            return 1;
        }

        printf("Listening on port %s\n", argv[3]);

        char buffer[1024];
        struct sockaddr_in sender;
        socklen_t sender_len = sizeof(sender);

        while(1) {
            int recv_len = recvfrom(sockfd, buffer, 1023, 0,
                                   (struct sockaddr*)&sender, &sender_len);
            buffer[recv_len] = '\0';
            printf("Received: %s from %s:%d\n", buffer,
                   inet_ntoa(sender.sin_addr), ntohs(sender.sin_port));
        }
    } else if (!strcmp(argv[1], "send")) {
        struct sockaddr_in addr;
        addr.sin_family = AF_INET;
        addr.sin_port = htons(atoi(argv[3]));
        addr.sin_addr.s_addr = inet_addr(argv[2]);

        char message[1024];
        while(1) {
            printf("Enter message: ");
            fgets(message, 1023, stdin);
            sendto(sockfd, message, strlen(message), 0,
                  (struct sockaddr*)&addr, sizeof(addr));
            printf("Sent to %s:%s\n", argv[2], argv[3]);
        }
    }

    return 0;
}
