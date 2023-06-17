#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

#define MAGIC_ENC_ID 200

int file_read(FILE* file, char** out)
{
	fseek(file, 0, SEEK_END);
	int size = ftell(file);
	if (size <= 0) {
		if (size == -1)
			perror("ftell failure");
		fclose(file);
		return 0;
	}

	char* data = (char*)malloc(size+1);
	if (!data) {
		perror("allocation failure");
		fclose(file);
		return 0;
	}

	rewind(file);
	if (!fread(data, size, 1, file)) {
		perror("fread failure");
		fclose(file);
		free(data);
		return 0;
	}

	if (data[size-1] == '\n') {
		size--;
	}
	data[size] = 0; /* null terminate in all cases even if reading binary data */

	*out = data;
	return size;
}

void validate_files(char* plain, char* keyfile, char** pt_out, char** key_out, int* p_sz, int* k_sz);

int safe_recv(int sockfd, char* buf, int sz, int flags)
{
	int n, bytes_read = 0;
	do {
		n = recv(sockfd, &buf[bytes_read], sz-bytes_read, flags);
		if (n < 0) {
			perror("recv error");
			return 0;
		}
		bytes_read += n;
	} while (bytes_read != sz);
	//fprintf(stderr, "enc_client received %d bytes\n", sz);
	return 1;
}


int main(int argc, char **argv)
{
	int sockfd, port, n;
	struct sockaddr_in serv_addr;
	struct hostent *server;

	if (argc != 4) {
		printf("usage: %s plaintextfile keyfile port_number\n", argv[0]);
		return 0;
	}

	
	int p_sz=0, k_sz=0;
	char* plaintext, *key;
	validate_files(argv[1], argv[2], &plaintext, &key, &p_sz, &k_sz);



	port = atoi(argv[3]);

	//create socket
	//it take three arguments - address domain, type of socket, protocol
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd < 0) {
		perror("ERROR opening socket");
		return 0;
	}

	//funcion gethostbyname() takes name as an argument and returns a pointer to a hostent containing information about that host
	//name is taken as an argument from the user
	server = gethostbyname("localhost");

	//If hostent structure is NULL (after the above assignment), the system could not locate a host with this name
	if (!server) {
		fprintf(stderr, "ERROR, no such host\n");
		exit(0);
	}

	memset(&serv_addr, 0, sizeof(serv_addr));

	//following code sets the fields in serv_addr
	//contains a code for the address family
	serv_addr.sin_family = AF_INET;

  // Copy the first IP address from the DNS entry to sin_addr.s_addr
	memcpy((char*) &serv_addr.sin_addr.s_addr, 
	       server->h_addr_list[0],
	       server->h_length);

	//contain the port number
	serv_addr.sin_port = htons(port);

	if (connect(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
		perror("ERROR connecting");
		return 0;
	}
	
	//puts("Connected to server!");

	unsigned char id = MAGIC_ENC_ID;

	n = send(sockfd, &id, 1, 0);
	if (n < 0) {
		 perror("ERROR writing to socket");
		 return 0;
	}

	char is_good = 0;
	recv(sockfd, &is_good, 1, 0);
	if (!is_good) {
		fprintf(stderr, "enc_client cannot use dec_server\n");
		return 2;
	}

	// TODO check for errors?
	send(sockfd, &p_sz, 4, 0);
	send(sockfd, plaintext, p_sz+1, 0);

	send(sockfd, &k_sz, 4, 0);
	send(sockfd, key, k_sz+1, 0);

	//both the server can read and write after a connection has been established.
	
	char* ciphertext = plaintext; // reuse buffer with new name

	safe_recv(sockfd, ciphertext, p_sz+1, 0);

	printf("%s\n", ciphertext);

	fsync(sockfd);
	//close connections using file descriptors
	close(sockfd);

	return 0;
}

//still seems bad?
void validate_files(char* plain, char* keyfile, char** pt_out, char** key_out, int* p_sz, int* k_sz)
{
	const char* error_strs[] =
	{
		"Key length is less than plaintext length\n",
		"plaintext contains invalid characters\n",
		"key contains invalid characters\n",
	};
	int err;
	FILE* pfile = fopen(plain, "r");
	if (!pfile) {
		perror("Error opening plaintext file");
		exit(0);
	}

	char* plaintext = NULL;
	int pt_sz = file_read(pfile, &plaintext);
	if (!pt_sz) {
		exit(0);
	}

	fclose(pfile);

	FILE* kfile = fopen(keyfile, "r");
	if (!kfile) {
		perror("Error opening key file");
		exit(0);
	}

	char* key = NULL;
	int key_sz = file_read(pfile, &key);
	if (!key_sz) {
		exit(0);
	}

	fclose(kfile);

	int i;
	for (i=0; i<key_sz; i++) {
		if (!isupper(key[i]) && key[i] != ' ') {
			err = 2;
			goto invalid_input;
		}
	}

	for (i=0; i<pt_sz; i++) {
		if (!isupper(plaintext[i]) && plaintext[i] != ' ') {
			err = 1;
			goto invalid_input;
		}
	}

	if (key_sz < pt_sz) {
		err = 0;
		goto invalid_input;
	}

	*key_out = key;
	*pt_out = plaintext;

	*k_sz = key_sz;
	*p_sz = pt_sz;

	return;

invalid_input:
	fprintf(stderr, "%s", error_strs[err]);
	exit(1);
}
