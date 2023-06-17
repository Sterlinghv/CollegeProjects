
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>


#define BUF_SZ 1001
#define MAX_LINES 50

char buf1[MAX_LINES][BUF_SZ];
char buf2[MAX_LINES][BUF_SZ];
char buf3[MAX_LINES][BUF_SZ];


// input to nl, new line
int prod1;
int con1;

// nl to plus
int prod2;
int con2;

// plus to output
int prod3;
int con3;


// Initialize the mutex for transformations input -> nl
pthread_mutex_t mutex_nl = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t full_nl = PTHREAD_COND_INITIALIZER;

// nl to plus thread
pthread_mutex_t mutex_plus = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t full_plus = PTHREAD_COND_INITIALIZER;

// plus to output thread
pthread_mutex_t mutex_out = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t out_ready = PTHREAD_COND_INITIALIZER;

void* get_input(void* data)
{
	char buf[BUF_SZ];
	char* line;
	while (1) {
		line = fgets(buf, BUF_SZ, stdin);

		if (!line) break;

		//printf("%s", line);
		pthread_mutex_lock(&mutex_nl);

		strcpy(buf1[prod1], buf);
		prod1++;

		//signal to the consumer that the buffer is no longer empty
		pthread_cond_signal(&full_nl);

		//unlock the mutex
		pthread_mutex_unlock(&mutex_nl);

		if (!strcmp(line, "STOP\n")) {
			break;
		}
	}

	return NULL;
}


void* replace_nl(void* data)
{
	char* line;
	while (1) {
		pthread_mutex_lock(&mutex_nl);
		while (con1 >= prod1) {
			pthread_cond_wait(&full_nl, &mutex_nl);
		}

		line = buf1[con1];

		line[strlen(line)-1] = ' ';
		con1++;

		pthread_mutex_lock(&mutex_plus);

		strcpy(buf2[prod2], line);
		prod2++;

		pthread_cond_signal(&full_plus);
		pthread_mutex_unlock(&mutex_plus);

		// TODO could move up after con++, or not?
		pthread_mutex_unlock(&mutex_nl);

		if (!strcmp(line, "STOP ")) {
			break;
		}
	}

	return NULL;
}

/*
"a++bc"
i == 1
5-1-1 // would be 5-i-2 except i want the null terminator to shift over too...
*/
void* plus_sign_func(void* data)
{
	char* line;
	while (1) {
		pthread_mutex_lock(&mutex_plus);
		while (con2 >= prod2) {
			pthread_cond_wait(&full_plus, &mutex_plus);
		}

		line = buf2[con2];

		char* c = strstr(line, "++");
		int i;
		int len = strlen(line);
		while (c) {
			i = c - line;
			c[0] = '^';

			memmove(&c[1], &c[2], len-i-1);
			c = strstr(c, "++");
			len--;
		}

		con2++;

		pthread_mutex_lock(&mutex_out);
		strcpy(buf3[prod3], line);
		prod3++;

		pthread_cond_signal(&out_ready);
		pthread_mutex_unlock(&mutex_out);

		// TODO to more up or not to move up?
		pthread_mutex_unlock(&mutex_plus);


		if (!strcmp(line, "STOP ")) {
			break;
		}
	}
	return NULL;
}

void* output_func(void* data)
{
	//something do be wrong here with the not
	//calling to write test, I think it would involve
	//major refactoring, which at this point, I 
	// dont want to do... 
	int pos = 0;
	char output_buf[100];
	char* line;
	int exit = 0;
	while (1) {
		pthread_mutex_lock(&mutex_out);
		while (con3 >= prod3) {
			pthread_cond_wait(&out_ready, &mutex_out);
		}
		pthread_mutex_unlock(&mutex_out);

		// Can this even happen?
		while (con3 < prod3) {
			line = buf3[con3];
			if (!strcmp(line, "STOP ")) {
				exit = 1;
				break;
			}

			for (int i=0; line[i]; i++) {
				if (pos == 80) {
					//output_buf[pos] = '\n';
					//write(STDOUT_FILENO, output_buf, 81); why.......
					printf("%s\n", output_buf);
                    fflush(stdout);
					//putchar('\n');
					pos = 0;
				}
				output_buf[pos++] = line[i];
				//putchar(line[i]);
			}
			con3++;
		}
		//pthread_mutex_unlock(&mutex_out);
		if (exit) {
			break;
		}
	}

	return NULL; //is this right? seems to be working...
}

int main()
{

//what a stupid test string
/*
abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz
*/

	pthread_t input_t, line_sep_t, plus_sign_t, output_t;
	//create da threads
	pthread_create(&input_t, NULL, get_input, NULL);
	pthread_create(&line_sep_t, NULL, replace_nl, NULL);
	pthread_create(&plus_sign_t, NULL, plus_sign_func, NULL);
	pthread_create(&output_t, NULL, output_func, NULL);

	//wait for the threads to terminate..
	pthread_join(input_t, NULL);
	pthread_join(line_sep_t, NULL);
	pthread_join(plus_sign_t, NULL);
	pthread_join(output_t, NULL);

	return 0;
}
