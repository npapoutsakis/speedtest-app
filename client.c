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
#define BUFFER_SIZE 1024

int main(int argc, char *argv[]) {

    int client_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (client_socket == -1) {
        printf("Socket creation failed...\n");
        exit(EXIT_FAILURE);
    }

    // set up the client address structure
    struct sockaddr_in client_addr;
    
    memset(&client_addr, 0, sizeof(client_addr));
    client_addr.sin_family = AF_INET;
    client_addr.sin_addr.s_addr = inet_addr(DEFAULT_IP);
    // client_addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    client_addr.sin_port = htons(PORT);
    
    // attempt to connect to the server    
    if (connect(client_socket, (struct sockaddr *)&client_addr, sizeof(client_addr)) == -1) {
        printf("Connection to server failed...\n");
        exit(EXIT_FAILURE);
    }
    

    char buffer[BUFFER_SIZE];
    int n;
    
    // main client loop
    printf("Connected to server. Type 'exit' to quit.\n");
    while (1) {
        bzero(buffer, BUFFER_SIZE);
        printf("Type a message: ");
        n = 0;
        while ((buffer[n++] = getchar()) != '\n');
        
        send(client_socket, buffer, sizeof(buffer), 0);
        bzero(buffer, BUFFER_SIZE);
        
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("From server: %s", buffer);

        if (strncmp(buffer, "exit", 4) == 0) {
            printf("Exiting...\n");
            break;
        }
    }

    close(client_socket);
    printf("Connection closed.\n");
    return 0;
}