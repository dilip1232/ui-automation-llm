import subprocess
import time
from config.config import EMULATOR_NAME, APK_PATH

def start_emulator():
    print("Starting emulator...")
    # Use Popen to run the emulator in the background
    subprocess.Popen(["emulator", "-avd", EMULATOR_NAME, "-read-only"])

def install_apk():
    print("Installing APK...")
    subprocess.run(["adb", "install", APK_PATH], check=True)

def check_devices():
    print("Checking connected devices...")
    subprocess.run(["adb", "devices"], check=True)

def wait_for_device():
    print("Waiting for device to be ready...")
    while True:
        result = subprocess.run(["adb", "shell", "getprop", "sys.boot_completed"], stdout=subprocess.PIPE, text=True)
        if result.stdout.strip() == "1":
            print("Device is ready!")
            break
        time.sleep(5)  # Wait for 5 seconds before checking again

if __name__ == "__main__":
    start_emulator()
    wait_for_device()  # Wait until the emulator is fully booted
    check_devices()
    install_apk()