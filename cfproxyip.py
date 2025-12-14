import re
import requests
from requests.exceptions import RequestException

# 국가 코드 -> 한국어 국가명 매핑 딕셔너리
COUNTRY_CODE_TO_KOREAN = {
    'HK': '홍콩', 'SG': '싱가포르', 'JP': '일본', 'KR': '한국', 'TW': '대만',
    'CN': '중국', 'TH': '태국', 'VN': '베트남', 'MY': '말레이시아', 'ID': '인도네시아',
    'PH': '필리핀', 'IN': '인도', 'PK': '파키스탄', 'BD': '방글라데시', 'MM': '미얀마',
    'LA': '라오스', 'KH': '캄보디아', 'BN': '브루나이', 'MO': '마카오', 'NP': '네팔',
    'US': '미국', 'CA': '캐나다', 'MX': '멕시코', 'GB': '영국', 'FR': '프랑스',
    'DE': '독일', 'IT': '이탈리아', 'ES': '스페인', 'NL': '네덜란드', 'SE': '스웨덴',
    'NO': '노르웨이', 'FI': '핀란드', 'DK': '덴마크', 'RU': '러시아', 'UA': '우크라이나',
    'PL': '폴란드', 'CZ': '체코', 'SK': '슬로바키아', 'HU': '헝가리', 'AT': '오스트리아',
    'CH': '스위스', 'BE': '벨기에', 'PT': '포르투갈', 'GR': '그리스', 'IE': '아일랜드',
    'IS': '아이슬란드', 'AU': '호주', 'NZ': '뉴질랜드', 'ZA': '남아프리카', 'EG': '이집트',
    'KE': '케냐', 'NG': '나이지리아', 'BR': '브라질', 'AR': '아르헨티나', 'CL': '칠레',
    'CO': '콜롬비아', 'PE': '페루', 'AE': '아랍에미리트', 'SA': '사우디아라비아', 'QA': '카타르',
    'KW': '쿠웨이트', 'BH': '바레인', 'OM': '오만', 'JO': '요르단', 'LB': '레바논',
    'IL': '이스라엘', 'TR': '터키', 'IR': '이란', 'EU': '유럽', 'UK': '영국',
}

def get_korean_country_name(country_code):
    """국가 코드를 한국어 국가명으로 변환"""
    if not country_code or country_code == 'N/A':
        return '알수없음'
    return COUNTRY_CODE_TO_KOREAN.get(country_code.upper(), country_code.upper())

def extract_ip_port_country_code_validated(url):
    """
    URL에서 텍스트를 가져와 IP, Port, 그리고 국가 코드를 추출합니다.
    """
    extracted_data = []
    
    try:
        response = requests.get(url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }) 
        response.raise_for_status()
        content = response.text
        
        # 패턴: 국가 코드, IP, PORT 추출
        pattern = r'(?:name|country|code)[^A-Z]*?(?P<country_code>[A-Z]{2,3})[^A-Z]*?server:\s*(?P<ip>[\d.]+).*?port:\s*(?P<port>\d+)'
        regex = re.compile(pattern, re.DOTALL | re.IGNORECASE)
        matches = list(regex.finditer(content))
        
        for match in matches:
            ip = match.group('ip')
            port = match.group('port')
            raw_country_code = match.group('country_code').upper() if match.group('country_code') else 'N/A'
            korean_name = get_korean_country_name(raw_country_code)
            
            # IP 주소를 숫자 리스트로 변환하여 정렬 기준 생성
            ip_parts = list(map(int, ip.split('.')))
            
            # 형식: IP:PORT#국가코드 한국어국가명
            entry = {
                'ip_parts': ip_parts,
                'string': f"{ip}:{port}#{raw_country_code} {korean_name}"
            }
            
            # 중복 제거
            if entry not in extracted_data:
                extracted_data.append(entry)
        
        # IP 주소 기준으로 정렬 (1.2.3.4 형식의 숫자 순서대로)
        extracted_data.sort(key=lambda x: x['ip_parts'])
        
        # 정렬된 문자열 목록만 반환
        return [entry['string'] for entry in extracted_data]
        
    except Exception as e:
        return []

def save_to_file(data_list, filename="cfproxy.txt"):
    """데이터 리스트를 파일로 저장"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for item in data_list:
                f.write(item + '\n')
        print(f"파일 저장 완료: {filename} ({len(data_list)}개 항목)")
        return True
    except Exception as e:
        print(f"파일 저장 실패: {e}")
        return False

# --- 실행 부분 ---

REAL_TARGET_URL = "https://url.v1.mk/sub?target=clash&url=https%3A%2F%2Fcm.soso.edu.kg%2Fsub%3Fpassword%3Daaa%26security%3Dtls%26type%3Dws%26host%3Daaaa%26sni%3Daaa%26path%3D%252Fproxyip%253DProxyIP.JP.CMLiussss.Net%26encryption%3Dnone%26allowInsecure%3D1&insert=false&config=https%3A%2F%2Fraw.githubusercontent.com%2Fcmliu%2FACL4SSR%2Fmain%2FClash%2Fconfig%2FACL4SSR_Online.ini&emoji=true&list=true&xudp=false&udp=false&tfo=false&expand=true&scv=false&fdn=false&new_name=true"

# 함수 실행 및 파일 저장
extracted_list = extract_ip_port_country_code_validated(REAL_TARGET_URL)

# 파일로 저장
if extracted_list:
    save_to_file(extracted_list, "cfproxy.txt")
    
    # 콘솔에도 간단히 확인용으로 첫 5개 항목 출력 (선택사항)
    print("\n파일 내용 샘플 (첫 5개 항목):")
    for i, item in enumerate(extracted_list[:5]):
        print(f"  {item}")
    if len(extracted_list) > 5:
        print(f"  ... 외 {len(extracted_list) - 5}개 항목")
else:
    print("추출된 데이터가 없습니다.")
