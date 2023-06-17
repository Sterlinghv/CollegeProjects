#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static char s[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ";

//what can i say, its a keygen!
int main(int argc, char** argv)
{
	if (argc != 2) {
		printf("Usage: %s keylen\n", argv[0]);
		return 0;
	}

	int keylen = atoi(argv[1]);
	if (keylen < 1) {
		fprintf(stderr, "Invalid key length\n");
		return 0;
	}

	srand(time(NULL));
	int c;
	for (int i=0; i<keylen; i++) {
		c = rand() % 27;
		putchar(s[c]);
	}
	putchar('\n');
}
