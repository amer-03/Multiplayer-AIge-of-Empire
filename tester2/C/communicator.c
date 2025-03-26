#include "include.h"

extern int GAME_PORT;

void generate_instance_id(Communicator* comm) {
    srand(time(NULL) ^ getpid());
    snprintf(comm->instance_id, ID_SIZE, "%08X", rand() % 0xFFFFFFFF);
}

Communicator* init_communicator(int listener_port, int destination_port, const char* destination_addr) {
    Communicator* comm = (Communicator*)malloc(sizeof(Communicator));
    if (!comm) {
        perror("Memory allocation failed");
        return NULL;
    }
    
    // Initialize recv_buffer to zero
    memset(comm->recv_buffer, 0, BUFFER_SIZE);

    // Generate random unique ID
    generate_instance_id(comm);

    if ((comm->sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Socket creation failed");
        free(comm);
        return NULL;
    }

    // Non-blocking mode
    int flags = fcntl(comm->sockfd, F_GETFL, 0);
    if (fcntl(comm->sockfd, F_SETFL, flags | O_NONBLOCK) < 0) {
        perror("Failed to set socket to non-blocking mode");
        close(comm->sockfd);
        free(comm);
        return NULL;
    }
    
    int reuseaddr = REUSEADDR_FLAG;
    if (setsockopt(comm->sockfd, SOL_SOCKET, SO_REUSEADDR, &reuseaddr, sizeof(reuseaddr)) < 0) {
        perror("setsockopt SO_REUSEADDR failed");
        close(comm->sockfd);
        free(comm);
        return NULL;
    }

    int broadcast = BROADCAST_FLAG;
    if (setsockopt(comm->sockfd, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast)) < 0) {
        perror("setsockopt SO_BROADCAST failed");
        close(comm->sockfd);
        free(comm);
        return NULL;
    }

    int receive_buff = RCVBUF_SIZE;
    if (setsockopt(comm->sockfd, SOL_SOCKET, SO_RCVBUF, &receive_buff, sizeof(receive_buff)) < 0) {
        perror("setsockopt SO_RCVBUF failed");
        close(comm->sockfd);
        free(comm);
        return NULL;
    }

    int send_buff = SNDBUF_SIZE;
    if (setsockopt(comm->sockfd, SOL_SOCKET, SO_SNDBUF, &send_buff, sizeof(send_buff)) < 0) {
        perror("setsockopt SO_SNDBUF failed");
        close(comm->sockfd);
        free(comm);
        return NULL;
    }

    int priority = SOCKET_PRIORITY;
    if(setsockopt(comm->sockfd, SOL_SOCKET, SO_PRIORITY, &priority, sizeof(priority)) < 0){
        perror("setsockopt SO_PRIORITY failed");
        close(comm->sockfd);
        free(comm);
        return NULL;
    }

    // Receiving address
    memset(&comm->listener_addr, 0, sizeof(comm->listener_addr));
    comm->listener_addr.sin_family = AF_INET;
    comm->listener_addr.sin_port = htons(listener_port);
    comm->listener_addr.sin_addr.s_addr = INADDR_ANY;
    
    // Destination address
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

    printf("[+] Initialized communicator (ID: %s | Listening on %d | Destination %d)\n",  
           comm->instance_id, ntohs(comm->listener_addr.sin_port), ntohs(comm->destination_addr.sin_port));
    printf("[+] Socket Options :\n");
    printf("\t[~] Non-blocking mode enabled\n");
    printf("\t[~] SO_REUSEADDR: %d\n", reuseaddr);
    printf("\t[~] SO_BROADCAST: %d\n", broadcast);
    printf("\t[~] SO_RCVBUF: %d bytes\n", receive_buff);
    printf("\t[~] SO_SNDBUF: %d bytes\n", send_buff);
    printf("\t[~] SO_PRIORITY: %d\n", priority);

    return comm;
}

PlayersTable* init_player_table() {
    // Allocate memory for the table
    PlayersTable* Ptable = malloc(sizeof(PlayersTable));
    if (Ptable == NULL) {
        perror("Memory allocation failed for player table");
        return NULL;
    }
    
    // Initialize the table
    Ptable->count = 0;
    memset(Ptable->players, 0, sizeof(Ptable->players));
    
    return Ptable;
}

// Function to initialize PacketInfo
void initPacketInfo(PacketInfo* packetInfo, struct sockaddr_in sender, const char* sender_id, const char* query, int id) {
    packetInfo->sender = sender;
    packetInfo->sender_id = strdup(sender_id);
    packetInfo->query = strdup(query);
    packetInfo->id = id;
}

// Function to reset PacketInfo
void reset_packet(PacketInfo* packetInfo) {
    if (packetInfo) {
        // Only free if not already NULL
        if (packetInfo->sender_id) {
            free(packetInfo->sender_id);
            packetInfo->sender_id = NULL;
        }
        if (packetInfo->query) {
            free(packetInfo->query);
            packetInfo->query = NULL;
        }
        memset(&packetInfo->sender, 0, sizeof(struct sockaddr_in));
        packetInfo->id = 0;
    }
}

// Function to initialize PlayerInfo
void initPlayerInfo(PlayerInfo* playerInfo, const char* ip, const int port, const char* instance_id) {
    // Null checks
    if (playerInfo == NULL || ip == NULL || instance_id == NULL) {
        fprintf(stderr, "Error: Null parameter passed to initPlayerInfo\n");
        return;
    }

    // Safely copy IP
    strncpy(playerInfo->ip, ip, INET_ADDRSTRLEN - 1);
    playerInfo->ip[INET_ADDRSTRLEN - 1] = '\0';  // Ensure null-termination

    // Safely copy instance ID
    strncpy(playerInfo->instance_id, instance_id, ID_SIZE - 1);
    playerInfo->instance_id[ID_SIZE - 1] = '\0';  // Ensure null-termination

    // Set port
    playerInfo->port = port;

    // Logging
    printf("Player added - IP: %s, Port: %d, Instance ID: %s\n", 
           playerInfo->ip, playerInfo->port, playerInfo->instance_id);

    // Initialize other fields
    playerInfo->last_seen = time(NULL);
    playerInfo->PacketsCount = 0;
}

// Function to reset PlayerInfo
void resetPlayerInfo(PlayerInfo* playerInfo) {
    memset(playerInfo->ip, 0, INET_ADDRSTRLEN);
    memset(playerInfo->instance_id, 0, ID_SIZE);
    playerInfo->last_seen = 0;
    playerInfo->PacketsCount = 0;
}

char* construct_buffer(Communicator* comm, const char* query) {
    char* buffer = malloc(BUFFER_SIZE * sizeof(char));
    if (ntohs(comm->destination_addr.sin_port) != PYTHON_PORT){
        snprintf(buffer, BUFFER_SIZE, "%s%c%s", comm->instance_id, SEPARATOR, query);
    } else {
        strncpy(buffer, query, BUFFER_SIZE - 1);
        buffer[BUFFER_SIZE - 1] = '\0';
    }

    return buffer;
}

int process_buffer(Communicator* comm, PacketInfo* packet) {
    // Use strlen to check if buffer contains data, instead of address comparison
    if (!packet || strlen(comm->recv_buffer) == 0) return -1;

    char* buffer = comm->recv_buffer;
    char* separator = strchr(buffer, SEPARATOR);
    
    // Free existing memory to prevent leaks
    if (packet->sender_id) {
        free(packet->sender_id);
        packet->sender_id = NULL;
    }
    if (packet->query) {
        free(packet->query);
        packet->query = NULL;
    }
    
    if (!separator) {
        packet->query = strdup(buffer);
        return packet->query ? 1 : -1;
    }
    
    size_t id_length = separator - buffer;
    size_t copy_size = (id_length < ID_SIZE - 1) ? id_length : ID_SIZE - 1;
    
    // Allocate memory for sender_id
    packet->sender_id = malloc(ID_SIZE * sizeof(char));
    if (packet->sender_id == NULL) {
        perror("Memory allocation failed for sender_id");
        return -1;
    }

    // Check if the packet is from ourselves
    if (strncmp(buffer, comm->instance_id, copy_size) == 0){
        printf("[+] Self req = Ignore\n");
        free(packet->sender_id);
        packet->sender_id = NULL;
        return 0;
    }

    // Copy sender ID
    memcpy(packet->sender_id, buffer, copy_size);
    packet->sender_id[copy_size] = '\0';

    // Copy query
    packet->query = strdup(separator + 1);
    if (packet->query == NULL) {
        perror("Memory allocation failed for query");
        free(packet->sender_id);
        packet->sender_id = NULL;
        return -1;
    }
    
    return 1;
}
int send_buffer(Communicator* comm, const char* buffer) {
    int result = sendto(comm->sockfd, buffer, strlen(buffer), 0, (struct sockaddr*)&comm->destination_addr, sizeof(comm->destination_addr));
    if (result < 0) {
        if (errno != EAGAIN && errno != EWOULDBLOCK) {
            perror("Send failed");
        }
        return -1;
    }
    char ip_str[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &comm->destination_addr.sin_addr, ip_str, sizeof(ip_str));
    if(result > 0) printf("[+] Sent %d bytes to %s:%d (%s)\n", result, ip_str, ntohs(comm->destination_addr.sin_port),buffer);
    return result;
}

int receive_buffer(Communicator* comm, struct sockaddr_in* sender) {
    socklen_t sender_len = sizeof(*sender);
    memset(sender, 0, sizeof(*sender));  // Correctly zeroing out sender
    int recv_len = recvfrom(comm->sockfd, comm->recv_buffer, BUFFER_SIZE - 1, 0, (struct sockaddr*)sender, &sender_len);
    
    if (recv_len <= 0) {
        if (recv_len == -1 && errno != EAGAIN && errno != EWOULDBLOCK) {
            perror("Receive failed");
        }
        return 0;
    }

    char ip_str[INET_ADDRSTRLEN];
    if (inet_ntop(AF_INET, &(sender->sin_addr), ip_str, sizeof(ip_str)) == NULL) {
         fprintf(stderr, "Failed to convert IP address\n");
         strcpy(ip_str, "Unknown");
    }

    comm->recv_buffer[recv_len] = '\0';

    printf("[+] Received %d bytes from %s:%d (%s)\n", recv_len, ip_str, ntohs(sender->sin_port), comm->recv_buffer);

    return recv_len;
}

void cleanup_communicator(Communicator* comm) {
    if (comm) {
        close(comm->sockfd);
        free(comm);
        printf("[+] Communicator cleaned up\n");
    }
}

int find_player(PlayersTable* Ptable, PacketInfo* packet) {
    for (int i = 0; i < Ptable->count; i++) {
        if (strcmp(Ptable->players[i].instance_id, packet->sender_id) == 0) {
            // Player exists, update last_seen and PacketsCount
            Ptable->players[i].last_seen = time(NULL);
            Ptable->players[i].PacketsCount += 1;
            return i;
        }
    }

    return -1;
}

int add_player(PlayersTable* PTable, PacketInfo* packet) {
    if (PTable->count >= MAX_PLAYERS) {
        printf("Players table is full. Cannot add more players.\n");
        return -1;
    }

    // Detailed debugging of sender information
    char ip_str[INET_ADDRSTRLEN] = "UNKNOWN";
    int port = 0;

    // Attempt to convert IP
    if (packet->sender.sin_family == AF_INET) {
        if (inet_ntop(AF_INET, &(packet->sender.sin_addr), ip_str, INET_ADDRSTRLEN) == NULL) {
            perror("Failed to convert IP address");
        }
        
        // Convert port from network to host order
        port = ntohs(packet->sender.sin_port);
    }

    // Critical null check for sender_id
    if (packet->sender_id == NULL) {
        return -1;
    }

    // Check if player already exists
    int existing_index = find_player(PTable, packet);
    if (existing_index < 0) {
        // Add new player
        PlayerInfo new_player;
        initPlayerInfo(&new_player, ip_str, port, packet->sender_id);

        // Add to players table
        PTable->players[PTable->count] = new_player;
        PTable->count += 1;

        printf("[+] Added new player: %s:%d (Instance ID: %s)\n", ip_str, port, packet->sender_id);
        print_players(PTable);
        return PTable->count - 1;
    }
    
    // Update existing player's last seen and packet count
    PTable->players[existing_index].last_seen = time(NULL);
    PTable->players[existing_index].PacketsCount += 1;
    
    return existing_index;
}

void cleanup_players(PlayersTable* PTable) {
    time_t current_time = time(NULL);
    int i = 0;
    // Loop through the players table
    while (i < PTable->count) {
        // Check if the player has been inactive for too long
        if (difftime(current_time, PTable->players[i].last_seen) > SYNC_INTERVAL) {
            printf("[!] Removing inactive player: %s (Last seen: %ld seconds ago)\n", PTable->players[i].instance_id, (long)difftime(current_time, PTable->players[i].last_seen));

            // Shift players to overwrite the removed one
            for (int j = i; j < PTable->count - 1; j++) {
                PTable->players[j] = PTable->players[j + 1];
            }

            PTable->count--;
        } else {
            // Move to the next player if current one is active
            i++;
        }
    }
}


void remove_player(char* sender_id, PlayersTable* playersTable) {
    for (int i = 0; i < playersTable->count; i++) {
        if (strcmp(playersTable->players[i].instance_id, sender_id) == 0) {
            // Shift remaining players
            for (int j = i; j < playersTable->count - 1; j++) {
                playersTable->players[j] = playersTable->players[j + 1];
            }
            playersTable->count--;
            printf("Removed player: %s\n", sender_id);
            return;
        }
    }
    printf("Player %s not found.\n", sender_id);
}

// Print all players (for debugging)
void print_players(PlayersTable* Ptable) {
    printf("Known players (%d):\n", Ptable->count);
    for (int i = 0; i < Ptable->count; i++) {
        printf("%d. IP_PORT: %s~%d, Instance ID: %s, Last Seen: %ld, Nb Packets: %d\n", 
               i+1, Ptable->players[i].ip, Ptable->players[i].port, Ptable->players[i].instance_id, 
               Ptable->players[i].last_seen, Ptable->players[i].PacketsCount);
    }
}

void send_discovery_broadcast(Communicator* external_communicator, char* QUERY) {
    send_buffer(external_communicator, QUERY);
    printf("[+] Sent to broadcast\n");
}

int send_to_player(Communicator* comm, struct sockaddr_in player_addr, const char* buffer) {
    // Copy the player's address to the communicator's destination address
    memcpy(&comm->destination_addr, &player_addr, sizeof(struct sockaddr_in));

    // Send buffer to the specific player
    int result = send_buffer(comm, buffer);

    return result;
}

int send_to_all(PlayersTable* Ptable, Communicator* comm, const char* buffer) {
    int total_sent = 0;
    for (int i = 0; i < Ptable->count; i++) {
        inet_pton(AF_INET, Ptable->players[i].ip, &comm->destination_addr.sin_addr);
        int result = send_buffer(comm, buffer);
        if (result > 0) {
            total_sent++;
        }
    }
    if ( Ptable->count == 0 ) send_buffer(comm, buffer);
    return total_sent;
}