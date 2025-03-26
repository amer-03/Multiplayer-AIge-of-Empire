#ifndef GAME_INIT_H
#define GAME_INIT_H

extern int GAME_PORT;

int python_options(Communicator* python_communicator, Communicator* discovery_communicator);
int evaluate_option(Communicator* discovery_communicator, char* query, int* port);
int find_port();
int is_port_free(int port);
void syn_request(Communicator* external_communicator);
void ack_response(Communicator* external_communicator);


#endif