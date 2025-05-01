/**
 *  Client
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define DEFAULT_IP "147.27.4.22"
#define PORT 5000

int main(int argc, char *argv[]) {

    if (argc != 2) {
        printf("Usage: %s <server_ip>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    // create client socket
    int client_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (client_socket == -1) {
        printf("Socket creation failed...\n");
        exit(EXIT_FAILURE);
    }
    
    // set up the client address structure
    struct sockaddr_in client_addr;
    
    memset(&client_addr, 0, sizeof(client_addr));
    client_addr.sin_family = AF_INET;
    client_addr.sin_addr.s_addr = inet_addr(argv[1]);
    client_addr.sin_port = htons(PORT);
    
    // need to check the queue size

    // attempt to connect to the server    
    if (connect(client_socket, (struct sockaddr *)&client_addr, sizeof(client_addr)) == -1) {
        printf("Connection to server failed...\n");
        exit(EXIT_FAILURE);
    }
    printf("[CLIENT] Connected to server at %s:%d\n", DEFAULT_IP, PORT);    
    printf("[CLIENT] Type 'exit' to quit.\n");
    
    // main client loop
    while (1) {
        char buffer[1024];
        printf("[CLIENT]: ");
        memset(buffer, 0, sizeof(buffer));
        
        int n = 0;
        while ((buffer[n++] = getchar()) != '\n');

        send(client_socket, buffer, strlen(buffer), 0);

        // check for exit command
        if (strncmp(buffer, "exit", 4) == 0) {
            break;
        }
        
        // send message to server
        memset(buffer, 0, sizeof(buffer));

        // receive response from server
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("[SERVER]: %s\n", buffer);
    }


    close(client_socket);
    printf("Connection closed.\n");
    return 0;
}