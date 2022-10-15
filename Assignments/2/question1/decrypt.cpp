#include <vector>
#include <string.h>
#include <iostream>

using namespace std;

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        cout << "Please provide the below two arguments" << endl;
        cout << "1. A key (a number between 0 to 25) for decryption" << endl;
        cout << "2. A ciphertext string to decrypt" << endl;
        return -1;
    }

    int key = (int)*argv[1] - 48;

    if (!(key >= 0 && key <= 25))
    {
        cout << "Please provide a key value strictly between 0 to 25" << endl;
        return -1;
    }

    string ciphertext = argv[2];
    string plaintext = "";

    // validate that all characters are upper case letters
    for (int i = 0; i < ciphertext.size(); i++)
    {
        if (!(ciphertext[i] >= 'A' && ciphertext[i] <= 'Z'))
        {
            cout << "Please provide ciphertext with upper case characters only!" << endl;
            return -1;
        }
    }

    // run the encryption algorithm
    for (int i = 0; i < ciphertext.size(); i++)
    {
        int e = (26 + ((int)ciphertext[i] - 65) - key) % 26 + 65;
        plaintext += (char)e;
    }

    cout << "Decrypted text is: " << plaintext << endl;
}