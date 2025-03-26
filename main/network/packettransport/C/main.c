#include "include.h"

int main() {
    PacketInfo internal_packet = {0};
    PacketInfo external_packet = {0};
    PacketInfo discovery_packet = {0};

    Communicator* python_communicator = init_communicator(C_PORT1, PYTHON_PORT, LOCALHOST_IP);
    Communicator* discovery_communicator = init_communicator(DISCOVERY_PORT, DISCOVERY_PORT, BROADCAST_IP);
    
    if (!python_communicator || !discovery_communicator) {
        fprintf(stderr, "Failed to initialize communicators\n");
        return EXIT_FAILURE;
    }

    int GAME_PORT = python_options(python_communicator, discovery_communicator);
    
    Communicator* external_communicator = init_communicator(GAME_PORT, GAME_PORT, BROADCAST_IP);
    PlayersTable* players_table = init_player_table();
    printf("==============================\n");
    printf("[+] Starting communication loop (Game Port: %d)\n", GAME_PORT);
    printf("==============================\n");
    
    if (!players_table || !external_communicator) {
        fprintf(stderr, "Failed to initialize players table or external communicator\n");
        cleanup_communicator(python_communicator);
        cleanup_communicator(discovery_communicator);
        return EXIT_FAILURE;
    }

    syn_request(external_communicator);

    int last_discovery_time = time(NULL);

    while (1) {
        // Periodic discovery broadcasts
        if (time(NULL) - last_discovery_time >= SYNC_INTERVAL) {
            syn_request(external_communicator);
            last_discovery_time = time(NULL);
        }

        // Reset packet memory before receiving
        reset_packet(&internal_packet);
        reset_packet(&external_packet);
        reset_packet(&discovery_packet);

        struct sockaddr_in sender = {0};

        // Receive packets only if data is available
        int internal_recv_len = receive_buffer(python_communicator, &sender);
        internal_packet.sender = sender;

        int external_recv_len = receive_buffer(external_communicator, &sender);
        external_packet.sender = sender;
        
        int discovery_recv_len = receive_buffer(discovery_communicator, &sender);
        discovery_packet.sender = sender;

        // Process external packet
        if (external_recv_len > 0) {
            int result = process_buffer(external_communicator, &external_packet);
            if (result > 0 && external_packet.query) {
                add_player(players_table, &external_packet);
                char* buffer = construct_buffer(python_communicator, external_packet.query);
                
                if(strcmp(external_packet.query, ACK_RESPONSE) != 0 && strcmp(external_packet.query, SYNC_QUERY) != 0 ){
                    send_buffer(python_communicator, buffer);
                }
                
                else if(!strcmp(external_packet.query, SYNC_QUERY)){
                    ack_response(external_communicator);
                }
                
                free(buffer);
            }
        }

        // Process internal packet
        if (internal_recv_len > 0) {
            int result = process_buffer(python_communicator, &internal_packet);
            if (result > 0 && internal_packet.query) {
                char* buffer;
                if(internal_packet.query[0] == 'R'){
                    char* request_buffer = malloc(BUFFER_SIZE * sizeof(char));
                    buffer = construct_buffer(discovery_communicator, internal_packet.query);
                    snprintf(request_buffer, BUFFER_SIZE, "%s:%d", buffer, GAME_PORT);
                    send_discovery_broadcast(discovery_communicator, request_buffer);
                    free(request_buffer);  // Free the temporary buffer
                } else {
                    buffer = construct_buffer(external_communicator, internal_packet.query);
                    send_to_all(players_table, external_communicator, buffer);
                }
                free(buffer);
            }
        }

        if (discovery_recv_len > 0) {
            int result = process_buffer(discovery_communicator, &discovery_packet);
            if (result > 0 && discovery_packet.query) {
                char* buffer = construct_buffer(python_communicator, discovery_packet.query);
                if(external_packet.query != NULL && strcmp(external_packet.query, ACK_RESPONSE) != 0 && strcmp(external_packet.query, SYNC_QUERY) != 0){
                    send_buffer(python_communicator, buffer);
                }
                free(buffer);
            }
        }

        usleep(SLEEP_TIME);
    }

    // Cleanup (this part will never be reached in the current infinite loop)
    cleanup_communicator(python_communicator);
    cleanup_communicator(discovery_communicator);
    cleanup_communicator(external_communicator);
    free(players_table);

    return EXIT_SUCCESS;
}