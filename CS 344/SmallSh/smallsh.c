#define _POSIX_C_SOURCE 200809L
#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <err.h>
#include <errno.h>
#include <unistd.h>
#include <dirent.h>   // opendir
#include <ctype.h>
#include <string.h>
#include <assert.h>
#include <sys/wait.h>  //waitpid

#include <inttypes.h> // intmax_t/PRIdMAX

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#ifndef MAX_WORDS
#define MAX_WORDS 512
#endif


enum {
        ERR_INVAL_CMDLINE,
        ERR_CMD_NOTFOUND,
        ERR_NO_DIRECTORY,
        ERR_OPENFAIL_INFILE,
        ERR_OPENFAIL_OUTFILE,
        NUM_ERROR_CODES
};

void error_message(const char* str, int error_code) {
        //fprintf(stderr, "Error: %s\n", error_mesgs[error_code]);
        perror(str);
        errno = 0;
}
#define BUFSZ 200
#define MAX_BG 200


char* words[MAX_WORDS];
char* final_words[MAX_WORDS];
size_t wordsplit(char const *line);
char * expand(char const *word);


pid_t bg_threads[MAX_BG];
int max_bg;


pid_t ss_thrd;


int handle_redirects(int n_words);
void handle_bg_tasks();

void sigint_handler(int sig) { }

struct sigaction SIGINT_hdlr = {0};
struct sigaction SIGTSTP_hdlr = {0};

int main(int argc, char *argv[])
{
        FILE *input = stdin;
        char *input_fn = "(stdin)";
        if (argc == 2) {
                input_fn = argv[1];
                input = fopen(input_fn, "re");
                if (!input) err(1, "%s", input_fn);
        } else if (argc > 2) {
                errx(1, "too many arguments");
        }

        char *line = NULL;
        size_t n = 0;
        char empty[] = "";
        char* prompt = NULL;
        char buf[BUFSZ];


        //setup signal behavior
        struct sigaction SIGINT_old, SIGTSTP_old;
        struct sigaction SIGINT_IGN;

        SIGTSTP_hdlr.sa_handler = SIG_IGN;
        sigfillset(&SIGTSTP_hdlr.sa_mask);
        SIGTSTP_hdlr.sa_flags = 0;
        if (sigaction(SIGTSTP, &SIGTSTP_hdlr, &SIGTSTP_old)) {
                perror("sigaction");
        }

        // do nothing for SIGINT except...
        SIGINT_IGN.sa_handler = SIG_IGN;
        sigfillset(&SIGINT_IGN.sa_mask);
        SIGINT_IGN.sa_flags = 0;

        //during getline....
        SIGINT_hdlr.sa_handler = sigint_handler;
        sigfillset(&SIGINT_hdlr.sa_mask);
        SIGINT_hdlr.sa_flags = 0;

        if (sigaction(SIGINT, &SIGINT_IGN, &SIGINT_old)) {
                perror("sigaction");
        }

        ss_thrd = getpid();

        if (!(prompt = getenv("PS1"))) {
                prompt = empty;
        }
        if (setenv("$?", "0", 1)) {
                perror("Could not set $?");
        }

        for (;;) {
                fflush(NULL);
                fflush(input);
                errno = 0;
                //prompt:;
                /* TODO: Manage background processes */
                handle_bg_tasks();

                /* TODO: prompt */
                if (input == stdin) {

                        fprintf(stderr, "%s", prompt);

                }
                if (sigaction(SIGINT, &SIGINT_hdlr, NULL)) {
                        perror("sigaction");
                        exit(1);
                }
                ssize_t line_len = getline(&line, &n, input);
                if (errno) {
                        fputc('\n', stderr);
                        free(line);
                        line = NULL;
                        line_len = 0;
                        clearerr(input);  //why did this fix issue? thinking emoji
                        fflush(NULL);
                        fflush(input);
                        continue;
                }

                // EOF
                if (line_len < 0) {
                        return 0;
                }
                if (sigaction(SIGINT, &SIGINT_IGN, NULL)) {
                        perror("sigaction");
                        exit(1);
                }


                size_t nwords = wordsplit(line);
                if (!nwords) continue;

                for (size_t i = 0; i < nwords; ++i) {

                        //fprintf(stderr, "Word %zu: %s  -->  ", i, words[i]);
                        char *exp_word = expand(words[i]);
                        free(words[i]);
                        words[i] = exp_word;
                        //fprintf(stderr, "%s\n", words[i]);
                }
                words[nwords] = NULL;

                int is_bg = 0;
                if (!strcmp(words[nwords-1], "&")) {
                        is_bg = 1;
                        words[nwords-1] = NULL;
                        nwords--;
                }

                if (!strcmp(words[0], "exit")) {
                        if (nwords == 1) {
                                handle_bg_tasks();
                                return atoi(getenv("$?"));
                        }

                        errno = 0;
                        int exit_val;
                        char* endptr = NULL;
                        int base = 10;
                        if (nwords != 2) {
                                //error_message("", ERR_INVAL_CMDLINE);
                                continue;
                        }
                        exit_val = strtol(words[1], &endptr, base);
                        if (errno || endptr == words[1]) {
                                //error_message("", ERR_INVAL_CMDLINE);
                                continue;
                        }
                        handle_bg_tasks();
                        return exit_val;
                }
                if (!strcmp(words[0], "cd")) {
                        if (nwords > 2) {
                                error_message("cd", ERR_INVAL_CMDLINE);
                                continue;
                        }
                        char* path = getenv("HOME");

                        if (nwords == 2) {
                                path = words[1];
                        }
                        if (chdir(path)) {
                                error_message("cd", ERR_NO_DIRECTORY);
                        }
                        continue;
                }


                pid_t pid = fork();
                if (pid == 0) {

                        if (!(nwords = handle_redirects(nwords))) {
                                exit(1);
                                continue;
                        }
                        /*
                        for (int i=0; final_words[i]; i++) {
                                printf("'%s'\n", final_words[i]);
                        }
                        */
                        if (sigaction(SIGINT, &SIGINT_old, NULL)) {
                                //perror("sigaction");
                                exit(1);
                        }
                        if (sigaction(SIGTSTP, &SIGTSTP_old, NULL)) {
                                //perror("sigaction");
                                exit(1);
                        }


                        execvp(final_words[0], final_words);
                        error_message("execvp", ERR_CMD_NOTFOUND);
                        exit(0);
                } else if (pid > 0) {
                        int status, signum;

                        if (is_bg) {
                                //printf("background %d\n", pid);
                                // TODO reaping/reusing?
                                bg_threads[max_bg++] = pid;

                                snprintf(buf, BUFSZ, "%d", pid);
                                setenv("$!", buf, 1);

                        } else {
                                waitpid(pid, &status, 0);

                                // normal or signal exit
                                if (WIFSIGNALED(status)) {
                                        signum = WTERMSIG(status);
                                        //printf("%d %d %d\n", signum, SIGTSTP, SIGSTOP);
                                        // TODO is this 123? lol
                                        if (signum == SIGTSTP) {
                                                kill(pid, SIGCONT);
                                                fprintf(stderr, "Child process %jd stopped. Continuing.\n", pid);
                                                snprintf(buf, BUFSZ, "%d", pid);
                                                // save in bg array for reaping as a zombie later?
                                        } else {
                                                //printf("terminated by %d\n", signum);
                                                snprintf(buf, BUFSZ, "%d", signum+128);
                                        }
                                } else {
                                        snprintf(buf, BUFSZ, "%d", WEXITSTATUS(status));
                                }

                                setenv("$?", buf, 1);
                        }

                } else {
                        //perror("fork");
                        exit(1);
                }

        }

        // free all words
        for (int i=0; i<MAX_WORDS; i++) {
                free(words[i]);
        }

        return 0;
}

//this handles redirects, who would have thought?
int handle_redirects(int nwords)
{
        int fn_words = 0;
        final_words[0] = words[0];
        fn_words++;
        int fd;
        for (int i=1; i<nwords; i++) {
                if (!strcmp(words[i], "<")) {
                        if ((fd = open(words[i+1], O_RDONLY)) == -1) {
                                error_message("open", ERR_OPENFAIL_INFILE);
                                return 0;
                        }
                        if (dup2(fd, STDIN_FILENO) == -1) {
                                error_message("dup2", ERR_OPENFAIL_INFILE);
                                return 0;
                        }
                        close(fd);

                        i++;
                        // TODO?

                } else if (!strcmp(words[i], ">") || !strcmp(words[i], ">>")) {
                        int flags = O_CREAT | O_RDWR;

                        if (!words[i][1]) {
                                flags |= O_TRUNC;
                        } else {
                                flags |= O_APPEND;
                        }
                        // TODO use macro for mode?
                        if ((fd = open(words[i+1], flags, 0777)) == -1) {
                                error_message("open", ERR_OPENFAIL_OUTFILE);
                                return 0;
                        }
                        if (dup2(fd, STDOUT_FILENO) == -1) {
                                error_message("dup2", ERR_OPENFAIL_OUTFILE);
                                return 0;
                        }
                        close(fd);
                        i++; // skip over file
                } else {
                        final_words[fn_words++] = words[i];
                }
        }

        final_words[fn_words] = NULL;

        return fn_words;

}


/* Splits a string into words delimited by whitespace. Recognizes
 * comments as '#' at the beginning of a word, and backslash escapes.
 *
 * Returns number of words parsed, and updates the words[] array
 * with pointers to the words, each as an allocated string.
 */
size_t wordsplit(char const *line) {
        size_t wlen = 0;
        size_t wind = 0;

        char const *c = line;
        for (;*c && isspace(*c); ++c); /* discard leading space */

        for (; *c;) {
                if (wind == MAX_WORDS) break;
                /* read a word */
                if (*c == '#') break;
                for (;*c && !isspace(*c); ++c) {
                        if (*c == '\\') ++c;
                        void *tmp = realloc(words[wind], sizeof **words * (wlen + 2));
                        if (!tmp) err(1, "realloc");
                        words[wind] = tmp;
                        words[wind][wlen++] = *c; 
                        words[wind][wlen] = '\0';
                }
                ++wind;
                wlen = 0;
                for (;*c && isspace(*c); ++c);
        }
        return wind;
}


/* Find next instance of a parameter within a word. Sets
 * start and end pointers to the start and end of the parameter
 * token.
 */
char
param_scan(char const *word, char **start, char **end)
{
        static char *prev;
        if (!word) word = prev;

        char ret = 0;
        *start = NULL;
        *end = NULL;
        char *s;
        s = strchr(word, '$');
        while (s) {
                char *c = strchr("$!?", s[1]);
                if (c) {
                        ret = *c;
                        *start = s;
                        *end = s + 2;
                        break;
                } else if (s[1] == '{') {
                        char *e = strchr(s + 2, '}');
                        if (e) {
                                ret = '{';
                                *start = s;
                                *end = e + 1;
                        }
                        break;
                } else {
                        s = strchr(s+1, '$');
                }
        }
        prev = *end;
        return ret;
}

/* Simple string-builder function. Builds up a base
 * string by appending supplied strings/character ranges
 * to it.
 */
char *
build_str(char const *start, char const *end)
{
        static size_t base_len = 0;
        static char *base = 0;

        if (!start) {
                /* Reset; new base string, return old one */
                char *ret = base;
                base = NULL;
                base_len = 0;
                return ret;
        }
        /* Append [start, end) to base string 
         * If end is NULL, append whole start string to base string.
         * Returns a newly allocated string that the caller must free.
         */
        size_t n = end ? end - start : strlen(start);
        size_t newsize = sizeof *base *(base_len + n + 1);
        void *tmp = realloc(base, newsize);
        if (!tmp) err(1, "realloc");
        base = tmp;
        memcpy(base + base_len, start, n);
        base_len += n;
        base[base_len] = '\0';

        //printf("base = '%s'\n", base);
        return base;
}

/* Expands all instances of $! $$ $? and ${param} in a string 
 * Returns a newly allocated string that the caller must free
 */
char *
expand(char const *word)
{
        char buf[200];
        char const *pos = word;
        char *start, *end, *tmp_s;
        char c = param_scan(pos, &start, &end);
        build_str(NULL, NULL);
        build_str(pos, start);
        while (c) {
                //printf("%s\n", c);
                if (c == '!') {
                        tmp_s = getenv("$!");
                        snprintf(buf, 200, "%s", (!tmp_s) ? "" : tmp_s);
                        build_str(buf, NULL);
                } else if (c == '$') {
                        snprintf(buf, 200, "%jd", (intmax_t)ss_thrd);
                        build_str(buf, NULL);
                } else if (c == '?') {
                        tmp_s = getenv("$?");
                        snprintf(buf, 200, "%s", (!tmp_s) ? "" : tmp_s);
                        build_str(buf, NULL);

                } else if (c == '{') {
                        // TODO, but seems to be working
                        end[-1] = 0;
                        tmp_s = getenv(start+2);
                        snprintf(buf, 200, "%s", (!tmp_s) ? "" : tmp_s);
                        build_str(buf, NULL);
                }
                pos = end;
                c = param_scan(pos, &start, &end);
                build_str(pos, start);
        }
        return build_str(start, NULL);
}

void handle_bg_tasks()
{
        int status, signum;
        char buf[BUFSZ];

        // -1 if error
        pid_t bg_pid;
        int reap;
        while ((bg_pid = waitpid(-1, &status, WNOHANG)) > 0) {
                reap = 0;
                if (WIFEXITED(status)) {
                        fprintf(stderr, "Child process %d done. Exit status %d.\n", bg_pid, WEXITSTATUS(status));
                        fflush(NULL);
                        reap = 1;
                } else if (WIFSIGNALED(status)) {
                        // TODO or not TODO?
                        signum = WTERMSIG(status);
                        if (signum == SIGSTOP) {
                                kill(bg_pid, SIGCONT);
                                fprintf(stderr, "Child process %d stopped. Continuing.\n", bg_pid);
                                fflush(NULL);
                                snprintf(buf, BUFSZ, "%jd", bg_pid);
                                // save in bg array for reaping as a zombie later? idk...
                        } else {
                                fprintf(stderr, "Child process %jd done. Signaled %d.\n", bg_pid, WTERMSIG(status));
                                fflush(NULL);
                                reap = 1;
                        }
                }

                if (reap) {
                        for (int i=0; i<max_bg; i++) {
                                if (bg_threads[i] == bg_pid) {
                                        bg_threads[i] = 0;
                                        break;
                                }
                        }
                }
        }
        // no children exist, not really an "error" for us...
        if (errno == ECHILD) {
                errno = 0;
        }
}

