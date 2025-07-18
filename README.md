<p align="center">
  <img width="250" alt="Fingerprinter logo" src="img/fingerprinter.png">
</p>

# Fingerprinter

Spoof hardware IDs with a single click!

> FOR EDUCATIONAL PURPOSES ONLY. Use responsibly.
>

---

## Features
- Machine GUID Spoofing  
- Product ID Spoofing  
- Windows Install Date Spoofing  
- DNS Cache Clearing  
- Temporary Files Cleanup  
- Logging to external file 
- Full Automation Mode

## Download
A precompiled `.exe` version is available under the [Releases](https://google.com/) tab.

---

## Manual Launch (Python)

If you prefer running the script manually, follow these steps:

### Step 1 - Install Python

Download and install **Python 3.8 or newer** from the [official website](https://www.python.org/downloads/windows/).  
During installation, make sure to enable **"Add Python to PATH"**.

### Step 2 - Get the code

Download the ZIP archive from GitHub or use Git:

```bash
git clone https://github.com/hinqiwame/fingerprinter.git
cd fingerprinter\src
```

### Step 3 - Run the script

Open Command Prompt as Administrator, navigate to the folder, and run:

```
py fingerprinter.py
```

## Example output
```
==================================================
        FINGERPRINTER | made by @hinqiwame
==================================================
[+] OS: win32
[!] WARNING: Program is running without administrator privileges!
[!] Some functions may not work correctly.
[!] It is recommended to run as administrator.

Select an action:
1. Full spoofing (recommended)
2. Machine GUID spoofing only
3. Product ID spoofing only
4. Install date spoofing only
5. Clear cache and temporary files
0. Exit
```

## Requirements

- Windows 10 or 11 (64-bit)

- Python 3.8+ (if not using the .exe)

- Administrator privileges for registry changes


