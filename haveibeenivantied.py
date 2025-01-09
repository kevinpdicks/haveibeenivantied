import winreg
import re
import requests

def get_ivanti_vpn_version():
    registry_paths = [
        r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",  # Standard 64-bit path
        r"SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall",  # 32-bit on 64-bit
    ]

    for registry_path in registry_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):  # Iterate through subkeys
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        try:
                            # Check the display name of the program
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            if "Ivanti Secure Access Client" in display_name:
                                # Retrieve the version number
                                version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                                return version
                        except FileNotFoundError:
                            continue
        except Exception as e:
            pass

    return None

def get_latest_version():
    # Hard-coded latest version as of the most recent known update
    return "22.7R4"

def compare_versions(installed_version, latest_version):
    def version_to_tuple(version):
        # Convert version strings like "22.7R4" into tuples for comparison
        version = re.sub(r'[R]', '.', version)  # Replace R with dot
        return tuple(map(int, re.findall(r'\d+', version)))

    installed_parts = version_to_tuple(installed_version)
    latest_parts = version_to_tuple(latest_version)
    return installed_parts < latest_parts

def main():
    installed_version = get_ivanti_vpn_version()
    if installed_version:
        print(f"Ivanti Secure VPN is installed. Version: {installed_version}")
        latest_version = get_latest_version()
        print(f"Latest version available: {latest_version}")
        if compare_versions(installed_version, latest_version):
            print("You've been Ivanti'ed. Your version is outdated. Please update to the latest version.")
        else:
            print("Your version is up to date.")
    else:
        print("Ivanti Secure VPN is not installed on this system.")

if __name__ == "__main__":
    main()
