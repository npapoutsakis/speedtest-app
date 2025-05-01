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

// Ref: Beej’s Guide to Network Programming (pg 12) --> see available ports: cat /etc/services
#define PORT 5000


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
    if (listen(server_socket, 0) == -1) {
        printf("Socket listening failed...\n");
        exit(EXIT_FAILURE);
    }

    printf("[SERVER] Server listening on port %d\n", PORT);

    
    // main server loop
    while (1) {

        struct sockaddr_in client_addr;
        socklen_t client_addr_len = sizeof(client_addr);

        // accept a connection from a client
        int client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &client_addr_len);
        if (client_socket == -1) {
            printf("Socket accepting failed...\n");
            exit(EXIT_FAILURE);
        }
        printf("[SERVER] Client %s:%d connected\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));

        
        // while (1) {  }
        /** 
         *  0. The test will be 30 seconds long
         *  1. Server alwayes listens for incoming connections (has wireless connection to ap)
         *  2. Server will print the data sent rate (Mbps) in 2 seconds intervals 
         *  3. Server will print the aggregated throughput (Mbps) over the 30 seconds
         */

        while (1) {
            // receive data from the client
            char buffer[1024];
            memset(buffer, 0, sizeof(buffer));
            ssize_t bytes_received = recv(client_socket, buffer, sizeof(buffer), 0);
            if (bytes_received == -1) {
                printf("Socket receiving failed...\n");
                exit(EXIT_FAILURE);
            }

            // check if the clint has disconnected
            if (strncmp(buffer, "exit", 4) == 0) {
                printf("[SERVER] Client %s:%d disconnected\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
                break;
            }
            
            // print the received data
            printf("[CLIENT]: %s\n", buffer);

            // reset & type a response
            memset(buffer, 0, sizeof(buffer));
            printf("[SERVER]: ");

            int n = 0;
            while ((buffer[n++] = getchar()) != '\n');

            ssize_t bytes_sent = send(client_socket, buffer, strlen(buffer), 0);
            if (bytes_sent == -1) {
                printf("Socket sending failed...\n");
                exit(EXIT_FAILURE);
            }
        }

        printf("[SERVER] Awaiting client connection...\n");
    }

    // close the sockets
    close(server_socket);
    printf("[SERVER] Server closed.\n");
    return 0;
}