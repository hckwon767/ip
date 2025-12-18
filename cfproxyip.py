import re
import requests

# 국가 코드 -> 한국어 국가명 매핑
COUNTRY_CODE_TO_KOREAN = {
    'HK': '홍콩', 'HKG': '홍콩', 'SG': '싱가포르', 'SGP': '싱가포르', 
    'JP': '일본', 'JPN': '일본', 'KR': '한국', 'KOR': '한국', 
    'TW': '대만', 'TWN': '대만', 'CN': '중국', 'CHN': '중국',
    'US': '미국', 'USA': '미국', 'GB': '영국', 'GBR': '영국',
    'FR': '프랑스', 'FRA': '프랑스', 'DE': '독일', 'DEU': '독일',
    'IT': '이탈리아', 'ITA': '이탈리아', 'ES': '스페인', 'ESP': '스페인',
}

def get_korean_country_name(country_code):
    """국가 코드를 한국어 국가명으로 변환"""
    if not country_code or country_code == 'N/A':
        return '알수없음'
    
    code_upper = country_code.upper()
    
    if code_upper in COUNTRY_CODE_TO_KOREAN:
        return COUNTRY_CODE_TO_KOREAN[code_upper]
    
    if len(code_upper) == 3:
        two_char_code = code_upper[:2]
        if two_char_code in COUNTRY_CODE_TO_KOREAN:
            return COUNTRY_CODE_TO_KOREAN[two_char_code]
    
    return code_upper

def extract_ip_port_country_code_validated(url):
    """URL에서 IP, Port, 국가 코드 추출"""
    extracted_data = []
    
    try:
        response = requests.get(url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }) 
        response.raise_for_status()
        content = response.text
        
        # 정규식 패턴: 국가 코드, IP, PORT 추출
        pattern = r'- {name:.*?(?:[\uD83C][\uDDE6-\uDDFF]){2}[^A-Z]*?(?P<country_code>[A-Z]{2,3}).*?server:\s*(?P<ip>[\d.]+).*?port:\s*(?P<port>\d+)'
        regex = re.compile(pattern, re.DOTALL | re.IGNORECASE)
        matches = list(regex.finditer(content))
        
        if not matches:
            pattern2 = r'- {name:.*?(?P<country_code>[A-Z]{2,3}).*?server:\s*(?P<ip>[\d.]+).*?port:\s*(?P<port>\d+)'
            regex2 = re.compile(pattern2, re.DOTALL | re.IGNORECASE)
            matches = list(regex2.finditer(content))
        
        for match in matches:
            ip = match.group('ip')
            port = match.group('port')
            raw_country_code = match.group('country_code').upper() if match.group('country_code') else 'N/A'
            korean_name = get_korean_country_name(raw_country_code)
            
            # IP 주소 정렬을 위한 숫자 리스트
            ip_parts = list(map(int, ip.split('.')))
            
            entry = {
                'ip_parts': ip_parts,
                'string': f"{ip}:{port}#{raw_country_code} {korean_name} {port} 메로나"
            }
            
            if entry not in extracted_data:
                extracted_data.append(entry)
        
        # IP 주소 기준 정렬
        extracted_data.sort(key=lambda x: x['ip_parts'])
        
        return [entry['string'] for entry in extracted_data]
        
    except Exception:
        return []

# URL
REAL_TARGET_URL = "https://api.subcsub.com/sub?target=clash&url=https%3A%2F%2Fcm.soso.edu.kg%2Fsub%3Fpassword%3Daaa%26security%3Dtls%26type%3Dws%26host%3Daaaa%26sni%3Daaa%26path%3D%252Fproxyip%253DProxyIP.JP.CMLiussss.Net%26encryption%3Dnone%26allowInsecure%3D1&insert=false&config=https%3A%2F%2Fraw.githubusercontent.com%2Fcmliu%2FACL4SSR%2Fmain%2FClash%2Fconfig%2FACL4SSR_Online.ini&emoji=true&list=true&xudp=false&udp=false&tfo=false&expand=true&scv=false&fdn=false&new_name=true"

# 데이터 추출 및 파일 저장
extracted_list = extract_ip_port_country_code_validated(REAL_TARGET_URL)

# cfproxy.txt 파일로 저장
if extracted_list:
    with open("cfproxy.txt", "w", encoding="utf-8") as f:
        for item in extracted_list:
            f.write(item + "\n")
