#include <vector>
#include <string.h>
#include <iostream>

using namespace std;

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        cout << "Please provide the below two arguments" << endl;
        cout << "1. A key (a number between 0 to 25) for encryption" << endl;
        cout << "2. A plaintext string to encrypt" << endl;
        return -1;
    }

    int key = (int)*argv[1] - 48;

    if (!(key >= 0 && key <= 25))
    {
        cout << "Please provide a key value strictly between 0 to 25" << endl;
        return -1;
    }

    string plaintext = argv[2];
    string ciphertext = "";

    // validate that all characters are upper case letters
    for (int i = 0; i < plaintext.size(); i++)
    {
        if (!(plaintext[i] >= 'A' && plaintext[i] <= 'Z'))
        {
            cout << "Please provide plaintext with upper case characters only!" << endl;
            return -1;
        }
    }

    // run the encryption algorithm
    for (int i = 0; i < plaintext.size(); i++)
    {
        int e = (((int)plaintext[i] - 65) + key) % 26 + 65;
        ciphertext += (char)e;
    }

    cout << "Encrypted text is: " << ciphertext << endl;
}