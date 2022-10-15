#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

void
help()
{
  cout << "[!] USAGE: ./decipher <PLAINTEXT> <CIPHERTEXT>" << endl;
  cout << "[!] PLAINTEXT and CIPHERTEXT have to be UPPERCASE!" << endl;
}

bool
containsLower(string& s)
{
  for (auto& c : s) {
    if (c > 'Z')
      return true;
  }
  return false;
}

vector<string>
createKeySchedule()
{
  string charSet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  vector<string> singleKeys;

  // Start with 1 sized keys
  for (auto chr : charSet) {
    singleKeys.push_back(string(1, chr));
  }

  // Move on to two chars
  vector<string> doubleKeys;
  for (auto key : singleKeys) {
    for (auto chr : charSet) {
      doubleKeys.push_back(key + chr);
    }
  }

  // Move on to three chars
  vector<string> tripleKeys;
  for (auto key : doubleKeys) {
    for (auto chr : charSet) {
      tripleKeys.push_back(key + chr);
    }
  }

  // Combine all vectors
  singleKeys.insert(singleKeys.end(), doubleKeys.begin(), doubleKeys.end());
  singleKeys.insert(singleKeys.end(), tripleKeys.begin(), tripleKeys.end());

  return singleKeys;
}

string
vigEnc(string& pt, string& key)
{
  //
  string ct;
  for (int i = 0; i < pt.size(); i++) {
    char keyChar = key[i % key.size()] - 'A';
    char ptChar = pt[i] - 'A';
    char ctChar = (keyChar + ptChar) % 26;
    ctChar += 'A';
    ct.push_back(ctChar);
  }
  return ct;
}

int
main(int argc, char** argv)
{
  if (argc < 3) {
    help();
    return -1;
  }

  auto pt = string(argv[1]);
  auto ct = string(argv[2]);

  // Check if the inputs contain any uppercase characters
  if (containsLower(pt) || containsLower(ct)) {
    help();
    return -1;
  }

  // Generate keys
  auto keys = createKeySchedule();

  // Perform the exhaustive search.
  // Here, we are trying to check if cipher text generated with any key matches
  // our plaintext.
  ofstream outFile;
  cout << "[+] The program generated " << keys.size() << " keys!" << endl;
  cout << "[+] Saving output to `generated_keys.txt`." << endl;
  outFile.open("generated_keys.txt", ios::out);
  outFile << "--------------------------------------------" << endl;
  outFile << "Length of keys: " << keys.size() << endl;
  outFile << "Here's the list of generated keys: " << endl;
  outFile << "--------------------------------------------" << endl;
  for (auto key : keys) {
    string ctEnc = vigEnc(pt, key);
    if (ctEnc == ct) {
      cout << "[+] For the given inputs, the key is: " << key << endl;
    }
    outFile << key << endl;
  }

  outFile.close();
  cout << "[+] Done!" << endl;
}
