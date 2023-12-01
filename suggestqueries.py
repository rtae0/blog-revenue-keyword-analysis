import requests
import xml.etree.ElementTree as ET

def get_google_suggestions(search_query):
    # Google Suggest API URL 설정
    url = f"https://suggestqueries.google.com/complete/search?output=toolbar&q={search_query}"

    # 요청 보내고 응답 받기
    response = requests.get(url)

    # 응답을 파싱하기 위해 XML 파서 사용
    xml_data = response.text
    root = ET.fromstring(xml_data)

    # 추천 검색어를 저장할 리스트 초기화
    suggestions = []

    # 각 CompleteSuggestion 요소를 반복하여 추천 검색어 데이터 추출
    for suggestion in root.findall(".//CompleteSuggestion"):
        data = suggestion.find("suggestion").attrib["data"]
        suggestions.append(data)

    return suggestions


