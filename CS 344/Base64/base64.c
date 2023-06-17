#include <stdio.h>  // Standard input and output
#include <errno.h>  // Access to errno and Exxx macros
#include <stdint.h> // Extra fixed-width data types
#include <string.h> // String utilities
#include <err.h>    // Convenience functions for error reporting (non-standard)

//Sterling Violette
//CS 344
//base64 Encoder

#define CUTTOFF_LENGTH 76 //constant max line

static char const b64_alphabet[] =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789"
    "+/";
static char const padding = '=';

int main(int argc, char *argv[])
{
    FILE *file = stdin;
    if (argc > 2)
    {
        fprintf(stderr, "Usage: %s [FILE]\n", argv[0]);
        errx(1, "Too many arguments");
    }
    else if (argc == 2 && strcmp(argv[1], "-"))
    {
        //there was a file, proceed to use it instead of stdin
        FILE *daFile = fopen(argv[1], "r");
        if (!daFile)
            err(1, "Unable to open and read file! %s", argv[1]);
        else
        {
            file = daFile;
        }
    }
    else
    {
        //there was no file, so read from stdin
        file = stdin;
    }
    uint32_t countOfDigits = 0; //should we use normal or precise 32 int?
    for (;;) //what an odd way to say for true...
    {
        uint8_t input_bytes[3] = {0};
        size_t n_read = fread(input_bytes, 1, 3, file);
        //need to add a line break if were at 76
        if (countOfDigits >0 && countOfDigits % CUTTOFF_LENGTH == 0 && n_read > 0)
        {
            putchar('\n');
        }
        //continue
        if (n_read != 0)
        {
            /* Have data */
            int alph_ind[4] = {0}; //should this be uint32_t?
            //use shifts...
            alph_ind[0] = (input_bytes[0] & 0xFC) >> 2;
            alph_ind[1] = ((input_bytes[0] & 0x03) << 4) | (((input_bytes[1] & 0xF0) >> 4) & 0x3Fu);
            alph_ind[2] = ((input_bytes[1] & 0x0F) << 2) | (((input_bytes[2] & 0xC0) >> 6) & 0x3Fu);
            alph_ind[3] = input_bytes[2] & 0x3Fu;
            char output[4] = {0};
            for (int index =0; index < 4; index++)
            {
                output[index] = b64_alphabet[alph_ind[index]];
            }
            //deal with padding using the '=' sign
            if (n_read < 3)
            {
                output[3] = padding;
                if (n_read < 2)
                {
                    output[2] =padding;
                }
            }
            size_t n_write = fwrite(output, 1, 4, stdout);
            countOfDigits += n_write;
            // this should be rare right?
            if (ferror(stdout))
                err(1,"There was an error writing to stdout! Could not write!");
        }
        if (n_read < 3)
        {
            /* Got less than expected */
            if (feof(file))
                break;
            if (ferror(file))
                err(1,"There was an error reading from file! Could not read!");
        }
    }
    //another line break...
    if (countOfDigits > 0)
        putchar('\n');
    if (file != stdin)
        fclose(file); /* close opened files; */
    return 0;
}
