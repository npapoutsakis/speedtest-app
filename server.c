/**
 *  Server - SpeedTest Implementation
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <time.h>

// Ref: Beej’s Guide to Network Programming (pg 12) --> see available ports: cat /etc/services
#define PORT 5000
#define TEST_DURATION 30
#define TIME_INTERVAL 2
#define BUFFER_SIZE 128000 //(128 KB -> used in iperf)

int main(int argc, char *argv[]) {
    
    /**
     *  References: 
     *      1. https://www.tutorialspoint.com/unix_sockets/socket_quick_guide.htm
     *      2. https://www.geeksforgeeks.org/tcp-server-client-implementation-in-c/
     *      3. Beej’s Guide to Network Programming
     */
    
    // create the socket, stream socket because we are using TCP
    int server_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (server_socket == -1) {
        printf("Socket creation failed...\n"); 
        exit(EXIT_FAILURE);
    }
    
    // set up the server address structure
    struct sockaddr_in server_address;
    
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);
    server_address.sin_port = htons(PORT);

    // bind the socket to the address and port
    if (bind(server_socket, (struct sockaddr *)&server_address, sizeof(server_address)) == -1) {
        printf("Socket binding failed...\n");
        exit(EXIT_FAILURE);
    }

    // listen for incoming connections, 1 is the maximum number of queued connections
    if (listen(server_socket, 1) == -1) {
        printf("Socket listening failed...\n");
        exit(EXIT_FAILURE);
    }
    
    printf("[SERVER] Server listening on port %d\n", PORT);

    
    // main server loop
    while (1) {
        
        printf("[SERVER] Awaiting client connection...\n");

        struct sockaddr_in client_address;
        socklen_t client_addr_len = sizeof(client_address);

        // accept a connection from a client - code blocks until a client connects
        int client_socket = accept(server_socket, (struct sockaddr *)&client_address, &client_addr_len);
        if (client_socket == -1) {
            printf("Socket accepting failed...\n");
            exit(EXIT_FAILURE);
        }
        printf("[SERVER] Client %s:%d connected\n", inet_ntoa(client_address.sin_addr), ntohs(client_address.sin_port));


        /*-------------------- SpeedTest --------------------*/
        printf("\n[SERVER] Starting %d second downlink throughput test...\n", TEST_DURATION);

        // SpeedTest variables
        char buffer[BUFFER_SIZE];
        
        // data rate variables
        ssize_t bytes_received;
        double total_bytes_received = 0;
        double interval_bytes_received = 0;
        
        // time variables
        time_t start_time = time(NULL);
        time_t previous_interval = time(NULL);
        time_t current_time;
        
        double time_passed;
        double aggregated_throughput;

        // speedtest loop
        while (1) {

            // receive data from the client
            bytes_received = recv(client_socket, buffer, BUFFER_SIZE, 0);

            // get the current time and calculate the time passed from the start
            current_time = time(NULL);
            time_passed = difftime(current_time, start_time);

            // sum up the total bytes received
            total_bytes_received += bytes_received;
            interval_bytes_received += bytes_received;
            
            // calculate the 2 second interval
            double current_time_interval = difftime(current_time, previous_interval);
            if (current_time_interval >= TIME_INTERVAL) {
                // *8 to convert to bits & /1000000 to convert to Mbits
                double data_rate = (interval_bytes_received * 8.0)/(current_time_interval * 1000000.0);
                printf("[SERVER] Time Interval [%.1fs - %.1fs]: %.2f Mbps\n", difftime(previous_interval, start_time), time_passed, data_rate);
                
                // reset the bytes on the 2-second window
                interval_bytes_received = 0;
                previous_interval = current_time;
            }

            // break condition: check test duration
            if (time_passed >= TEST_DURATION) {
                break;
            }
        }

        // update the current time
        current_time = time(NULL);
        time_passed = difftime(current_time, start_time);
        aggregated_throughput = (total_bytes_received * 8.0)/(time_passed * 1000000.0);
        
        printf("[SERVER] Aggregated throughput: %.2f Mbps\n", aggregated_throughput);
        printf("[SERVER] Connection closed.\n");
        close(client_socket);
    }

    close(server_socket);
    return 0;
}