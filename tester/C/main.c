#include "communicator.h"
#include <unistd.h>
#include <time.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main() {
    Communicator* python_communicator = init_communicator(C_PORT1, PYTHON_PORT, LOCALHOST_IP);
    Communicator* external_communicator = init_communicator(C_PORT2, EXTERNAL_PORT, BROADCAST_IP);

    if (!python_communicator || !external_communicator) {
        fprintf(stderr, "Failed to initialize communicators\n");
        return EXIT_FAILURE;    
    }

    PlayersTable* players_table = init_player_table();
    if (!players_table) {
        fprintf(stderr, "Failed to initialize players table\n");
        cleanup_communicator(python_communicator);
        cleanup_communicator(external_communicator);
        return EXIT_FAILURE;
    }

    printf("[+] Starting communication loop (Press Ctrl+C to exit)\n");

    time_t last_discovery_time = 0;
    PacketInfo internal_packet = {0};
    PacketInfo external_packet = {0};

    // Initial discovery broadcast
    send_discovery_broadcast(external_communicator);
    last_discovery_time = time(NULL);

    while (1) {
        // Periodic discovery broadcasts
        if (time(NULL) - last_discovery_time >= DISCOVERY_INTERVAL) {
            send_discovery_broadcast(external_communicator);
            last_discovery_time = time(NULL);

            // Clean up stale players
            cleanup_stale_players(players_table, DISCOVERY_TIMEOUT);
        }

        // Reset packet memory before receiving
        if (internal_packet.sender_id) free(internal_packet.sender_id);
        if (internal_packet.query) free(internal_packet.query);
        if (external_packet.sender_id) free(external_packet.sender_id);
        if (external_packet.query) free(external_packet.query);
        memset(&internal_packet, 0, sizeof(PacketInfo));
        memset(&external_packet, 0, sizeof(PacketInfo));

        // Receive packets only if data is available
        int external_recv_len = receive_buffer(external_communicator, external_packet.sender);
        int internal_recv_len = receive_buffer(python_communicator, internal_packet.sender);

        // Process external packet
        if (external_recv_len > 0) {
            int result = process_buffer(external_communicator, &external_packet);
            if (result > 0 && external_packet.query) {
                int discovery_result = handle_discovery(&external_packet, players_table);

                // If not a discovery message, handle normally
                if (discovery_result < 0) {
                    char sender_ip[INET_ADDRSTRLEN];
                    inet_ntop(AF_INET, &external_packet.sender.sin_addr, sender_ip, INET_ADDRSTRLEN);
                    
                    int player_index = find_player(players_table, sender_ip);
                    if (player_index != -1) {
                        char* buffer = construct_buffer(python_communicator, external_packet.query);
                        send_buffer(python_communicator, buffer);
                        free(buffer);
                    }
                }
            }
        }

        // Process internal packet
        if (internal_recv_len > 0) {
            int result = process_buffer(python_communicator, &internal_packet);
            if (result > 0 && internal_packet.query) {
                printf("Received : %s\n", internal_packet.query);
                char* buffer = construct_buffer(external_communicator, internal_packet.query);
                send_buffer(external_communicator, buffer);
                free(buffer);
            }
        }

        usleep(SLEEP_TIME);
    }

    // Cleanup (this part will never be reached in the current implementation)
    cleanup_communicator(python_communicator);
    cleanup_communicator(external_communicator);
    free(players_table);

    return EXIT_SUCCESS;
}