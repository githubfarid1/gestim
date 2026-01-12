import ctypes
import sys
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == '__main__':
    if is_admin():
        # Code to run with administrator privileges goes here
        print("Now running in admin mode. Executing a privileged command...")
        # Example: running a command that requires admin, like 'net session'
        try:
            # Use subprocess.run for modern Python (3.5+)
            command = ["w32tm", "/resync", "/force"]
            subprocess.run(command, check=True, shell=True)
            print("Privileged command executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        input("Press Enter to exit...")
    else:
        # Re-run the program with admin rights
        # The "runas" verb triggers the UAC prompt
        ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas", 
            sys.executable, 
            " ".join(sys.argv), 
            None, 
            1
        )
        sys.exit(0) # Exit the non-admin process
