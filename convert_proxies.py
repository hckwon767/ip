import urllib.request
from typing import Dict

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

def get_country_korean_name(country_code: str) -> str:
    """국가 코드를 한글 국가명으로 변환"""
    return COUNTRY_MAP.get(country_code.upper(), '알수없음')

def convert_proxy_format(input_url: str, output_file: str = "converted_proxies.txt"):
    """
    프록시 데이터 형식을 변환하여 파일로 저장
    
    Args:
        input_url: 원본 데이터 URL
        output_file: 출력 파일명
    """
    try:
        # urllib를 사용하여 파일 내용 가져오기
        with urllib.request.urlopen(input_url) as response:
            data = response.read().decode('utf-8')
        
        lines = data.strip().split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            try:
                # ip:port#countrycode_name 형식 파싱
                if '#' in line:
                    ip_port, country_info = line.split('#', 1)
                    
                    # countrycode 부분만 추출 (countrycode_name에서 countrycode만)
                    country_code = country_info.split('_')[0] if '_' in country_info else country_info
                    
                    # 국가 코드를 대문자로 변환
                    country_code_upper = country_code.upper()
                    
                    # 한글 국가명 가져오기
                    korean_name = get_country_korean_name(country_code_upper)
                    
                    # 새로운 형식으로 변환
                    result = f"{ip_port}#{country_code_upper} {korean_name}"
                    processed_lines.append(result)
                    
            except ValueError:
                # 파싱 오류 시 원본 라인 유지
                processed_lines.append(line)
                continue
        
        # 결과를 파일로 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            for result in processed_lines:
                f.write(result + '\n')
        
        print(f"변환 완료: {len(processed_lines)}개의 항목이 {output_file}에 저장되었습니다.")
            
    except Exception as e:
        print(f"오류 발생: {e}")

def convert_local_file(input_file: str, output_file: str = "converted_proxies.txt"):
    """
    로컬 파일에서 프록시 데이터를 변환하여 파일로 저장
    
    Args:
        input_file: 입력 파일명
        output_file: 출력 파일명
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            try:
                # ip:port#countrycode_name 형식 파싱
                if '#' in line:
                    ip_port, country_info = line.split('#', 1)
                    
                    # countrycode 부분만 추출 (countrycode_name에서 countrycode만)
                    country_code = country_info.split('_')[0] if '_' in country_info else country_info
                    
                    # 국가 코드를 대문자로 변환
                    country_code_upper = country_code.upper()
                    
                    # 한글 국가명 가져오기
                    korean_name = get_country_korean_name(country_code_upper)
                    
                    # 새로운 형식으로 변환
                    result = f"{ip_port}#{country_code_upper} {korean_name}"
                    processed_lines.append(result)
                    
            except ValueError:
                # 파싱 오류 시 원본 라인 유지
                processed_lines.append(line)
                continue
        
        # 결과를 파일로 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            for result in processed_lines:
                f.write(result + '\n')
        
        print(f"변환 완료: {len(processed_lines)}개의 항목이 {output_file}에 저장되었습니다.")
                
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {input_file}")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    # GitHub URL에서 직접 변환
    url = "https://raw.githubusercontent.com/rxsweet/cfip/refs/heads/main/all.txt"
    convert_proxy_format(url, "converted_proxies.txt")
    
    # 로컬 파일 변환 (필요한 경우)
    # convert_local_file("all.txt", "converted_proxies.txt")
