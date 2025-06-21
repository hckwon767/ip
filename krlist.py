import requests

def process_proxy_list_to_file(url, output_filename="proxy_kr_hk_jp.txt"):
    """
    주어진 URL에서 프록시 목록을 읽어와 country code가 'KR', 'HK', 또는 'JP'인 줄만 필터링하고,
    지정된 형식으로 변환하여 파일에 저장합니다.

    Args:
        url (str): 프록시 목록이 있는 URL.
        output_filename (str): 결과를 저장할 파일의 이름 (기본값: 'proxy_kr_hk_jp.txt').
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킵니다.

        lines = response.text.splitlines() # URL 내용을 줄 단위로 분리합니다.

        with open(output_filename, 'w', encoding='utf-8') as outfile:
            for line in lines:
                parts = line.strip().split(',') # 각 줄을 쉼표로 분리합니다.
                if len(parts) == 4: # ip, port, country code, name 4가지 구성인지 확인합니다.
                    ip = parts[0]
                    port = parts[1]
                    country_code = parts[2]
                    name = parts[3]

                    if country_code in ['KR', 'HK', 'JP']: # country code가 'KR', 'HK', 또는 'JP'인 경우만 필터링합니다.
                        # 원하는 출력 형식으로 조합하여 파일에 씁니다.
                        outfile.write(f"{ip}:{port}#{country_code} {name}\n")
                    else:
                        # 형식이 맞지 않는 줄은 건너뜁니다.
                        pass
        print(f"필터링된 프록시 목록이 '{output_filename}' 파일에 성공적으로 저장되었습니다.")

    except requests.exceptions.RequestException as e:
        print(f"URL에서 데이터를 가져오는 중 오류가 발생했습니다: {e}")
    except Exception as e:
        print(f"스크립트 실행 중 오류가 발생했습니다: {e}")

# --- 스크립트 사용 방법 ---
if __name__ == "__main__":
    # 여기에 실제 URL을 입력해주세요.
    # 예시: proxy_list_url = "https://raw.githubusercontent.com/someuser/somerepo/main/proxylist.txt"
    proxy_list_url = "https://raw.githubusercontent.com/freetomaid/5412/refs/heads/main/proxylist2.txt" # 이 부분을 실제 URL로 변경해주세요.

    if proxy_list_url == "YOUR_URL_HERE":
        print("프록시 목록이 있는 URL을 'proxy_list_url' 변수에 입력해주세요.")
    else:
        process_proxy_list_to_file(proxy_list_url, output_filename="krlist.txt")
