# StegC-Crypt - Advanced Steganographic Encryption Tool

A powerful Python-based steganography tool that securely encrypts files and text into images using LSB (Least Significant Bit) technique combined with Fernet encryption.

## 🌟 Features

- 🔒 Secure file encryption into PNG images
- 📝 Direct text-to-image encryption
- 🎨 Custom image support for steganography
- 🔑 Automatic key management
- 🖼️ High-resolution output (1024x1024 minimum)
- 🛡️ Fernet symmetric encryption
- 📂 Original filename preservation
- 🔄 System reset capability

## 🚀 Installation Guide

### Prerequisites

1. Install pyenv (Python Version Manager)

   **Linux/macOS:**
   ```bash
   curl https://pyenv.run | bash
   ```

   Add to your shell configuration (~/.bashrc, ~/.zshrc, etc.):
   ```bash
   export PYENV_ROOT="$HOME/.pyenv"
   export PATH="$PYENV_ROOT/bin:$PATH"
   eval "$(pyenv init -)"
   eval "$(pyenv virtualenv-init -)"
   ```

   Restart your shell:
   ```bash
   exec "$SHELL"
   ```

2. Install Python 3.9+ using pyenv:
   ```bash
   pyenv install 3.9.0
   pyenv global 3.9.0
   ```

### Project Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/iksoft/stegc-crypt.git
   cd stegc-crypt
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   
   # On Linux/macOS:
   source venv/bin/activate
   
   # On Windows:
   .\venv\Scripts\activate
   ```

3. Install dependencies (one-line command):
   ```bash
   python -m pip install --upgrade pip && pip install Pillow>=10.0.0 numpy>=1.24.0 cryptography>=41.0.0
   ```

## 💻 Usage Guide

1. Run the program:
   ```bash
   python simple_encryptor.py
   ```

2. Choose from the following options:

   - **Encrypt a File:**
     1. Select option 1
     2. Enter the path to your file
     3. Choose whether to use a custom base image (y/n)
     4. If yes, provide the path to your custom image
     5. Save the encryption key displayed after successful encryption

   - **Encrypt Text:**
     1. Select option 2
     2. Enter your text
     3. Choose whether to use a custom base image (y/n)
     4. If yes, provide the path to your custom image
     5. Save the encryption key displayed after successful encryption

   - **Decrypt an Image:**
     1. Select option 3
     2. Enter the path to the encrypted image
     3. Enter the decryption key
     4. Find your decrypted file in the `decrypted_files` directory

   - **Reset System:**
     1. Select option 4
     2. Confirm reset (y/n)
     3. All encrypted and decrypted files will be removed

## 📁 Directory Structure

```
stegc-crypt/
├── simple_encryptor.py     # Main program
├── requirements.txt        # Dependencies
├── encrypted_files/        # Stores encrypted images
├── decrypted_files/       # Stores decrypted files
└── README.md              # Documentation
```

## 🔐 Security Notes

- Always keep your encryption keys safe
- Keys are automatically saved in `encrypted_files/keys.json`
- The security relies on keeping the encryption key private
- Encrypted data is hidden using LSB steganography
- Images appear as normal PNG files

## ⚠️ Important Notes

- Minimum image resolution is 1024x1024 pixels
- Supports any file type for encryption
- Output is always in PNG format to prevent data loss
- Custom base images will be resized to fit the required dimensions
- The program creates necessary directories automatically

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Created By

Iksoft Original - Advanced Steganographic Solutions 