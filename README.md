# 수익형 블로그를 위한 키워드 분석


## 프로젝트 개요
이 프로젝트는 구글 애드센스를 사용하는 수익형 블로그 운영자들을 위한 키워드 분석 도구입니다.주제별로 수익성 높은 키워드를 식별하고, 블로그 콘텐츠와 광고의 매칭 효율성을 극대화하기 위해 개발되었습니다.

## 주요 기능
* **키워드 데이터 수집** : 네이버 검색 API와 광고 API를 사용하여 키워드 관련 데이터를 수집합니다.
* **데이터 전처리** : 월간 검색수가 200건 이상인 키워드를 필터링하고, 필요한 정보만을 추출합니다.
* **추가 정보 수집** : 각 키워드에 대한 전체 문서 수, 연관 검색어, 월별 검색 비율, 블로그 링크 등을 수집합니다.
* **경쟁-검색 균형 지수 계산** : 각 키워드의 수익성을 평가하기 위한 지표를 계산합니다.
* **시각화 및 시계열 분석** : 키워드의 월별 검색 추이를 시각화하고, 미래 검색 비율을 예측합니다.
* **엑셀 파일로 결과 출력** : 분석 결과를 엑셀 파일로 저장하고, 시각화된 데이터를 포함합니다.

## 사용 방법
* **API 인증 정보 설정** : api_credentials.py 파일에 네이버 검색 API와 광고 API의 인증 정보를 입력합니다.
* **키워드 입력** : 사용자가 분석하고자 하는 키워드를 입력합니다.
* **데이터 수집 및 분석 실행** : 스크립트를 실행하여 데이터를 수집하고 분석합니다.
* **결과 확인** : result.xlsx 파일을 통해 분석 결과와 시각화된 데이터를 확인합니다.

### 데이터 수집
#### 키워드 데이터 수집
```
resultdf = get_results(hintKeywords)
```
- get_results 함수는 네이버 검색 광고 API를 호출하여 키워드 관련 데이터를 수집합니다. 이 함수는 사용자가 입력한 hintKeywords를 받아 해당 키워드와 관련된 다양한 정보(예: 월간 검색수, 클릭률)를 JSON 형식으로 반환하고, 이를 판다스 데이터프레임으로 변환하여 resultdf에 저장합니다.


#### 추가 정보 수집
```
total_docs = get_total_documents(keyword)
suggest_keyword = get_google_suggestions(keyword)
```
- get_total_documents 함수는 네이버 검색 API를 사용하여 주어진 키워드에 대한 전체 문서 수를 검색하고 결과를 반환합니다. 이는 경쟁률을 평가하는 데 중요한 지표입니다.
- get_google_suggestions 함수는 Google의 자동 완성 API를 호출하여 주어진 키워드에 대한 관련 검색어 목록을 수집합니다. 이 정보는 사용자가 콘텐츠 계획을 수립할 때 유용합니다.

### 데이터 전처리 및 시각화
#### 데이터 필터링 및 정리
```
resultdf = resultdf[resultdf['relKeyword'].str.contains(hintKeywords)]
resultdf = resultdf[(resultdf['monthlyPcQcCnt'] + resultdf['monthlyMobileQcCnt']).fillna(0) >= 200]
```
- 수집된 데이터 중 키워드가 포함된 항목만 필터링하고, 월간 검색수가 200건 이상인 행만 유지합니다.

#### 데이터 시각화 및 분석
```
for index, item in enumerate(cell_data):
    # 데이터 준비 및 시각화 코드
```
matplotlib를 사용하여 각 키워드의 월별 검색 추이를 시각화합니다.


#### 선형 회귀 분석
```
model = LinearRegression()
model.fit(df[['DateInt']], df['Ratio'])
```
선형 회귀 모델을 사용하여 미래 검색 비율을 예측합니다.

<img width="100%" alt="image" src="https://github.com/rtae0/blog-revenue-keyword-analysis/assets/69848839/2f792558-3087-46a6-86be-b1ed5c5f3c39">

#### 시각화 결과 이미지 삽입
```
for index in range(1, ws.max_row):
    img = Image(img_path)
    ws.add_image(img, f"J{index + 1}")
```
각 키워드의 검색 추이 그래프를 이미지 형태로 엑셀 파일에 삽입합니다.



## 사용 라이브러리
```
pandas
matplotlib
requests
openpyxl
urllib
hashlib
datetime
```
