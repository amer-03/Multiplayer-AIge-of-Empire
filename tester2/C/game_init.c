#include "include.h"
int GAME_PORT = 0;

int python_options(Communicator* python_communicator, Communicator* discovery_communicator){
	if (!python_communicator) {
        fprintf(stderr, "Failed to initialize python communicators\n");
        return EXIT_FAILURE;    
    }

    PacketInfo internal_packet = {0};
    PacketInfo discovery_packet = {0};
    int port = 0;

    while (!port) {
        reset_packet(&internal_packet);
        reset_packet(&discovery_packet);

        // Receive packets only if data is available
        int internal_recv_len = receive_buffer(python_communicator, &(internal_packet.sender));
        int discovery_recv_len = receive_buffer(discovery_communicator, &(discovery_packet.sender));


        if (discovery_recv_len > 0) {
            int result = process_buffer(discovery_communicator, &discovery_packet);
            if (result > 0 && discovery_packet.query) {
                printf("Received : %s\n", discovery_packet.query);
				char* buffer = construct_buffer(python_communicator, discovery_packet.query);
                send_buffer(python_communicator, buffer);
                free(buffer);
            }
        }
        // Process internal packet
        if (internal_recv_len > 0) {
            int result = process_buffer(python_communicator, &internal_packet);
            if (result > 0 && internal_packet.query) {
                printf("Received : %s\n", internal_packet.query);
                evaluate_option(discovery_communicator, internal_packet.query, &port);
            }
        }

     usleep(SLEEP_TIME);
    }

    return port;

}

int evaluate_option(Communicator* discovery_communicator, char* query, int* port){
	if(query[0] == 'D'){
		send_discovery_broadcast(discovery_communicator, query);
	}
	
	else if(query[0] == 'J') {
		*port = atoi(&query[1]); 
		return *port;
	}
	
	else if(query[0] == 'C') {
		*port = find_port();
		return *port;
	}
	return 0;

}

int find_port() {
    int sockfd;
    struct sockaddr_in addr;

    for (int port = 50003; port <= 50010; port++) {
        sockfd = socket(AF_INET, SOCK_STREAM, 0);
        if (sockfd < 0) {
            perror("Socket creation failed");
            continue;
        }

        memset(&addr, 0, sizeof(addr));
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = INADDR_ANY;
        addr.sin_port = htons(port);

        if (bind(sockfd, (struct sockaddr*)&addr, sizeof(addr)) == 0) {
            close(sockfd);
            return port;
        }

        close(sockfd);
    }

    return -1;
}


void syn_request(Communicator* external_communicator) {
    char* buffer = construct_buffer(external_communicator, SYNC_QUERY);
    send_buffer(external_communicator, buffer);
    printf("[+] Sent SYN\n");
}

void ack_response(Communicator* external_communicator) {
    char* buffer = construct_buffer(external_communicator, ACK_RESPONSE);
    send_buffer(external_communicator, buffer);
    printf("[+] Sent ACK\n");
}
