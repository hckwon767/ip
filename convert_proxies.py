import urllib.request
from typing import Dict, List, Optional

# 국가 코드와 한글 국가명 매핑 딕셔너리
COUNTRY_MAP: Dict[str, str] = {
    # 아시아
    'KR': '대한민국', 'CN': '중국', 'JP': '일본', 'HK': '홍콩', 'TW': '대만',
    'SG': '싱가포르', 'TH': '태국', 'VN': '베트남', 'MY': '말레이시아', 'ID': '인도네시아',
    'PH': '필리핀', 'IN': '인도', 'BD': '방글라데시', 'PK': '파키스탄', 'LK': '스리랑카',
    
    # 유럽
    'GB': '영국', 'FR': '프랑스', 'DE': '독일', 'IT': '이탈리아', 'ES': '스페인',
    'NL': '네덜란드', 'BE': '벨기에', 'CH': '스위스', 'SE': '스웨덴', 'NO': '노르웨이',
    'FI': '핀란드', 'DK': '덴마크', 'PL': '폴란드', 'CZ': '체코', 'HU': '헝가리',
    'RO': '루마니아', 'BG': '불가리아', 'GR': '그리스', 'PT': '포르투갈', 'AT': '오스트리아',
    'RU': '러시아', 'UA': '우크라이나',
    
    # 북아메리카
    'US': '미국', 'CA': '캐나다', 'MX': '멕시코',
    
    # 남아메리카
    'BR': '브라질', 'AR': '아르헨티나', 'CL': '칠레', 'CO': '콜롬비아', 'PE': '페루',
    
    # 오세아니아
    'AU': '오스트레일리아', 'NZ': '뉴질랜드',
    
    # 아프리카
    'ZA': '남아프리카공화국', 'EG': '이집트', 'NG': '나이지리아', 'KE': '케냐',
    
    # 중동
    'AE': '아랍에미리트', 'SA': '사우디아라비아', 'IL': '이스라엘', 'TR': '튀르키예'
}

# 변환된 데이터 제일 아래에 고정으로 추가될 목록 (HK 홍콩으로 변환되며 "CDN HOST" 태그가 붙음)
FIXED_PROXIES: List[str] = [
    "cloudflare.182682.xyz:443#HK",
    "speed.marisalnc.com:443#HK",
    "freeyx.cloudflare88.eu.org:443#HK",
    "bestcf.top:443#HK",
    "cdn.2020111.xyz:443#HK",
    "cfip.cfcdn.vip:443#HK",
    "cf.0sm.com:443#HK",
    "cf.090227.xyz:443#HK",
    "cf.zhetengsha.eu.org:443#HK",
    "cloudflare.9jy.cc:443#HK",
    "cf.zerone-cdn.pp.ua:443#HK",
    "cfip.1323123.xyz:443#HK",
    "cnamefuckxxs.yuchen.icu:443#HK",
    "cloudflare-ip.mofashi.ltd:443#HK",
    "115155.xyz:443#HK",
    "cname.xirancdn.us:443#HK",
    "f3058171cad.002404.xyz:443#HK",
    "8.889288.xyz:443#HK",
    "cdn.tzpro.xyz:443#HK",
    "cf.877771.xyz:443#HK",
    "xn--b6gac.eu.org:443#HK",
    "kr.tp50000.netlib.re:50000#KR",
    "mfa.gov.ua:443#HK MFA"
]

def get_country_korean_name(country_code: str) -> str:
    """국가 코드를 한글 국가명으로 변환"""
    return COUNTRY_MAP.get(country_code.upper(), '알수없음')

def _process_single_line(line: str, is_cdn_host: bool = False) -> Optional[str]:
    """
    단일 프록시 라인을 새로운 형식으로 변환합니다.
    (ip:port#COUNTRYCODE [CDN HOST] 한글국가명)
    
    Args:
        line: 입력 라인 문자열 (e.g., ip:port#countrycode_name 또는 ip:port#countrycode)
        is_cdn_host: True이면 결과에 " CDN HOST" 문구를 추가합니다.
        
    Returns:
        변환된 라인 문자열, 처리할 수 없는 경우 원본 라인, 또는 빈 라인의 경우 None
    """
    line = line.strip()
    if not line:
        return None
        
    try:
        # ip:port#countrycode_name 형식 파싱
        if '#' in line:
            ip_port, country_info = line.split('#', 1)
            
            # countrycode 부분만 추출
            country_code = country_info.split('_')[0] if '_' in country_info else country_info
            
            # 국가 코드를 대문자로 변환
            country_code_upper = country_code.upper()
            
            # 한글 국가명 가져오기
            korean_name = get_country_korean_name(country_code_upper)
            
            # CDN HOST 문구 조건부 추가
            # is_cdn_host가 True일 때만 ' CDN HOST' 문자열을 추가합니다.
            extra_tag = " CDN HOST" if is_cdn_host else ""
            
            # 새로운 형식으로 변환: ip:port#COUNTRYCODE [CDN HOST] 한글국가명
            return f"{ip_port}#{country_code_upper}{extra_tag} {korean_name}"
            
    except ValueError:
        # 파싱 오류 시 원본 라인 유지
        return line
        
    # '#'이 없는 경우 원본 라인 유지
    return line 

def convert_proxy_format(input_url: str, output_file: str = "converted_proxies.txt"):
    """
    URL에서 프록시 데이터를 가져와 형식을 변환하고 고정 목록을 추가하여 파일로 저장
    
    Args:
        input_url: 원본 데이터 URL
        output_file: 출력 파일명
    """
    processed_lines = []
    
    try:
        # urllib를 사용하여 파일 내용 가져오기
        with urllib.request.urlopen(input_url) as response:
            data = response.read().decode('utf-8')
        
        lines = data.strip().split('\n')
        
        # 1. URL에서 가져온 라인 처리 (CDN HOST 태그 미적용)
        for line in lines:
            result = _process_single_line(line, is_cdn_host=False)
            if result is not None:
                processed_lines.append(result)
        
    except Exception as e:
        print(f"URL에서 데이터를 가져오는 중 오류 발생: {e}")
    
    # 2. 고정 목록 라인 처리 및 추가 (CDN HOST 태그 적용)
    for line in FIXED_PROXIES:
        # FIXED_PROXIES는 is_cdn_host=True로 처리하여 " CDN HOST" 태그를 추가합니다.
        fixed_result = _process_single_line(line, is_cdn_host=True)
        if fixed_result is not None:
            processed_lines.append(fixed_result)
            
    # 3. 결과를 파일로 저장
    if processed_lines:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for result in processed_lines:
                    f.write(result + '\n')
            
            print(f"변환 완료: 총 {len(processed_lines)}개의 항목(고정 목록 포함)이 {output_file}에 저장되었습니다.")
        except Exception as e:
            print(f"파일 저장 중 오류 발생: {e}")
    else:
        print("처리된 유효한 항목이 없으므로 파일이 저장되지 않았습니다.")


def convert_local_file(input_file: str, output_file: str = "converted_proxies.txt"):
    """
    로컬 파일에서 프록시 데이터를 변환하고 고정 목록을 추가하여 파일로 저장
    
    Args:
        input_file: 입력 파일명
        output_file: 출력 파일명
    """
    processed_lines = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # 1. 로컬 파일의 라인 처리 (CDN HOST 태그 미적용)
        for line in lines:
            result = _process_single_line(line, is_cdn_host=False)
            if result is not None:
                processed_lines.append(result)
            
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {input_file}")
        
    except Exception as e:
        print(f"파일 처리 중 오류 발생: {e}")

    # 2. 고정 목록 라인 처리 및 추가 (CDN HOST 태그 적용)
    for line in FIXED_PROXIES:
        # FIXED_PROXIES는 is_cdn_host=True로 처리하여 " CDN HOST" 태그를 추가합니다.
        fixed_result = _process_single_line(line, is_cdn_host=True)
        if fixed_result is not None:
            processed_lines.append(fixed_result)
    
    # 3. 결과를 파일로 저장
    if processed_lines:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for result in processed_lines:
                    f.write(result + '\n')
            
            print(f"변환 완료: 총 {len(processed_lines)}개의 항목(고정 목록 포함)이 {output_file}에 저장되었습니다.")
        except Exception as e:
            print(f"파일 저장 중 오류 발생: {e}")
    else:
        print("처리된 유효한 항목이 없으므로 파일이 저장되지 않았습니다.")

if __name__ == "__main__":
    # GitHub URL에서 직접 변환
    url = "https://raw.githubusercontent.com/rxsweet/cfip/refs/heads/main/all.txt"
    convert_proxy_format(url, "converted_proxies.txt")
    
    # 로컬 파일 변환 (필요한 경우)
    # convert_local_file("all.txt", "converted_proxies_local.txt")
