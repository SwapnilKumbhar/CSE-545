#include <vector>
#include <unordered_map>
#include <queue>
#include <algorithm>
#include <string.h>
#include <iostream>

using namespace std;

string decrypt(string ciphertext, int key)
{
    string plaintext = "";

    for (int i = 0; i < ciphertext.size(); i++)
    {
        int e = (26 + ((int)ciphertext[i] - 65) - key) % 26 + 65;
        plaintext += (char)e;
    }

    return plaintext;
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        cout << "Please provide the below argument" << endl;
        cout << "A ciphertext string to decrypt" << endl;
        return -1;
    }

    string ciphertext = argv[1];
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

    unordered_map<int, int> ciphertext_count;
    unordered_map<int, double> ciphertext_frequencies;

    for (int i = 0; i < ciphertext.size(); i++)
    {
        ciphertext_count[(int)ciphertext[i] - 65] += 1;
    }

    for (auto i : ciphertext_count)
    {
        int key = i.first;
        int value = i.second;
        ciphertext_frequencies[key] = double(value) / ciphertext.size();
    }

    vector<double> character_frequencies = {.08, .015, .03, .04, 0.13, .02, .015, .06, .065, .005, .005, .035, .03, .07, .08, .02, .002, .065, .06, .09, .03, .01, .015, .005, .02, .002};
    vector<pair<int, double>> correlations_map;

    for (int i = 0; i < 26; i++)
    {
        double correlation = 0;
        for (auto j : ciphertext_frequencies)
        {
            int character_index = j.first;
            double frequency = j.second;
            int p_index = (26 + character_index - i) % 26;
            double p_frequency = character_frequencies[p_index];
            correlation += frequency * p_frequency;
        }
        correlations_map.push_back(make_pair(i, correlation));
    }

    sort(correlations_map.begin(), correlations_map.end(), [](pair<int, double> &a, pair<int, double> &b)
         { return a.second > b.second; });

    cout << "Possible plaintexts: " << endl;

    for (int i = 0; i < 6; i++)
    {
        int key = correlations_map[i].first;
        cout << "Key: " << key << ", Plaintext: " << decrypt(ciphertext, key) << endl;
    }
}