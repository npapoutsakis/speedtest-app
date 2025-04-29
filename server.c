/**
 *  Server
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>

// see available ports: cat /etc/services
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

    // listen for incoming connections
    if (listen(server_socket, 5) == -1) {
        printf("Socket listening failed...\n");
        exit(EXIT_FAILURE);
    }






    return 0;
}