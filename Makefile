all: server client

server: server.c
	gcc -o server server.c -lpthread

client: client.c
	gcc -o client client.c -lpthread
	@echo "Client and server compiled successfully."

clean:
	rm -f client server
	