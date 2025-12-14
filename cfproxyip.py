import re
import requests
from requests.exceptions import RequestException

# 국가 코드 -> 한국어 국가명 매핑 딕셔너리
COUNTRY_CODE_TO_KOREAN = {
    # 아시아
    'HK': '홍콩', 'SG': '싱가포르', 'JP': '일본', 'KR': '한국', 'TW': '대만',
    'CN': '중국', 'TH': '태국', 'VN': '베트남', 'MY': '말레이시아', 'ID': '인도네시아',
    'PH': '필리핀', 'IN': '인도', 'PK': '파키스탄', 'BD': '방글라데시', 'MM': '미얀마',
    'LA': '라오스', 'KH': '캄보디아', 'BN': '브루나이', 'MO': '마카오', 'NP': '네팔',
    
    # 북아메리카
    'US': '미국', 'CA': '캐나다', 'MX': '멕시코',
    
    # 유럽
    'GB': '영국', 'FR': '프랑스', 'DE': '독일', 'IT': '이탈리아', 'ES': '스페인',
    'NL': '네덜란드', 'SE': '스웨덴', 'NO': '노르웨이', 'FI': '핀란드', 'DK': '덴마크',
    'RU': '러시아', 'UA': '우크라이나', 'PL': '폴란드', 'CZ': '체코', 'SK': '슬로바키아',
    'HU': '헝가리', 'AT': '오스트리아', 'CH': '스위스', 'BE': '벨기에', 'PT': '포르투갈',
    'GR': '그리스', 'IE': '아일랜드', 'IS': '아이슬란드',
    
    # 오세아니아
    'AU': '호주', 'NZ': '뉴질랜드',
    
    # 아프리카
    'ZA': '남아프리카', 'EG': '이집트', 'KE': '케냐', 'NG': '나이지리아',
    
    # 남아메리카
    'BR': '브라질', 'AR': '아르헨티나', 'CL': '칠레', 'CO': '콜롬비아', 'PE': '페루',
    
    # 중동
    'AE': '아랍에미리트', 'SA': '사우디아라비아', 'QA': '카타르', 'KW': '쿠웨이트',
    'BH': '바레인', 'OM': '오만', 'JO': '요르단', 'LB': '레바논', 'IL': '이스라엘',
    'TR': '터키', 'IR': '이란',
    
    # 기타 일반적인 코드
    'EU': '유럽', 'UK': '영국', 'AN': '네덜란드령 안틸레스',
}

def get_korean_country_name(country_code):
    """국가 코드를 한국어 국가명으로 변환"""
    if not country_code or country_code == 'N/A':
        return '알수없음'
    
    # 대문자로 변환
    code_upper = country_code.upper()
    
    # 매핑된 국가명 반환, 없으면 코드 그대로 반환
    return COUNTRY_CODE_TO_KOREAN.get(code_upper, code_upper)

def extract_ip_port_country_code_validated(url):
    """
    URL에서 텍스트를 가져와 IP, Port, 그리고 name 필드 내 2~3자리 문자열 국가 코드를 추출합니다.
    """
    extracted_data = []
    
    try:
        print(f"URL에서 데이터 가져오는 중: {url}")
        
        response = requests.get(url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }) 
        response.raise_for_status() 
        
        # 인코딩 문제 방지
        content = response.text
        
        # 여러 패턴 시도
        patterns = [
            # 패턴 1: name 필드에서 국가 코드 추출 시도
            r'name:\s*[\w\s]*?(?P<country_code>[A-Z]{2,3})[^A-Z]*?server:\s*(?P<ip>[\d.]+).*?port:\s*(?P<port>\d+)',
            
            # 패턴 2: 더 넓은 범위에서 국가 코드 찾기
            r'(?:name|country|code)[^A-Z]*?(?P<country_code>[A-Z]{2,3})[^A-Z]*?server:\s*(?P<ip>[\d.]+).*?port:\s*(?P<port>\d+)',
            
            # 패턴 3: 깃발 이모지와 함께 있는 국가 코드
            r'[\uD83C][\uDDE6-\uDDFF]{2}[^A-Z]*?(?P<country_code>[A-Z]{2,3})[^A-Z]*?server:\s*(?P<ip>[\d.]+).*?port:\s*(?P<port>\d+)',
        ]
        
        match_count = 0
        found_pattern = None
        
        for i, pattern in enumerate(patterns, 1):
            regex = re.compile(pattern, re.DOTALL | re.IGNORECASE)
            matches = list(regex.finditer(content))
            
            if matches:
                print(f"패턴 {i}에서 {len(matches)}개의 매치를 찾았습니다.")
                found_pattern = i
                
                for match in matches:
                    match_count += 1
                    ip = match.group('ip')
                    port = match.group('port')
                    raw_country_code = match.group('country_code').upper() if match.group('country_code') else 'N/A'
                    
                    # 한국어 국가명 가져오기
                    korean_name = get_korean_country_name(raw_country_code)
                    
                    # 형식: IP:PORT#국가코드 한국어국가명
                    entry = f"{ip}:{port}#{raw_country_code} {korean_name}"
                    
                    # 중복 제거
                    if entry not in extracted_data:
                        extracted_data.append(entry)
                
                break  # 하나의 패턴이 성공하면 나머지는 스킵
        
        if match_count == 0:
            print("❗경고: 모든 패턴으로 매치되는 항목을 찾지 못했습니다.")

    except RequestException as e:
        print(f"오류: URL 접근 또는 통신 중 문제가 발생했습니다: {e}")
    except Exception as e:
        print(f"데이터 처리 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

    return extracted_data

# --- 실제 실행 부분 ---

REAL_TARGET_URL = "https://url.v1.mk/sub?target=clash&url=https%3A%2F%2Fcm.soso.edu.kg%2Fsub%3Fpassword%3Daaa%26security%3Dtls%26type%3Dws%26host%3Daaaa%26sni%3Daaa%26path%3D%252Fproxyip%253DProxyIP.JP.CMLiussss.Net%26encryption%3Dnone%26allowInsecure%3D1&insert=false&config=https%3A%2F%2Fraw.githubusercontent.com%2Fcmliu%2FACL4SSR%2Fmain%2FClash%2Fconfig%2FACL4SSR_Online.ini&emoji=true&list=true&xudp=false&udp=false&tfo=false&expand=true&scv=false&fdn=false&new_name=true"

# 함수 실행
print("=== 국가 코드 추출 시작 (한국어 국가명 포함) ===")
extracted_list = extract_ip_port_country_code_validated(REAL_TARGET_URL)

# 결과 출력 - 전체 항목 출력
print("\n" + "="*70)
print("전체 IP:PORT#국가코드 한국어국가명 목록")
print("="*70)

if extracted_list:
    # 모든 항목 출력
    for idx, item in enumerate(extracted_list, 1):
        print(f"{idx:4d}. {item}")
    
    print("="*70)
    print(f"총 {len(extracted_list)}개 항목 추출 완료")
    print("="*70)
    
    # 국가별 통계
    print("\n국가별 통계:")
    country_stats = {}
    for item in extracted_list:
        # "HK 홍콩" 부분 추출
        parts = item.split('#')[1].split()
        if len(parts) >= 2:
            country_info = f"{parts[0]} {parts[1]}"
        else:
            country_info = parts[0]
        
        country_stats[country_info] = country_stats.get(country_info, 0) + 1
    
    # 통계 정렬 및 출력
    sorted_stats = sorted(country_stats.items(), key=lambda x: x[1], reverse=True)
    
    for country_info, count in sorted_stats:
        print(f"  {country_info}: {count}개")
    
    # 요약 정보
    print(f"\n총 {len(sorted_stats)}개 국가/지역 발견")
    
else:
    print("추출된 데이터가 없거나 패턴 매칭에 실패했습니다.")

# 추가 기능: 특정 국가만 필터링하는 함수 (선택사항)
def filter_by_country(data_list, country_code):
    """특정 국가 코드로 데이터 필터링"""
    filtered = []
    for item in data_list:
        if f"#{country_code.upper()}" in item:
            filtered.append(item)
    return filtered

# 사용 예시:
# hk_list = filter_by_country(extracted_list, 'HK')
# print(f"\n홍콩 서버 {len(hk_list)}개:")
# for item in hk_list:
#     print(f"  {item}")
