import requests
from typing import List

def process_proxy_list_to_file(
    url: str, 
    output_filename: str = "proxy_filtered_list.txt", 
    target_countries: List[str] = None
):
    """
    주어진 URL에서 프록시 목록을 읽어와 지정된 국가 코드에 해당하는 줄만 필터링하고,
    지정된 형식으로 변환하여 파일에 저장합니다.

    Args:
        url (str): 프록시 목록이 있는 URL.
        output_filename (str): 결과를 저장할 파일의 이름 (기본값: 'proxy_filtered_list.txt').
        target_countries (List[str]): 필터링할 국가 코드 목록 (예: ['KR', 'HK', 'JP']).
                                      None으로 지정하면 기본값 ['KR']을 사용합니다.
    """
    
    # target_countries가 제공되지 않으면 기본값으로 'KR'을 사용합니다.
    if target_countries is None:
        target_countries = ['KR']

    try:
        # 1. 데이터 가져오기
        response = requests.get(url, timeout=10) # 타임아웃 추가로 안정성 향상
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킵니다.

        lines = response.text.splitlines()

        # 2. 필터링 및 파일 저장
        count = 0
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            for line in lines:
                parts = line.strip().split(',')
                
                # 프록시 데이터가 'ip,port,country code,name' 4가지 구성인지 확인
                if len(parts) == 4:
                    ip = parts[0].strip()
                    port = parts[1].strip()
                    country_code = parts[2].strip()
                    name = parts[3].strip()

                    # 지정된 국가 코드 목록에 포함되는지 확인하여 필터링합니다.
                    if country_code in target_countries:
                        # 원하는 출력 형식으로 조합하여 파일에 씁니다. (예: 123.45.67.89:8080#KR Korea Proxy)
                        outfile.write(f"{ip}:{port}#{country_code} {name}\n")
                        count += 1
        
        print(f"✅ {url} 에서 데이터를 성공적으로 가져왔습니다.")
        print(f"✅ 총 {count}개의 필터링된 프록시 목록이 '{output_filename}' 파일에 저장되었습니다.")

    except requests.exceptions.RequestException as e:
        print(f"❌ URL에서 데이터를 가져오는 중 오류가 발생했습니다: {e}")
    except Exception as e:
        print(f"❌ 스크립트 실행 중 오류가 발생했습니다: {e}")

# --- 스크립트 사용 방법 (수정됨) ---
if __name__ == "__main__":
    # 실제 URL로 변경해 주세요. (제공해주신 URL을 사용합니다.)
#    proxy_list_url = "https://raw.githubusercontent.com/freetomaid/5412/refs/heads/main/proxylist2.txt" 
    proxy_list_url = "https://raw.githubusercontent.com/tedjo877/cek/refs/heads/main/update_proxyip.txt" 

    # 1. 한국(KR)만 필터링하여 krlist.txt에 저장
    print("--- 1. 한국(KR) 프록시 필터링 시작 (출력: krlist.txt) ---")
    process_proxy_list_to_file(
        url=proxy_list_url, 
        output_filename="krlist.txt", 
        target_countries=['KR']
    )
    
    # 2. 홍콩(HK)만 필터링하여 hklist.txt에 저장
    print("\n--- 2. 홍콩(HK) 프록시 필터링 시작 (출력: hklist.txt) ---")
    process_proxy_list_to_file(
        url=proxy_list_url, 
        output_filename="hklist.txt", 
        target_countries=['HK']
    )

    # 3. 일본(JP)만 필터링하여 jplist.txt에 저장
    print("\n--- 3. 일본(JP) 프록시 필터링 시작 (출력: jplist.txt) ---")
    process_proxy_list_to_file(
        url=proxy_list_url, 
        output_filename="jplist.txt", 
        target_countries=['JP']
    )
    
    # 4. 싱가포르(SG)만 필터링하여 sglist.txt에 저장 (추가됨)
    print("\n--- 4. 싱가포르(SG) 프록시 필터링 시작 (출력: sglist.txt) ---")
    process_proxy_list_to_file(
        url=proxy_list_url, 
        output_filename="sglist.txt", 
        target_countries=['SG']
    )

    # 5. 대만(TW)만 필터링하여 twlist.txt에 저장 (추가됨)
    print("\n--- 5. 대만(TW) 프록시 필터링 시작 (출력: twlist.txt) ---")
    process_proxy_list_to_file(
        url=proxy_list_url, 
        output_filename="twlist.txt", 
        target_countries=['TW']
    )
