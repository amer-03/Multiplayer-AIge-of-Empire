#include "communicator.h"
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <windows.h> // pour Sleep

int main() {
    Communicator* python_communicator = init_communicator(C_PORT1, PYTHON_PORT, LOCALHOST_IP);
    Communicator* external_communicator = init_communicator(C_PORT2, EXTERNAL_PORT, BROADCAST_IP);

    if (!python_communicator || !external_communicator) {
        fprintf(stderr, "[-] Failed to initialize communicators\n");
        return EXIT_FAILURE;
    }

    printf("[+] Communication loop started (Ctrl+C to stop)\n");

    // Statistiques (facultatives)
    int internal_total_receive = 0;
    int external_total_receive = 0;
    int internal_total_sent = 0;
    int external_total_sent = 0;
    int internal_packet_lost = 0;
    int external_packet_lost = 0;

    double internal_total_size = 0.0;
    double external_total_size = 0.0;

    while (1) {
        // Écoute des deux côtés
        char* internal_query = receive_packet(python_communicator);
        char* external_query = receive_packet(external_communicator);

        // Statistiques si un message est reçu
        if (internal_query != NULL) {
            internal_total_receive++;
            internal_total_size += (double)strlen(internal_query) / 1024.0;

            if (atoi(internal_query) - internal_packet_lost != internal_total_receive) {
                internal_packet_lost++;
            }

            send_packet(external_communicator, internal_query);
            external_total_sent++;
        }

        if (external_query != NULL) {
            external_total_receive++;
            external_total_size += (double)strlen(external_query) / 1024.0;

            if (atoi(external_query) - external_packet_lost != external_total_receive) {
                external_packet_lost++;
            }

            send_packet(python_communicator, external_query);
            internal_total_sent++;
        }

        Sleep(SLEEP_TIME_MS); // Temporisation
    }

    cleanup_communicator(python_communicator);
    cleanup_communicator(external_communicator);

    return EXIT_SUCCESS;
}
