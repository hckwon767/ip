import requests
from typing import List

# 사용자 요청에 따라 홍콩(HK) 목록에 고정으로 추가될 호스트 목록
# 포트와 이름은 통일성을 위해 스크립트에서 추가됩니다.
FIXED_HK_HOSTS = [
    "cloudflare.182682.xyz",
    "speed.marisalnc.com",
    "freeyx.cloudflare88.eu.org",
    "bestcf.top",
    "cdn.2020111.xyz",
    "cfip.cfcdn.vip",
    "cf.0sm.com",
    "cf.090227.xyz",
    "cf.zhetengsha.eu.org",
    "cloudflare.9jy.cc",
    "cf.zerone-cdn.pp.ua",
    "cfip.1323123.xyz",
    "cnamefuckxxs.yuchen.icu",
    "cloudflare-ip.mofashi.ltd",
    "115155.xyz",
    "cname.xirancdn.us",
    "f3058171cad.002404.xyz",
    "8.889288.xyz",
    "cdn.tzpro.xyz",
    "cf.877771.xyz",
    "xn--b6gac.eu.org",
]

def process_proxy_list_to_file(
    url: str, 
    output_filename: str = "proxy_filtered_list.txt", 
    target_countries: List[str] = None
):
    """
    주어진 URL에서 프록시 목록을 읽어와 지정된 국가 코드에 해당하는 줄만 필터링하고,
    지정된 형식으로 변환하여 파일에 저장합니다. 이 함수는 파일을 'w' 모드로 열어 
    기존 내용을 덮어씁니다. (고정 목록 추가를 위해 'w' 모드 유지)

    Args:
        url (str): 프록시 목록이 있는 URL.
        output_filename (str): 결과를 저장할 파일의 이름.
        target_countries (List[str]): 필터링할 국가 코드 목록.
    """
    
    # target_countries가 제공되지 않으면 기본값으로 'KR'을 사용합니다.
    if target_countries is None:
        target_countries = ['KR']

    dynamic_count = 0
    
    try:
        # 1. 데이터 가져오기
        response = requests.get(url, timeout=10) # 타임아웃 추가로 안정성 향상
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킵니다.

        lines = response.text.splitlines()

        # 2. 필터링 및 파일 저장 (w 모드로 덮어쓰기)
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
                        dynamic_count += 1
        
        print(f"✅ URL에서 동적 목록을 성공적으로 가져왔습니다.")
        print(f"   - 총 {dynamic_count}개의 필터링된 동적 프록시 목록이 '{output_filename}'에 저장되었습니다.")
        return dynamic_count

    except requests.exceptions.RequestException as e:
        print(f"❌ URL에서 데이터를 가져오는 중 오류가 발생했습니다: {e}")
    except Exception as e:
        print(f"❌ 스크립트 실행 중 오류가 발생했습니다: {e}")
    
    return dynamic_count

def append_fixed_entries(
    output_filename: str, 
    hosts: List[str], 
    country_code: str, 
    default_port: str = "443", 
    default_name: str = "CDN Host"
):
    """
    고정된 호스트 목록을 지정된 형식으로 변환하여 기존 파일에 추가합니다.
    
    Args:
        output_filename (str): 추가할 파일의 이름.
        hosts (List[str]): 고정된 호스트(도메인) 목록.
        country_code (str): 사용할 국가 코드.
        default_port (str): 호스트에 적용할 기본 포트.
        default_name (str): 호스트에 적용할 기본 이름.
    """
    fixed_count = 0
    try:
        # 'a' 모드(append)로 파일을 열어 내용을 추가합니다.
        with open(output_filename, 'a', encoding='utf-8') as outfile:
            for host in hosts:
                # 원하는 출력 형식으로 조합하여 파일에 씁니다. (예: domain:443#HK CDN Host)
                outfile.write(f"{host}:{default_port}#{country_code} {default_name}\n")
                fixed_count += 1
        
        print(f"   - 총 {fixed_count}개의 고정 {country_code} 호스트 목록이 '{output_filename}' 파일에 추가되었습니다.")

    except Exception as e:
        print(f"❌ 고정 목록을 파일에 추가하는 중 오류가 발생했습니다: {e}")
        
# --- 스크립트 사용 방법 ---
if __name__ == "__main__":
    
    proxy_list_url = "https://raw.githubusercontent.com/tedjo877/cek/refs/heads/main/update_proxyip.txt" 
    print(f"🔗 데이터 출처 URL: {proxy_list_url}\n")

    # 1. 한국(KR) 프록시 필터링
    print("--- 1. 한국(KR) 프록시 필터링 시작 (출력: krlist.txt) ---")
    process_proxy_list_to_file(
        url=proxy_list_url, 
        output_filename="krlist.txt", 
        target_countries=['KR']
    )
    
    # 2. 홍콩(HK) 프록시 필터링 + 고정 목록 추가 (요청 사항 반영)
    print("\n--- 2. 홍콩(HK) 프록시 필터링 및 고정 목록 추가 시작 (출력: hklist.txt) ---")
    
    # 2-1. 동적 목록 필터링 (파일 덮어쓰기)
    process_proxy_list_to_file(
        url=proxy_list_url, 
        output_filename="hklist.txt", 
        target_countries=['HK']
    )
    
    # 2-2. 고정 목록 추가 (파일 이어쓰기)
    append_fixed_entries(
        output_filename="hklist.txt",
        hosts=FIXED_HK_HOSTS,
        country_code='HK'
    )

    # 3. 일본(JP) 프록시 필터링
    print("\n--- 3. 일본(JP) 프록시 필터링 시작 (출력: jplist.txt) ---")
    process_proxy_list_to_file(
        url=proxy_list_url, 
        output_filename="jplist.txt", 
        target_countries=['JP']
    )
    
    # 4. 싱가포르(SG) 프록시 필터링
    print("\n--- 4. 싱가포르(SG) 프록시 필터링 시작 (출력: sglist.txt) ---")
    process_proxy_list_to_file(
        url=proxy_list_url, 
        output_filename="sglist.txt", 
        target_countries=['SG']
    )

    # 5. 대만(TW) 프록시 필터링
    print("\n--- 5. 대만(TW) 프록시 필터링 시작 (출력: twlist.txt) ---")
    process_proxy_list_to_file(
        url=proxy_list_url, 
        output_filename="twlist.txt", 
        target_countries=['TW']
    )
    
    print("\n--- 모든 필터링 작업이 완료되었습니다. ---")
