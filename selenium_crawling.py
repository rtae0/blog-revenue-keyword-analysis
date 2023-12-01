from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

def scrape_google_results(search_query, max_len=14):
    # Chrome 옵션 및 서비스 초기화
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    service = Service('./chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 결과를 저장할 리스트 초기화
    collected_links = []

    try:
        # Google 웹사이트 열기
        driver.get("http://www.google.com")

        # 검색창 찾기
        search_box = driver.find_element(By.NAME, 'q')

        # 검색어 입력 및 검색 실행
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)

        # 스크롤 및 결과 처리 루프
        while len(collected_links) < max_len:
            # 페이지의 마지막까지 스크롤
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)  # 추가 결과 로드를 기다리는 시간

            # 현재 페이지의 모든 결과 가져오기
            results = driver.find_elements(By.CSS_SELECTOR, 'div.g')

            # 결과 처리
            for result in results:
                if len(collected_links) >= max_len:
                    break  # max_len 되면 루프 탈출
                link = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                if link not in collected_links:
                    collected_links.append(link)

            if len(collected_links) >= max_len:
                break  # max_len 되면 바깥 루프도 탈출
    finally:
        # 브라우저 종료
        driver.quit()
    print("크롤링 완료 블로그 카운팅 시작")
    blog_count = 0
    site_count = 0
    blog_links = []
    for link in collected_links:
        # 특정 도메인 포함 여부 확인
        if 'tistory.com' in link or 'brunch.co.kr' in link or 'blog.naver.com' in link or 'velog.io' in link or 'medium.com' in link:
            blog_count += 1
            blog_links.append(link)
        site_count += 1

    return blog_count, site_count, blog_links
