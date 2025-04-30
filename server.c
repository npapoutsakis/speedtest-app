/**
 *  Server
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

// see available ports: cat /etc/services
#define PORT 5000
#define BUFFER_SIZE 1024


int main(int argc, char *argv[]) {
    
    /**
     *  References: 
     *      1. https://www.tutorialspoint.com/unix_sockets/socket_quick_guide.htm
     *      2. https://www.geeksforgeeks.org/tcp-server-client-implementation-in-c/
     */
    
    // create the socket, stream socket because we are using TCP
    int server_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (server_socket == -1) {
        printf("Socket creation failed...\n"); 
        exit(EXIT_FAILURE);
    }
    
    // set up the server address structure
    struct sockaddr_in server_addr;
    
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(PORT);

    // bind the socket to the address and port
    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        printf("Socket binding failed...\n");
        exit(EXIT_FAILURE);
    }

    // listen for incoming connections, 1 is the maximum number of queued connections
    if (listen(server_socket, 1) == -1) {
        printf("Socket listening failed...\n");
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port %d\n", PORT);

    
    struct sockaddr_in client_addr;
    socklen_t client_addr_len = sizeof(client_addr);
    
    // accept a connection from a client
    int client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &client_addr_len);
    if (client_socket == -1) {
        printf("Socket accepting failed...\n");
        exit(EXIT_FAILURE);
    }
    
    // print the client's ip address and port
    printf("Client connected: %s:%d\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
    
    char buffer[BUFFER_SIZE];
    int n;

    // main server loop
    while (1) {
        
        // clear buffer
        bzero(buffer, BUFFER_SIZE);

        // receive data from the client, returns the number of bytes received
        ssize_t bytes_received = recv(client_socket, buffer, sizeof(buffer), 0);
        if (bytes_received <= 0) {
            printf("Client disconnected...\n");
            break;
        }

        // print the received data
        printf("From client: %s\t To client : ", buffer);
        bzero(buffer, BUFFER_SIZE);
        
        n = 0; 
        while ((buffer[n++] = getchar()) != '\n'); 
    
        // send data to the client
        send(client_socket, buffer, strlen(buffer), 0);

        // close the client socket using `exit`
        if (strncmp("exit", buffer, 4) == 0) { 
            printf("Server Exit...\n"); 
            break; 
        } 
    }

    // close the sockets
    close(server_socket);
    printf("Server closed.\n");
    return 0;
}