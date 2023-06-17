#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>

#define NUM_THREADS 8
#define MAGIC_DEC_ID 201
#define BUF_SZ 2048

const char mapping[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ";

typedef struct thrd_data
{
	int sockfd;
	int tid;
} thrd_data;

void* process_request(void* data);


int main(int argc, char** argv)
{
	int sockfd, port;

	if (argc != 2) {
		printf("Usage: %s port\n", argv[0]);
		return 0;
	}

	port = atoi(argv[1]);
	// TODO
	if (port < 1024) {
		fprintf(stderr, "Invalid port\n");
		return 0;
	}

	//create socket
	//it take three arguments - address domain, type of socket, protocol
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd < 0) {
		perror("ERROR opening socket");
		return 0;
	}

	struct sockaddr_in serv_addr;
	//set server address filename with zeros with memset
	memset(&serv_addr, 0, sizeof(serv_addr));

	port = atoi(argv[1]);

	//contains a code for the address family
	serv_addr.sin_family = AF_INET;

	//contains the IP address of the host
	serv_addr.sin_addr.s_addr = INADDR_ANY;

	//contain the port number
	serv_addr.sin_port = htons(port);
	//seems bad but works 
	if (bind(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
		perror("ERROR on binding");
		return 0;
	}

	//listen system call allows the process to listen on the socket for connections.
	// takes socket file descriptor, and max length of queue of pending connections
	// no threads for now
	listen(sockfd, NUM_THREADS);

	pthread_t threads[NUM_THREADS];
	thrd_data tdata[NUM_THREADS];
	for (int i=0; i<NUM_THREADS; i++) {
		tdata[i].sockfd = sockfd;
		tdata[i].tid = i;
		if (pthread_create(&threads[i], NULL, process_request, &tdata[i])) {
			perror("couldn't create thread");
			//return 0; ?
		}
	}

	for (int i=0; i<NUM_THREADS; i++)
		pthread_join(threads[i], NULL);

	close(sockfd);


	return 0;
}

void* process_request(void* data)
{
	thrd_data* tdata = (thrd_data*)data;
	int sockfd = tdata->sockfd;
	int tid = tdata->tid;

	struct sockaddr_in cli_addr;
	int bytes_read, n;
	int newsockfd, port;
	socklen_t clilen;


	clilen = sizeof(cli_addr);

	// TODO errors?
	char* buf = malloc(BUF_SZ);
	char* keybuf = malloc(BUF_SZ);

	// int32_t technically ...
	int pt_sz, k_sz;



	unsigned char magic = 0;

	while (1) {
		//accept() system call causes the process to block until a client connects to the server.
		newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
		if (newsockfd < 0) {
			perror("ERROR on accept");
			return NULL;
			//continue;
		}

		//printf("Handling new connection on thread %d\n", tid);

		//After a connection a client has successfully connected to the server

		bytes_read = recv(newsockfd, &magic, 1, 0);
		if (magic != MAGIC_DEC_ID) {
			magic = 0;
			send(newsockfd, &magic, 1, 0);
			fprintf(stderr, "only dec_client connections accepted\n");
			goto close_sock;
		}
		// as long as the correct magic number is non-zero ie true to send back
		send(newsockfd, &magic, 1, 0);

		pt_sz = 0;
		bytes_read = recv(newsockfd, &pt_sz, 4, 0);
		if (!pt_sz) {
			// error
			goto close_sock;
		}

		char* tmp = realloc(buf, pt_sz+1);
		if (!tmp) {
			perror("Allocation failure");
			goto close_sock;
		}
		buf = tmp;

		bytes_read = 0;
		while (bytes_read != pt_sz+1) {
			n = recv(newsockfd, &buf[bytes_read], pt_sz+1-bytes_read, 0); // +1 or not for null termiator
			//printf("Didn't read whole ciphertext in one\n");
			if (n < 0) {
				perror("Failed to read socket");
				goto close_sock;
			}
			bytes_read += n;
		}

		k_sz = 0;
		bytes_read = recv(newsockfd, &k_sz, 4, 0);
		if (!k_sz) {
			// error
			goto close_sock;
		}

		tmp = realloc(keybuf, k_sz+1);
		if (!tmp) {
			perror("Allocation failure");
			goto close_sock;
		}
		keybuf = tmp;

		bytes_read = recv(newsockfd, keybuf, k_sz+1, 0); // +1 or not for null termiator
		if (bytes_read != k_sz+1) {
			printf("Didn't read whole ciphertext in one\n");
			// error
		}
		//printf("%s\n", keybuf);

		// do decryption
		int a, b, dif;
		for (int i=0; i<pt_sz; i++) {
			a = (buf[i] != ' ') ? buf[i] - 'A' : 26;
			b = (keybuf[i] != ' ') ? keybuf[i] - 'A' : 26;
			dif = a - b;
			if (dif < 0) dif += 27;
			
			buf[i] = mapping[dif];
		}


		
		n = send(newsockfd, buf, pt_sz+1, 0);
		//fprintf(stderr, "%d %d\n", n, pt_sz+1);

		
		fsync(newsockfd);

close_sock:
		//close connections using file descriptors
		close(newsockfd);

		//printf("[Server] Connection with Client closed. thread %d will wait now...\n", tid);
	}
}






