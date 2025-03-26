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


int is_port_free(int port) {
    Communicator* comm = init_communicator(port, port, BROADCAST_IP);
    if (comm == NULL) {
        return -1;  // Initialization failed
    }

    int last_discovery_time = time(NULL);
    syn_request(comm);
    
    struct sockaddr_in sender = {0};
    PacketInfo packet = {0};
    
    while(time(NULL) - last_discovery_time < 5) {
        // Clear packet before each receive
        memset(&packet, 0, sizeof(PacketInfo));
        
        int len = receive_buffer(comm, &sender);
        if(len > 0) {
            process_buffer(comm, &packet);
            // Safely check if query is not NULL and matches ACK_RESPONSE
            if(packet.query != NULL && strcmp(packet.query, ACK_RESPONSE) == 0) {
                free(comm);
                return 0;  // Port is not free
            } 
        }
    }
    
    free(comm);
    printf("FREEEEEEE");
    return 1;  // Port is free
}

int find_port() {
    int bind_sockfd;  // Declare bind_sockfd instead of sockfd
    
    // Extended range of ports to search
    for (int port = 50003; port <= 50010; port++) {
        // First, check if we can bind to the port
        bind_sockfd = socket(AF_INET, SOCK_STREAM, 0);
        if (bind_sockfd < 0) {
            perror("Socket creation failed");
            continue;
        }
        
        struct sockaddr_in addr;
        memset(&addr, 0, sizeof(addr));
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = INADDR_ANY;
        addr.sin_port = htons(port);
        
        // Try to bind
        if (bind(bind_sockfd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
            close(bind_sockfd);
            continue;
        }
        close(bind_sockfd);
        
        // If we can bind, do an additional check for port availability
        if (is_port_free(port)) {
            return port;
        }
    }
    
    // No free port found
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
