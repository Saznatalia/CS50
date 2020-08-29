#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

bool jpeg_beginning(unsigned char *block);


int main(int argc, char *argv[])
{
    //remember file name
    char *infile = argv[1];
    unsigned char *block = malloc(sizeof(unsigned char) * 512);
    char filename[8];

    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    //iterate over 512 byte blocks untill the EOF
    int count = 0;
    sprintf(filename, "%03i.jpg", count);// create a new jpeg file
    FILE *img;
    img = fopen(filename, "w");// open jpeg file for writing
    while (fread(block, 1, 512, inptr) == 512)
    {
        if (jpeg_beginning(block) == true)// if beginning of jpeg
        {
            if (count == 0)
            {
                fwrite(block, 1, 512, img); //write 512 bytes into jpeg file

                count += 1;
            }

            else
            {
                fclose(img); // close old image file

                sprintf(filename, "%03i.jpg", count);// create a new jpeg file

                img = fopen(filename, "w");// open jpeg file

                fwrite(block, 1, 512, img); //write 512 bytes into jpeg file

                count += 1;
            }
        }

        else
        {
            if (count != 0)// write 512 bytes into open existing jpeg
            {
                fwrite(block, 1, 512, img);
            }
        }
    }

    //printf("%i\n", count);

    //free the memory
    free(block);

    // close infile
    fclose(inptr);

    // close outfile
    fclose(img);

    // success
    return 0;

}

// checks if the beginning of jpeg image
bool jpeg_beginning(unsigned char *block)
{
    return (block[0] == 0xff &
            block[1] == 0xd8 &
            block[2] == 0xff &
            (block[3] & 0xf0) == 0xe0);
}



