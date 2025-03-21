#include "communicator.h"
#include <time.h>

int main() {
    Communicator* python_communicator = init_communicator(C_PORT1, PYTHON_PORT, LOCALHOST_IP, TRUE, TRUE);
    Communicator* external_communicator = init_communicator(C_PORT2, EXTERNAL_PORT, BROADCAST_IP, TRUE, TRUE);
    
    if (!python_communicator || !external_communicator) {
        fprintf(stderr, "Failed to initialize communicators\n");
        return EXIT_FAILURE;
    }
    
    printf("[+] Starting communication loop (Press Ctrl+C to exit)\n");
    
    // Variables to track packet statistics
    int sent_packets = 0;
    int received_packets = 0;
    time_t last_stats_time = time(NULL);
    
    while (1) {
        // Get current time
        time_t current_time = time(NULL);
        
        // Receive queries from both communicators
        char* internal_query = receive_packet(python_communicator);
        char* external_query = receive_packet(external_communicator);
        
        // Count received packets
        if (internal_query != NULL) {
            received_packets++;
        }
        if (external_query != NULL) {
            received_packets++;
        }
        
        // Process the external query if it exists
        if (external_query != NULL) {
            send_packet(python_communicator, external_query);
            sent_packets++;
        }
        
        // Process the internal query if it exists
        if (internal_query != NULL) {
            send_packet(external_communicator, internal_query);
            sent_packets++;
        }
        
        // Check if a second has passed and print statistics
        if (current_time > last_stats_time) {
            printf("[STATS] Sent: %d packets/sec | Received: %d packets/sec\n", 
                   sent_packets, received_packets);
            
            // Reset counters and update the time
            sent_packets = 0;
            received_packets = 0;
            last_stats_time = current_time;
        }
        
        usleep(SLEEP_TIME);
    }
    
    cleanup_communicator(python_communicator);
    cleanup_communicator(external_communicator);
    
    return EXIT_SUCCESS;
}