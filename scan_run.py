#!/usr/bin/env python3

import requests
import os
import argparse

def create_group (group_name):
    url = 'https://api.metascan-online.com/v1/groups'
    headers = {'apikey': 'YOUR_API_KEY'} # Replace with your MetaScan API key
    data = {'name': group_name}
    response = requests.post(url, headers = headers, json = data)
    if response.status_code == 200:
        return response.json()['data']['group_id']
    else:
        print(f"Failed to create group: {response.text}")
        return None

def add_ip_to_group(group_id, ip_address):
    url = f'https://api.metascan-online.com/v1/groups/{group_id}/ips'
    headers = {'apikey': 'YOUR_API_KEY'} # Replace with your MetaScan API key
    data = {'ip': ip_address}
    response = requests.post(url, headers = headers, json = data)
    if response.status_code != 200:
        print(f"Failed to add IP address to group: {response.text}")

def start_scan (group_id):
    url = f'https://api.metascan-online.com/v1/groups/{group_id}/scans'
    headers = {'apikey': 'YOUR_API_KEY'} # Replace with your MetaScan API key
    response = requests.post(url, headers = headers)
    if response.status_code != 200:
        print(f"Failed to start scanner: {response.text}")

def main():
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "--target",
            type=str,
            help='Path to dir with ips'
        )
    args = parser.parse_args()
    if args.target:
        dir_target = args.target
    else:
        dir_target = '.'
    # Read IP addresses from a text file
    files = os.listdir(dir_target)
    txt_files = [file for file in files if file.endswith('.txt')]
    for filename in txt_files:
        filename = 'ip_addresses.txt'
        with open(filename, 'r') as file:
            ip_addresses = file.read().splitlines()

        # work and IP address settings
        group_name = filename.split('.')[0].replace('-', '_')
        group_id = create_group(group_name)
        if group_id:
            for ip in ip_addresses:
                add_ip_to_group(group_id, ip)

            # Start scanning group
            start_scan(group_id)

if __name__=="__main__":
    main()