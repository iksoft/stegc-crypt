from PIL import Image
import numpy as np
from cryptography.fernet import Fernet
import os
import base64
import sys
import math
import time
from datetime import datetime
import json
import shutil

# ANSI Color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'

def print_banner():
    """Print a professional banner for the application"""
    os.system('clear' if os.name == 'posix' else 'cls')
    banner = f"""{Colors.CYAN}
╔════════════════════════════════════════════════════════════════╗
║ {Colors.WARNING}███████╗████████╗███████╗ ██████╗  ██████╗{Colors.CYAN}               ║
║ {Colors.WARNING}██╔════╝╚══██╔══╝██╔════╝██╔════╝ ██╔════╝{Colors.CYAN}               ║
║ {Colors.WARNING}███████╗   ██║   █████╗  ██║  ███╗██║{Colors.CYAN}                    ║
║ {Colors.WARNING}╚════██║   ██║   ██╔══╝  ██║   ██║██║{Colors.CYAN}                    ║
║ {Colors.WARNING}███████║   ██║   ███████╗╚██████╔╝╚██████╗{Colors.CYAN}               ║
║ {Colors.WARNING}╚══════╝   ╚═╝   ╚══════╝ ╚═════╝  ╚═════╝{Colors.CYAN}               ║
║ {Colors.WARNING} ██████╗██████╗ ██╗   ██╗██████╗ ████████╗{Colors.CYAN}               ║
║ {Colors.WARNING}██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝{Colors.CYAN}               ║
║ {Colors.WARNING}██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║{Colors.CYAN}                  ║
║ {Colors.WARNING}██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║{Colors.CYAN}                  ║
║ {Colors.WARNING}╚██████╗██║  ██║   ██║   ██║        ██║{Colors.CYAN}                  ║
║ {Colors.WARNING} ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝{Colors.CYAN}                  ║
║ {Colors.GREEN}[ Advanced Steganographic Encryption Tool v2.1 ]{Colors.CYAN}            ║
║ {Colors.BLUE}[ Created by: Iksoft Original ]{Colors.CYAN}                             ║
║ {Colors.BLUE}[ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ]{Colors.CYAN} • {Colors.WARNING}[ 🔒 LSB Encryption ]{Colors.CYAN}  ║
╚════════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    print(banner)

def print_status(message, status_type="info"):
    """Print a formatted status message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    if status_type == "info":
        print(f"{Colors.BLUE}[{timestamp}] ℹ️  {message}{Colors.ENDC}")
    elif status_type == "success":
        print(f"{Colors.GREEN}[{timestamp}] ✓ {message}{Colors.ENDC}")
    elif status_type == "warning":
        print(f"{Colors.WARNING}[{timestamp}] ⚠️  {message}{Colors.ENDC}")
    elif status_type == "error":
        print(f"{Colors.FAIL}[{timestamp}] ❌ {message}{Colors.ENDC}")
    elif status_type == "processing":
        print(f"{Colors.CYAN}[{timestamp}] 🔄 {message}{Colors.ENDC}")

def print_progress_bar(progress, total, prefix='', suffix=''):
    """Print a progress bar"""
    percent = 100 * (progress / float(total))
    bar_length = 50
    filled_length = int(bar_length * progress // total)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    print(f'\r{Colors.BLUE}{prefix} |{Colors.GREEN}{bar}{Colors.BLUE}| {percent:.1f}% {suffix}', end='\r')
    if progress == total:
        print()

def get_file_info(file_path):
    """Get detailed file information"""
    stats = os.stat(file_path)
    size = stats.st_size
    created = datetime.fromtimestamp(stats.st_ctime)
    modified = datetime.fromtimestamp(stats.st_mtime)
    
    size_str = f"{size:,} bytes"
    if size > 1024:
        size_str += f" ({size/1024:.2f} KB)"
    if size > 1024*1024:
        size_str += f" ({size/(1024*1024):.2f} MB)"
    
    return {
        'size': size_str,
        'created': created.strftime("%Y-%m-%d %H:%M:%S"),
        'modified': modified.strftime("%Y-%m-%d %H:%M:%S")
    }

def get_square_dimensions(data_size):
    """Calculate square dimensions that can hold the data with good resolution"""
    # Each pixel can store 3 bits (RGB channels)
    total_pixels_needed = math.ceil(data_size / 3)
    
    # Set minimum dimensions for good quality (1024x1024)
    MIN_SIZE = 1024
    
    # Calculate base square size
    base_size = math.ceil(math.sqrt(total_pixels_needed))
    
    # Ensure minimum size and make it even for better compression
    square_size = max(base_size, MIN_SIZE)
    square_size = square_size + (square_size % 2)  # Make it even
    
    return square_size, square_size

def encrypt_file_to_image(input_file, output_image=None, key=None, custom_image=None):
    """Encrypt a file into an image"""
    try:
        print_status("Starting encryption process", "processing")
        print_status(f"Target file: {input_file}", "info")
        
        # Get file information
        file_info = get_file_info(input_file)
        print(f"\n{Colors.CYAN}File Information:{Colors.ENDC}")
        print(f"{Colors.BLUE}├─ Size: {file_info['size']}")
        print(f"├─ Created: {file_info['created']}")
        print(f"└─ Modified: {file_info['modified']}{Colors.ENDC}\n")
        
        # Set default output path
        if output_image is None:
            os.makedirs("encrypted_files", exist_ok=True)
            output_image = os.path.join("encrypted_files", 
                                      os.path.splitext(os.path.basename(input_file))[0] + ".png")
        
        print_status(f"Output destination: {output_image}", "info")
        
        # Generate or use encryption key
        if key is None:
            key = Fernet.generate_key()
            print_status(f"Generated encryption key: {key.decode()}", "info")
        cipher_suite = Fernet(key)
        
        # Read and encrypt file with progress bar
        print_status("Reading and encrypting file", "processing")
        with open(input_file, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(input_file)
            print_progress_bar(0, 2, prefix='Progress:', suffix='Preparing data')
            time.sleep(0.2)  # For visual effect
            data = f"{file_name}|||{base64.b64encode(file_data).decode()}"
            print_progress_bar(1, 2, prefix='Progress:', suffix='Encrypting')
            time.sleep(0.2)  # For visual effect
            encrypted_data = cipher_suite.encrypt(data.encode())
            print_progress_bar(2, 2, prefix='Progress:', suffix='Complete')
        
        # Convert to binary and show stats
        binary_data = ''.join(format(byte, '08b') for byte in encrypted_data)
        data_len = len(binary_data)
        
        print(f"\n{Colors.CYAN}Encryption Statistics:{Colors.ENDC}")
        print(f"{Colors.BLUE}├─ Original size: {len(file_data):,} bytes")
        print(f"├─ Encrypted size: {len(encrypted_data):,} bytes")
        print(f"└─ Binary length: {data_len:,} bits{Colors.ENDC}\n")
        
        # Calculate dimensions
        width, height = get_square_dimensions(data_len)
        print_status(f"Creating {width}x{height} pixel image", "processing")
        
        # Process image
        if custom_image:
            try:
                base_img = Image.open(custom_image)
                base_img = base_img.resize((width, height))
                img_array = np.array(base_img)
                print_status("Custom image loaded and resized", "success")
            except Exception as e:
                print_status(f"Failed to load custom image: {str(e)}", "error")
                raise
        else:
            img_array = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
        
        # Embed data with progress bar
        total_pixels = height * width * 3
        print_status("Embedding encrypted data", "processing")
        binary_idx = 0
        progress_step = total_pixels // 100
        
        for i in range(height):
            for j in range(width):
                for k in range(3):
                    if binary_idx < data_len:
                        img_array[i, j, k] = (img_array[i, j, k] & 0xFE) | int(binary_data[binary_idx])
                        binary_idx += 1
                    if binary_idx % progress_step == 0:
                        print_progress_bar(binary_idx, data_len, prefix='Progress:', 
                                         suffix=f'Embedding data ({binary_idx:,}/{data_len:,} bits)')
        
        print_progress_bar(data_len, data_len, prefix='Progress:', suffix='Data embedding complete')
        
        # Save image
        print_status("Saving encrypted image", "processing")
        os.makedirs(os.path.dirname(output_image), exist_ok=True)
        img = Image.fromarray(img_array)
        img.save(output_image, format='PNG', optimize=False)
        
        # Final status
        if os.path.exists(output_image):
            output_info = get_file_info(output_image)
            print(f"\n{Colors.CYAN}Output Information:{Colors.ENDC}")
            print(f"{Colors.BLUE}├─ Location: {output_image}")
            print(f"├─ Size: {output_info['size']}")
            print(f"└─ Created: {output_info['created']}{Colors.ENDC}\n")
            print_status("Encryption completed successfully", "success")
        else:
            raise ValueError("Failed to save encrypted image")
        
        return key
        
    except Exception as e:
        print_status(f"Encryption failed: {str(e)}", "error")
        raise

def decrypt_image_to_file(input_image, output_dir=None, key=None):
    """Decrypt an image back to the original file"""
    try:
        print_status("Starting decryption process", "processing")
        print_status(f"Source image: {input_image}", "info")
        
        # Get image information
        image_info = get_file_info(input_image)
        print(f"\n{Colors.CYAN}Image Information:{Colors.ENDC}")
        print(f"{Colors.BLUE}├─ Size: {image_info['size']}")
        print(f"├─ Created: {image_info['created']}")
        print(f"└─ Modified: {image_info['modified']}{Colors.ENDC}\n")
        
        if output_dir is None:
            output_dir = "decrypted_files"
        print_status(f"Output directory: {output_dir}", "info")
        
        if key is None:
            raise ValueError("Decryption key is required")
        
        # Create cipher suite
        cipher_suite = Fernet(key)
        
        # Read and process image
        print_status("Reading encrypted image", "processing")
        img = Image.open(input_image)
        img_array = np.array(img)
        
        # Extract data with progress bar
        print_status("Extracting hidden data", "processing")
        binary_data = ""
        height, width = img_array.shape[:2]
        total_pixels = height * width * 3
        progress_step = total_pixels // 100
        pixel_count = 0
        
        for i in range(height):
            for j in range(width):
                for k in range(3):
                    binary_data += str(img_array[i, j, k] & 1)
                    pixel_count += 1
                    if pixel_count % progress_step == 0:
                        print_progress_bar(pixel_count, total_pixels, prefix='Progress:', 
                                         suffix=f'Extracting data ({pixel_count:,}/{total_pixels:,} pixels)')
        
        print_progress_bar(total_pixels, total_pixels, prefix='Progress:', suffix='Data extraction complete')
        
        # Process binary data
        print_status("Processing extracted data", "processing")
        binary_data = binary_data[:len(binary_data) - (len(binary_data) % 8)]
        data_bytes = bytes(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))
        
        # Decrypt data
        try:
            print_status("Decrypting data", "processing")
            decrypted_data = cipher_suite.decrypt(data_bytes)
            file_name, file_content = decrypted_data.decode().split('|||')
            file_content = base64.b64decode(file_content)
            print_status(f"Successfully decrypted: {file_name}", "success")
        except Exception as e:
            print_status("Failed to decrypt data - invalid key or corrupted data", "error")
            raise
        
        # Save decrypted file
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, file_name)
        
        print_status(f"Saving decrypted file: {output_path}", "processing")
        with open(output_path, 'wb') as file:
            file.write(file_content)
        
        # Final status
        if os.path.exists(output_path):
            output_info = get_file_info(output_path)
            print(f"\n{Colors.CYAN}Decrypted File Information:{Colors.ENDC}")
            print(f"{Colors.BLUE}├─ Location: {output_path}")
            print(f"├─ Size: {output_info['size']}")
            print(f"└─ Created: {output_info['created']}{Colors.ENDC}\n")
            print_status("Decryption completed successfully", "success")
        else:
            raise ValueError("Failed to save decrypted file")
        
        return output_path
        
    except Exception as e:
        print_status(f"Decryption failed: {str(e)}", "error")
        raise

def get_user_input(prompt, default=None):
    """Get user input with optional default value"""
    try:
        if default:
            user_input = input(f"{Colors.CYAN}[?] {prompt} {Colors.WARNING}[{default}]{Colors.ENDC}: ").strip()
            return user_input if user_input else default
        return input(f"{Colors.CYAN}[?] {prompt}{Colors.ENDC}: ").strip()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] Operation cancelled by user{Colors.ENDC}")
        return "4"  # Return exit option

def display_encrypted_images():
    """Display encrypted images in a 3x3 grid with their keys"""
    if not os.path.exists("encrypted_files"):
        print_status("No encrypted files found", "warning")
        return

    # Get all PNG files in encrypted_files directory
    images = [f for f in os.listdir("encrypted_files") if f.endswith('.png')]
    if not images:
        print_status("No encrypted images found", "warning")
        return

    # Load keys from key storage
    keys = load_keys()
    
    print(f"\n{Colors.CYAN}╔════════════════════════════════════════════════════════════════╗")
    print(f"║                     {Colors.WARNING}ENCRYPTED IMAGES{Colors.CYAN}                           ║")
    print(f"╚════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")

    # Display images in rows of 3
    for i in range(0, len(images), 3):
        row = images[i:i+3]
        # Print image names
        for img in row:
            print(f"{Colors.GREEN}╔{'═' * 30}╗{Colors.ENDC}")
            name = img[:27] + "..." if len(img) > 30 else img
            print(f"{Colors.GREEN}║{Colors.BLUE} {name:<28}{Colors.GREEN} ║{Colors.ENDC}")
            print(f"{Colors.GREEN}╚{'═' * 30}╝{Colors.ENDC}", end="  ")
        print("\n")
        # Print keys
        for img in row:
            key = keys.get(img, "Key not found")
            if len(key) > 30:
                print(f"{Colors.WARNING}Key: {key[:27]}...{Colors.ENDC}", end="  ")
            else:
                print(f"{Colors.WARNING}Key: {key}{Colors.ENDC}", end="  ")
        print("\n")

def save_key(image_name, key):
    """Save encryption key for an image"""
    keys_file = "encrypted_files/keys.json"
    keys = load_keys()
    keys[image_name] = key.decode() if isinstance(key, bytes) else key
    os.makedirs("encrypted_files", exist_ok=True)
    with open(keys_file, 'w') as f:
        json.dump(keys, f, indent=4)

def load_keys():
    """Load saved encryption keys"""
    keys_file = "encrypted_files/keys.json"
    if os.path.exists(keys_file):
        with open(keys_file, 'r') as f:
            return json.load(f)
    return {}

def reset_system():
    """Reset the system by deleting all encrypted and decrypted files"""
    try:
        print_status("Preparing to reset system...", "warning")
        
        # List directories to be removed
        dirs = ["encrypted_files", "decrypted_files"]
        
        for dir_path in dirs:
            if os.path.exists(dir_path):
                print_status(f"Removing {dir_path}...", "processing")
                shutil.rmtree(dir_path)
                print_status(f"Removed {dir_path}", "success")
        
        print_status("System reset completed successfully", "success")
    except Exception as e:
        print_status(f"Error during reset: {str(e)}", "error")

def main_menu():
    """Display main menu and handle user interaction"""
    try:
        while True:
            print(f"\n{Colors.CYAN}╔════════════════════════════════╗")
            print(f"║         {Colors.WARNING}MAIN MENU{Colors.CYAN}            ║")
            print(f"╠════════════════════════════════╣")
            print(f"║ {Colors.GREEN}1.{Colors.BLUE} Encrypt a file{Colors.CYAN}             ║")
            print(f"║ {Colors.GREEN}2.{Colors.BLUE} Encrypt text input{Colors.CYAN}         ║")
            print(f"║ {Colors.GREEN}3.{Colors.BLUE} Decrypt an image{Colors.CYAN}           ║")
            print(f"║ {Colors.GREEN}4.{Colors.BLUE} Reset system{Colors.CYAN}               ║")
            print(f"║ {Colors.GREEN}5.{Colors.BLUE} Exit{Colors.CYAN}                       ║")
            print(f"╚════════════════════════════════╝{Colors.ENDC}")
            
            choice = get_user_input("Select an option (1-5)")
            
            if choice == "1":
                try:
                    input_file = get_user_input("Enter the path to the file to encrypt")
                    if input_file == "4":  # User cancelled
                        continue
                    if not os.path.exists(input_file):
                        print_status("File does not exist", "error")
                        continue
                    
                    use_custom = get_user_input("Use custom image as base? (y/n)", "n").lower()
                    if use_custom == "4":  # User cancelled
                        continue
                    
                    custom_image = None
                    if use_custom == "y":
                        custom_image = get_user_input("Enter the path to the custom image")
                        if custom_image == "4":  # User cancelled
                            continue
                        if not os.path.exists(custom_image):
                            print_status("Custom image does not exist", "error")
                            continue
                    
                    key = encrypt_file_to_image(input_file, custom_image=custom_image)
                    if key:
                        save_key(os.path.basename(input_file), key)
                    print_status("Encryption successful!", "success")
                    print_status(f"SAVE THIS KEY FOR DECRYPTION: {key.decode()}", "warning")
                except KeyboardInterrupt:
                    print(f"\n{Colors.WARNING}[!] Encryption cancelled by user{Colors.ENDC}")
                    continue
                except Exception as e:
                    print_status(str(e), "error")
            
            elif choice == "2":
                try:
                    text = get_user_input("Enter the text to encrypt")
                    if text == "4":  # User cancelled
                        continue
                        
                    temp_file = "temp_text.txt"
                    try:
                        with open(temp_file, 'w') as f:
                            f.write(text)
                        
                        use_custom = get_user_input("Use custom image as base? (y/n)", "n").lower()
                        if use_custom == "4":  # User cancelled
                            if os.path.exists(temp_file):
                                os.remove(temp_file)
                            continue
                            
                        custom_image = None
                        if use_custom == "y":
                            custom_image = get_user_input("Enter the path to the custom image")
                            if custom_image == "4":  # User cancelled
                                if os.path.exists(temp_file):
                                    os.remove(temp_file)
                                continue
                            if not os.path.exists(custom_image):
                                print_status("Custom image does not exist", "error")
                                if os.path.exists(temp_file):
                                    os.remove(temp_file)
                                continue
                        
                        key = encrypt_file_to_image(temp_file, custom_image=custom_image)
                        if key:
                            save_key(os.path.basename(temp_file), key)
                        print_status("Encryption successful!", "success")
                        print_status(f"SAVE THIS KEY FOR DECRYPTION: {key.decode()}", "warning")
                        
                    finally:
                        if os.path.exists(temp_file):
                            os.remove(temp_file)
                except KeyboardInterrupt:
                    print(f"\n{Colors.WARNING}[!] Text encryption cancelled by user{Colors.ENDC}")
                    continue
                except Exception as e:
                    print_status(str(e), "error")
            
            elif choice == "3":
                try:
                    input_image = get_user_input("Enter the path to the encrypted image")
                    if input_image == "4":  # User cancelled
                        continue
                    if not os.path.exists(input_image):
                        print_status("Image does not exist", "error")
                        continue
                    
                    key = get_user_input("Enter the decryption key")
                    if key == "4":  # User cancelled
                        continue
                        
                    try:
                        key = key.encode()
                        decrypted_file = decrypt_image_to_file(input_image, key=key)
                        print_status("Decryption successful!", "success")
                        print_status(f"File saved to: {decrypted_file}", "info")
                    except Exception as e:
                        print_status(str(e), "error")
                except KeyboardInterrupt:
                    print(f"\n{Colors.WARNING}[!] Decryption cancelled by user{Colors.ENDC}")
                    continue
            
            elif choice == "4":
                confirm = get_user_input("Are you sure you want to reset the system? (y/n)", "n").lower()
                if confirm == "y":
                    reset_system()
            
            elif choice == "5":
                print_status("Exiting program... Goodbye! 👋", "info")
                break
            
            else:
                print_status("Invalid option", "error")
    
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] Program terminated by user{Colors.ENDC}")
        print_status("Exiting program... Goodbye! 👋", "info")

if __name__ == "__main__":
    try:
        print_banner()
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] Program terminated by user{Colors.ENDC}")
        print_status("Exiting program... Goodbye! 👋", "info")
    except Exception as e:
        print_status(f"An unexpected error occurred: {str(e)}", "error")
        print_status("Exiting program...", "error") 