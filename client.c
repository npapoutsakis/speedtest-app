/**
 *      SpeedTest with Unix Sockets
 *   Client - SpeedTest Implementation    
 *  
 *  @authors Nikolaos Papoutsakis 2019030206
 *           Christakis Argyris   2019030078 
 *           Sokratis Siganos     2019030097
 *           Syrianos Michael     2019030058
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

#define DEFAULT_IP "147.27.4.22"
#define PORT 5000
#define BUFFER_SIZE 128000 // 128 KB
#define TEST_DURATION 30
#define TIME_INTERVAL 2

int main(int argc, char *argv[]) {

    // create client socket
    int client_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (client_socket == -1) {
        printf("Socket creation failed...\n");
        exit(EXIT_FAILURE);
    }
    
    // set up the client address structure
    struct sockaddr_in client_address;
    
    memset(&client_address, 0, sizeof(client_address));
    client_address.sin_family = AF_INET;
    client_address.sin_addr.s_addr = inet_addr(argv[1]== NULL ? DEFAULT_IP : argv[1]);
    client_address.sin_port = htons(PORT);
    
    // attempt to connect to the server    
    if (connect(client_socket, (struct sockaddr *)&client_address, sizeof(client_address)) == -1) {
        printf("Connection to server failed...\n");
        exit(EXIT_FAILURE);
    }
    printf("[CLIENT] Connected to server at %s:%d\n", argv[1] == NULL ? DEFAULT_IP : argv[1] , PORT);    


    /*-------------------- SpeedTest --------------------*/
    printf("[CLIENT] Starting %d second speedtest...\n", TEST_DURATION);
    
    // speedtest variables
    char buffer[BUFFER_SIZE];
    memset(buffer, 0, BUFFER_SIZE);

    // data rate variables
    ssize_t bytes_sent;
    ssize_t total_bytes_sent = 0;
    ssize_t interval_bytes_sent = 0;

    // time variables
    time_t start_time = time(NULL);
    time_t previous_interval = time(NULL);
    time_t current_time;

    double time_passed;

    // main client loop
    while (1) {
        bytes_sent = send(client_socket, buffer, BUFFER_SIZE, 0);
        
        // get the current time and calculate the time passed from the start
        current_time = time(NULL);
        time_passed = difftime(current_time, start_time);

        // sum up the total bytes sent
        total_bytes_sent += bytes_sent;
        interval_bytes_sent += bytes_sent;

        double interval_time_passed = difftime(current_time, previous_interval);
        if (interval_time_passed >= TIME_INTERVAL) {
            // calculate the throughput for the last 2 seconds
            double data_rate = (interval_bytes_sent * 8.0)/(interval_time_passed * 1000000.0);
            printf("[CLIENT] Time Interval [%.1fs - %.1fs]: %.2f Mbps\n", difftime(previous_interval, start_time), time_passed, data_rate);
            
            // reset the bytes sent on the 2-second window
            interval_bytes_sent = 0;
            previous_interval = current_time;
        }

        if (time_passed >= TEST_DURATION) {
            break;
        }
    }

    // update the time
    current_time = time(NULL);
    time_passed = difftime(current_time, start_time);

    printf("\n[CLIENT] SpeedTest finished. Terminating connection...\n");
    close(client_socket);
    return 0;
}