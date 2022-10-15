#include <iostream>
#include <string>

void
help()
{
  std::cout << "[!] USAGE: ./vigenere <KEY> <PLAINTEXT>" << std::endl;
  std::cout << "[!] The KEY must be uppercase and have length from 1 to 3!"
            << std::endl;
}

bool
containsLower(std::string& s)
{
  for (auto& c : s) {
    if (c > 'Z')
      return true;
  }
  return false;
}

void
printHex(std::string& s)
{
  for (auto& c : s) {
    printf("%02x", static_cast<unsigned char>(c));
  }
}

int
main(int argc, char** argv)
{
  if (argc < 3) {
    // Print help
    help();
    return -1;
  }

  std::string key = std::string(argv[1]);
  std::string plainText = std::string(argv[2]);

  if (containsLower(key)) {
    help();
    return -1;
  }

  if (key.length() > 3) {
    help();
    return -1;
  }

  // Encryption
  for (int i = 0; i < plainText.length(); i++) {
    char keyChar = key[i % key.length()];
    plainText[i] += keyChar;
  }

  std::cout << "Encrypted HEX output: ";
  printHex(plainText);
  std::cout << std::endl;
}
