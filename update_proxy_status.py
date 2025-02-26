import requests
import csv
import shutil
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_proxy(row, api_url_template):
    ip, port, country_code, name = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip()
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
            return (f"{ip}:{port}#{country_code} {name}", None)  # 수정된 부분
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
        print(f"File {input_file} tidak ditemukan.")
        return

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(check_proxy, row, api_url_template): row for row in rows if len(row) >= 4} #row 길이가 4 이상인지 확인

    for future in as_completed(futures):
        alive, error = future.result()
        if alive:
            alive_proxies.append(alive)
        if error:
            error_logs.append(error)

    try:
        with open(output_file, "w") as f: #csv writer가 아닌 일반 write로 변경
            for proxy in alive_proxies:
                f.write(proxy + "\n")
    except Exception as e:
        print(f"Error menulis ke {output_file}: {e}")
        return

    if error_logs:
        try:
            with open(error_file, "w") as f:
                for error in error_logs:
                    f.write(error + "\n")
            print(f"Beberapa error telah dicatat di {error_file}.")
        except Exception as e:
            print(f"Error menulis ke {error_file}: {e}")
            return

    try:
        shutil.move(output_file, input_file)
        print(f"{input_file} telah diperbarui dengan proxy yang ALIVE.")
    except Exception as e:
        print(f"Error menggantikan {input_file}: {e}")

if __name__ == "__main__":
    main()
