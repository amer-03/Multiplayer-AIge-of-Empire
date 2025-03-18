// read the file from the sender, write it in obj.pickle
// recv.c : Réception d'un fichier .pickle via UDP sur le port 50003
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define BUF_SIZE 1024
#define PORT 50002

void receive_pickle() {
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in local_addr, sender_addr;
    socklen_t sender_len = sizeof(sender_addr);

    local_addr.sin_family = AF_INET;
    local_addr.sin_port = htons(PORT);
    local_addr.sin_addr.s_addr = INADDR_ANY;

    if (bind(sockfd, (struct sockaddr*)&local_addr, sizeof(local_addr)) < 0) {
        perror("bind");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    char buffer[BUF_SIZE];
    char filename[256];
    int n;

    n = recvfrom(sockfd, filename, sizeof(filename), 0, (struct sockaddr*)&sender_addr, &sender_len);
    if (n <= 0) {
        perror("recvfrom filename");
        close(sockfd);
        exit(EXIT_FAILURE);
    }
    filename[n] = '\0';

    printf("Réception du fichier : %s\n", filename);

    FILE *file = fopen(filename, "wb");
    if (!file) {
        perror("fopen");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    while (1) {
        n = recvfrom(sockfd, buffer, BUF_SIZE, 0, (struct sockaddr*)&sender_addr, &sender_len);
        if (n <= 0) continue;

        buffer[n] = '\0';
        if (strcmp(buffer, "__END__") == 0)
            break;

        fwrite(buffer, 1, n, file);
    }

    printf("'%s' reçu et enregistré avec succès.\n", filename);

    fclose(file);
    close(sockfd);
}

int main() {
    printf("En écoute sur le port %d...\n", PORT);
    receive_pickle();
    return 0;
}
