#include "CythonCommunicator.h"

int main() {
    CythonCommunicator* comm = init_communicator(50001, 50000, "127.0.0.1");
    if (!comm) {
        fprintf(stderr, "Failed to initialize communicator\n");
        return EXIT_FAILURE;
    }

    printf("[+] Starting communication loop (Press Ctrl+C to exit)\n");

    while (1) {
        receive_message(comm);
        if (should_send_message(comm)) {
            send_message(comm, "message from C");
        }
        usleep(10000);
    }

    // Clean up (this part won't be reached due to infinite loop)
    cleanup_communicator(comm);
    return EXIT_SUCCESS;
}
