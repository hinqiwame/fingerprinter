import os
import sys
import uuid
import getpass
import ctypes
import winreg
import logging
from typing import Optional

class Fingerprinter:
    """Class for spoofing various system fingerprint parameters in Windows"""
    
    def __init__(self):
        self.setup_logging()
        self.is_admin = self.check_admin_rights()
        
    def setup_logging(self):
        """Setup logging"""
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # File handler with UTF-8 encoding
        file_handler = logging.FileHandler('fingerprinter.log', encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Setup logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def check_admin_rights(self) -> bool:
        """Check administrator privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
            
    def check_os(self) -> bool:
        """Check operating system"""
        return sys.platform == "win32"
        
    def get_current_guid(self) -> Optional[str]:
        """Get current Machine GUID"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Cryptography",
                0,
                winreg.KEY_READ | winreg.KEY_WOW64_64KEY
            )
            current_guid, _ = winreg.QueryValueEx(key, "MachineGuid")
            winreg.CloseKey(key)
            return current_guid
        except Exception as e:
            self.logger.error(f"Error getting GUID: {e}")
            return None
            
    def spoof_machine_guid(self) -> bool:
        """Spoof Machine GUID"""
        try:
            current_guid = self.get_current_guid()
            if current_guid:
                self.logger.info(f"Current Machine GUID: {current_guid}")
                
            new_guid = str(uuid.uuid4())
            
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Cryptography",
                0,
                winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY
            )
            winreg.SetValueEx(key, "MachineGuid", 0, winreg.REG_SZ, new_guid)
            winreg.CloseKey(key)
            
            self.logger.info(f"Machine GUID successfully changed to: {new_guid}")
            return True
            
        except PermissionError:
            self.logger.error("Access denied. Please run as administrator.")
            return False
        except Exception as e:
            self.logger.error(f"Error spoofing Machine GUID: {e}")
            return False
            
    def spoof_product_id(self) -> bool:
        """Spoof Product ID"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
                0,
                winreg.KEY_READ | winreg.KEY_WOW64_64KEY
            )
            current_pid, _ = winreg.QueryValueEx(key, "ProductId")
            winreg.CloseKey(key)
            
            self.logger.info(f"Current Product ID: {current_pid}")
            
            # Generate new Product ID in format XXXXX-XXXXX-XXXXX-XXXXX
            new_pid = '-'.join([str(uuid.uuid4())[:5].upper() for _ in range(4)])
            
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
                0,
                winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY
            )
            winreg.SetValueEx(key, "ProductId", 0, winreg.REG_SZ, new_pid)
            winreg.CloseKey(key)
            
            self.logger.info(f"Product ID successfully changed to: {new_pid}")
            return True
            
        except PermissionError:
            self.logger.error("Access denied. Please run as administrator.")
            return False
        except Exception as e:
            self.logger.error(f"Error spoofing Product ID: {e}")
            return False
            
    def spoof_install_date(self) -> bool:
        """Spoof Windows installation date"""
        try:
            from datetime import datetime, timedelta
            import random
            
            # Generate random date within last 2 years
            days_ago = random.randint(30, 730)
            new_date = datetime.now() - timedelta(days=days_ago)
            new_date_unix = int(new_date.timestamp())
            
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
                0,
                winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY
            )
            winreg.SetValueEx(key, "InstallDate", 0, winreg.REG_DWORD, new_date_unix)
            winreg.CloseKey(key)
            
            self.logger.info(f"Install date changed to: {new_date.strftime('%Y-%m-%d')}")
            return True
            
        except PermissionError:
            self.logger.error("Access denied. Please run as administrator.")
            return False
        except Exception as e:
            self.logger.error(f"Error spoofing install date: {e}")
            return False
            
    def clear_dns_cache(self) -> bool:
        """Clear DNS cache"""
        try:
            os.system("ipconfig /flushdns")
            self.logger.info("DNS cache cleared")
            return True
        except Exception as e:
            self.logger.error(f"Error clearing DNS cache: {e}")
            return False
            
    def clear_temp_files(self) -> bool:
        """Clear temporary files"""
        try:
            temp_paths = [
                os.environ.get('TEMP'),
                os.environ.get('TMP'),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp')
            ]
            
            for temp_path in temp_paths:
                if temp_path and os.path.exists(temp_path):
                    for root, dirs, files in os.walk(temp_path, topdown=False):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                os.remove(file_path)
                            except:
                                pass
                                
            self.logger.info("Temporary files cleared")
            return True
        except Exception as e:
            self.logger.error(f"Error clearing temporary files: {e}")
            return False
            
    def run_full_spoof(self) -> bool:
        """Run full spoofing"""
        self.logger.info("Starting full HWID spoofing...")
        
        success_count = 0
        total_operations = 4
        
        # Machine GUID spoofing
        if self.spoof_machine_guid():
            success_count += 1
            
        # Product ID spoofing
        if self.spoof_product_id():
            success_count += 1
            
        # Install date spoofing
        if self.spoof_install_date():
            success_count += 1
            
        # Clear cache and temporary files
        if self.clear_dns_cache():
            success_count += 1
            
        self.clear_temp_files()  # Not critical if failed
        
        self.logger.info(f"Spoofing completed. Successfully executed: {success_count}/{total_operations}")
        return success_count == total_operations

def main():
    """Main function"""
    try:
        # Set window title
        try:
            os.system("title Fingerprinter")
        except:
            pass
            
        print("=" * 50)
        print("        FINGERPRINTER | made by @hinqiwame")
        print("=" * 50)
        
        spoofer = Fingerprinter()
        
        # Check OS
        if not spoofer.check_os():
            print("[!] This software is only for Windows.")
            return
            
        print(f"[+] OS: {sys.platform}")
        
        # Check administrator privileges
        if not spoofer.is_admin:
            print("[!] WARNING: Program is running without administrator privileges!")
            print("[!] Some functions may not work correctly.")
            print("[!] It is recommended to run as administrator.")
            print()
            
        # Menu selection
        print("Select an action:")
        print("1. Full spoofing (recommended)")
        print("2. Machine GUID spoofing only")
        print("3. Product ID spoofing only")
        print("4. Install date spoofing only")
        print("5. Clear cache and temporary files")
        print("0. Exit")
        
        while True:
            try:
                choice = input("\nEnter number (0-5): ").strip()
                
                if choice == "0":
                    print("[~] Exiting program...")
                    break
                elif choice == "1":
                    spoofer.run_full_spoof()
                    break
                elif choice == "2":
                    spoofer.spoof_machine_guid()
                    break
                elif choice == "3":
                    spoofer.spoof_product_id()
                    break
                elif choice == "4":
                    spoofer.spoof_install_date()
                    break
                elif choice == "5":
                    spoofer.clear_dns_cache()
                    spoofer.clear_temp_files()
                    break
                else:
                    print("[!] Invalid choice. Try again.")
                    
            except KeyboardInterrupt:
                print("\n[~] Operation cancelled by user.")
                break
                
    except Exception as e:
        print(f"[!] An error occurred: {e}")
        
    finally:
        print("\n[~] Press Enter to exit...")
        getpass.getpass("")

if __name__ == "__main__":
    main()
