import requests
import argparse
import json
import sys

# Setup command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="UpSnap Device Debugger")
    parser.add_argument("--url", required=True, help="UpSnap URL (e.g., http://localhost:8090)")
    parser.add_argument("--username", required=True, help="UpSnap Username")
    parser.add_argument("--password", required=True, help="UpSnap Password")
    return parser.parse_args()

def main():
    args = parse_arguments()

    # 1. Authenticate
    print(f"Authenticating with {args.url}...")
    auth_url = f"{args.url}/api/collections/users/auth-with-password"
    try:
        auth_resp = requests.post(auth_url, json={"identity": args.username, "password": args.password})
        auth_resp.raise_for_status()
        token = auth_resp.json().get("token")
        print("Authentication successful.\n")
    except Exception as e:
        print(f"Authentication Failed: {e}")
        sys.exit(1)

    # 2. Get Devices
    print("Fetching device list...")
    devices_url = f"{args.url}/api/collections/devices/records"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        dev_resp = requests.get(devices_url, headers=headers)
        dev_resp.raise_for_status()
        data = dev_resp.json()
    except Exception as e:
        print(f"Failed to fetch devices: {e}")
        sys.exit(1)

    items = data.get("items", [])
    
    if not items:
        print("No devices found in UpSnap.")
        sys.exit(0)

    # 3. Print Results
    first_device = items[0]
    
    print("-" * 40)
    print(f"Found {len(items)} devices.")
    print(f"Here is the raw data for the first device found:")
    print("-" * 40)
    
    # Pretty print the JSON
    print(json.dumps(first_device, indent=4))
    
    print("-" * 40)
    print("AVAILABLE VARIABLES (Keys):")
    print("-" * 40)
    for key in first_device.keys():
        print(f"- {key}")

if __name__ == "__main__":
    main()
