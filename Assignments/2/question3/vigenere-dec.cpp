#include <iostream>
#include <ostream>
#include <stdexcept>
#include <string>

void
help()
{
  std::cout << "[!] USAGE: ./vigenere-dec <KEY> <HEX_CIPHERTEXT>" << std::endl;
  std::cout << "[!] KEY has to be from length 1 to 3 and uppercase"
            << std::endl;
  std::cout << "[!] HEX_CIPHERTEXT has to be valid hex." << std::endl;
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

bool
convertHexToStr(std::string& s, std::string& ct)
{
  //
  for (int i = 0; i < s.length(); i += 2) {
    auto num = s.substr(i, 2);
    try {
      auto chr = std::stoul(num, 0, 16);
      ct.push_back(chr);
    } catch (std::invalid_argument) {
      return false;
    } catch (std::out_of_range) {
      return false;
    }
  }
  return true;
}

int
main(int argc, char** argv)
{
  //
  if (argc < 3) {
    help();
    return -1;
  }

  auto key = std::string(argv[1]);
  auto cipherText = std::string(argv[2]);

  if (containsLower(key)) {
    help();
    return -1;
  }

  // Ciphertext after it is converted from hex to characters
  std::string ct_conv;

  if (!convertHexToStr(cipherText, ct_conv)) {
    help();
    return -1;
  }

  // Decryption
  std::string plainText;
  for (int i = 0; i < ct_conv.length(); i++) {
    //
    char keyChar = key[i % key.length()];
    plainText.push_back(ct_conv[i] - keyChar);
  }

  std::cout << "Decrypted output: " << plainText << std::endl;
}
