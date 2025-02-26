import requests
import csv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

def check_proxy(row, api_url_template):
    ip, port, country_code, company = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip()
    api_url = api_url_template.format(ip=ip, port=port)
    try:
        response = requests.get(api_url, timeout=60)
        response.raise_for_status()
        data = response.json()

        proxyip = data.get("proxyip", "")
        if isinstance(proxyip, bool):
            status = proxyip
        elif isinstance(proxyip, str):
            status = proxyip.strip().lower() == "true"
        else:
            status = False

        if status:
            print(f"{ip}:{port} is ALIVE")
            return (f"{ip}:{port}#{country_code} {company}", None)
        else:
            print(f"{ip}:{port} is DEAD")
            return (None, None)
    except requests.exceptions.RequestException as e:
        error_message = f"Error checking {ip}:{port}: {e}"
        print(error_message)
        return (None, error_message)
    except ValueError as ve:
        error_message = f"Error parsing JSON for {ip}:{port}: {ve}"
        print(error_message)
        return (None, error_message)

def main():
    input_file = os.getenv('IP_FILE', 'proxy.txt')
    output_file = 'proxy_updated.txt'
    error_file = 'errorproxy.txt'
    api_url_template = os.getenv('API_URL', 'https://p01--boiling-frame--kw6dd7bjv2nr.code.run/check?ip={ip}&host=speed.cloudflare.com&port={port}&tls=true')

    alive_proxies = []
    error_logs = []

    try:
        with open(input_file, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"File {input_file} not found.")
        return

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(check_proxy, row, api_url_template): row for row in rows if len(row) >= 4}

    for future in as_completed(futures):
        alive, error = future.result()
        if alive:
            ip_port_country_company = alive.split("#")
            ip_port = ip_port_country_company[0].split(":")
            port = ip_port[1]
            if port not in ["443", "8080", "2053", "8443"]: # port가 443 또는 8080이 아닌 경우만 추가
                alive_proxies.append(alive)
        if error:
            error_logs.append(f"{datetime.now()} - {error}")

    try:
        with open(output_file, "w") as f:
            for proxy_info in alive_proxies:
                f.write(proxy_info + "\n")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")
        return

    if error_logs:
        try:
            with open(error_file, "w") as f:
                for error in error_logs:
                    f.write(error + "\n")
            print(f"Errors have been logged in {error_file}.")
        except Exception as e:
            print(f"Error writing to {error_file}: {e}")
            return

    print(f"Alive proxies (excluding ports 443 and 8080) have been appended to {output_file}.") # 메시지 변경

if __name__ == "__main__":
    main()
