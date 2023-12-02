# 🔮 수익형 블로그를 위한 키워드 분석

## 목차
1. [📌 프로젝트 개요](#-프로젝트-개요)
2. [🖍️ 사용 방법](#%EF%B8%8F-사용-방법)
3. [🛠️ 주요 기능](#%EF%B8%8F-주요-기능)
    1. [📝 데이터 수집](#-데이터-수집)
       * [키워드 데이터 수집](#키워드-데이터-수집)
       * [추가 정보 수집](#키워드-데이터-수집)
    2. [👀 데이터 전처리 및 시각화](#-데이터-전처리-및-시각화)
       * [데이터 필터링 및 정리](#데이터-필터링-및-정리)
       * [데이터 시각화 및 분석](#데이터-시각화-및-분석)
       * [선형 회귀 모델 훈련 및 미래 1년뒤 예측](#선형-회귀-모델-훈련-및-미래-1년뒤-예측)
       * [시각화 결과 이미지 삽입](#시각화-결과-이미지-삽입)
       * [결과 파일](#결과-파일)
4. [📋 사용 라이브러리](#-사용-라이브러리)
      
---

## 📌 프로젝트 개요
이 프로젝트는 구글 애드센스를 사용하는 수익형 블로그 운영자들을 위한 키워드 분석 도구입니다.주제별로 수익성 높은 키워드를 식별하고, 블로그 콘텐츠와 광고의 매칭 효율성을 극대화하기 위해 개발되었습니다.


## 🖍️ 사용 방법
* **API 인증 정보 설정** : api_credentials.py 파일에 네이버 검색 API와 광고 API의 인증 정보를 입력합니다.
* **키워드 입력** : 사용자가 분석하고자 하는 키워드를 입력합니다.
* **데이터 수집 및 분석 실행** : 스크립트를 실행하여 데이터를 수집하고 분석합니다.
* **결과 확인** : result.xlsx 파일을 통해 분석 결과와 시각화된 데이터를 확인합니다.


## 🛠️ 주요 기능
* **키워드 데이터 수집** : 네이버 검색 API와 광고 API를 사용하여 키워드 관련 데이터를 수집합니다.
* **데이터 전처리** : 월간 검색수가 200건 이상인 키워드를 필터링하고, 필요한 정보만을 추출합니다.
* **추가 정보 수집** : 각 키워드에 대한 전체 문서 수, 연관 검색어, 월별 검색 비율, 블로그 링크 등을 수집합니다.
* **경쟁-검색 균형 지수 계산** : 각 키워드의 수익성을 평가하기 위한 지표를 계산합니다.
* **시각화 및 시계열 분석** : 키워드의 월별 검색 추이를 시각화하고, 미래 검색 비율을 예측합니다.
* **엑셀 파일로 결과 출력** : 분석 결과를 엑셀 파일로 저장하고, 시각화된 데이터를 포함합니다.


## 📝 데이터 수집
### 키워드 데이터 수집
```
resultdf = get_results(hintKeywords)
```
- get_results 함수는 네이버 검색 광고 API를 호출하여 키워드 관련 데이터를 수집합니다. 이 함수는 사용자가 입력한 hintKeywords를 받아 해당 키워드와 관련된 다양한 정보(예: 월간 검색수, 클릭률)를 JSON 형식으로 반환하고, 이를 판다스 데이터프레임으로 변환하여 resultdf에 저장합니다.


### 추가 정보 수집
```
total_docs = get_total_documents(keyword)
suggest_keyword = get_google_suggestions(keyword)
```
- get_total_documents 함수는 네이버 검색 API를 사용하여 주어진 키워드에 대한 전체 문서 수를 검색하고 결과를 반환합니다. 이는 경쟁률을 평가하는 데 중요한 지표입니다.
- get_google_suggestions 함수는 Google의 자동 완성 API를 호출하여 주어진 키워드에 대한 관련 검색어 목록을 수집합니다. 이 정보는 사용자가 콘텐츠 계획을 수립할 때 유용합니다.



## 👀 데이터 전처리 및 시각화
### 데이터 필터링 및 정리
```
resultdf = resultdf[resultdf['relKeyword'].str.contains(hintKeywords)]
resultdf = resultdf[(resultdf['monthlyPcQcCnt'] + resultdf['monthlyMobileQcCnt']).fillna(0) >= 200]
```
- 수집된 데이터 중 키워드가 포함된 항목만 필터링하고, 월간 검색수가 200건 이상인 행만 유지합니다.



### 경쟁-검색 균형 지수 계산
```
resultdf['경쟁-검색 균형 지수'] = (resultdf['월간검색수(PC)'] + resultdf['월간검색수(모바일)']) / (resultdf['경쟁정도_ratio'] + 1)
resultdf = resultdf.sort_values(by='경쟁-검색 균형 지수', ascending=False)
```
* 각 키워드의 경쟁-검색 균형 지수를 계산합니다.
* 계산된 지수를 기준으로 데이터프레임을 정렬하여, 가장 수익성이 높은 키워드를 쉽게 식별할 수 있도록 합니다.
* 이러한 분석 과정은 사용자가 효과적인 키워드를 선정하고, 최적의 콘텐츠 전략을 수립하는 데 도움을 줍니다.



### 데이터 시각화 및 분석
```
for index, item in enumerate(cell_data):
    # JSON 데이터를 파싱하여 데이터프레임으로 변환
    results_data = json.loads(item)['results'][0]['data']
    title = json.loads(item)['results'][0]['title']
    periods = [datetime.strptime(d['period'], "%Y-%m-%d") for d in results_data]
    ratios = [d['ratio'] for d in results_data]
    df = pd.DataFrame({'Date': periods, 'Ratio': ratios})

    # 데이터 시각화
    fig, ax = plt.subplots(figsize=(15, 5))
    colors = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'orange']
    years = df['Date'].dt.year.unique()
    for i, year in enumerate(years):
        year_data = df[df['Date'].dt.year == year]
        ax.plot(year_data['Date'], year_data['Ratio'], label=f'{year}년도', color=colors[i % len(colors)])
    
    # 그래프 제목 설정 및 범례 추가
    ax.set_title(title + '에 대한 검색 관심도 추이')
    ax.legend(loc='upper left')

    plt.tight_layout()
    plt.savefig(f'{index}.png')
    plt.show()

```
* enumerate(cell_data)를 통해 각 키워드에 대한 월별 검색 데이터(cell_data)를 순회합니다.
* JSON 형식의 데이터를 파싱하여 각 키워드에 대한 검색 비율(ratio)과 해당 기간(period)을 추출합니다.
* 추출된 데이터를 판다스 데이터프레임으로 변환하여 시계열 데이터로 준비합니다.
* matplotlib를 사용하여 각 연도별로 검색 비율을 다른 색상의 선으로 그래프에 표시합니다. 이를 통해 시간에 따른 검색 추이를 명확하게 시각화합니다.
* 최종적으로 생성된 그래프는 .png 형식의 이미지 파일로 저장되고 화면에 표시됩니다.


### 선형 회귀 모델 훈련 및 미래 1년뒤 예측
```
df['DateInt'] = df['Date'].apply(lambda x: x.toordinal())
model = LinearRegression()
model.fit(df[['DateInt']], df['Ratio'])

last_date = df['Date'].iloc[-1]
future_dates = [last_date + timedelta(days=x) for x in range(1, 365)]
future_date_int = [d.toordinal() for d in future_dates]
future_df = pd.DataFrame({'DateInt': future_date_int})
future_predictions = model.predict(future_df)
```
* LinearRegression 모델을 훈련시켜, 기존 데이터에 기반한 미래 검색 비율을 예측합니다.
* 마지막 날짜부터 미래 1년간의 날짜를 생성하고, 이를 모델에 적용하여 미래 검색 비율을 예측합니다.
* 이 예측 모델은 블로그 운영자들이 미래의 검색 트렌드를 이해하고 적절한 콘텐츠 계획을 세우는 데 도움을 줍니다.

<img width="100%" alt="image" src="https://github.com/rtae0/blog-revenue-keyword-analysis/assets/69848839/2f792558-3087-46a6-86be-b1ed5c5f3c39">

### 시각화 결과 이미지 삽입
```
for index in range(1, ws.max_row):
    img = Image(img_path)
    ws.add_image(img, f"J{index + 1}")
```
* 각 키워드별로 생성된 시각화 그래프 이미지(.png 파일)를 엑셀 파일의 적절한 위치에 삽입하는 과정입니다.
* Image(img_path)는 저장된 그래프 이미지를 불러오고, ws.add_image(img, f"J{index + 1}")는 해당 이미지를 엑셀 시트의 지정된 셀 위치(J 열)에 추가합니다.

### 결과 파일
* result.xlsx
<img width="100%" alt="스크린샷 2023-12-03 오전 12 29 32" src="https://github.com/rtae0/blog-revenue-keyword-analysis/assets/69848839/39d15910-7c8c-4080-8b8b-7ad1ea6b4a51">

* Keyword: 분석된 키워드입니다. 이는 블로그 운영자가 타겟팅하는 주요 검색어입니다.
* 노출광고수: 해당 키워드의 광고가 몇 번 노출되었는지를 나타내는 수치입니다. 일반적으로 높을수록 해당 키워드의 광고 경쟁이 치열함을 의미합니다.
* 광고클릭률: 특정 키워드에 대한 광고 클릭 비율로, 사용자가 해당 키워드를 검색했을 때 광고를 클릭하는 경향을 나타냅니다.
* 연관검색어: 대상 키워드와 관련된 검색어 목록입니다. 이들은 키워드와 함께 자주 검색되는 용어들이며, 콘텐츠 계획을 세울 때 참고할 수 있습니다.
* 총문서수: 대상 키워드에 대해 인터넷 상에서 찾을 수 있는 총 문서(웹페이지)의 수입니다. 문서 수가 적을수록 해당 키워드에 대한 경쟁이 낮은 것으로 해석할 수 있습니다.
* 총검색량: 해당 키워드에 대한 월간 검색량을 나타냅니다. 높은 검색량은 키워드의 인기를 나타내며, 수익성 있는 키워드를 식별하는 데 중요한 지표가 될 수 있습니다.
* 경쟁정도_ratio: 총문서수 대비 월간 검색량의 비율로, 키워드의 경쟁 정도를 나타냅니다. 낮은 비율은 상대적으로 낮은 경쟁을 의미합니다.
* 경쟁-검색 균형 지수: 월간 검색량과 경쟁정도_ratio를 기반으로 계산된 지수로, 키워드의 경쟁력과 수익성을 종합적으로 평가합니다.
* 구글 상위 블로그: 해당 키워드로 검색했을 때 구글 검색 결과 상위에 위치하는 블로그 링크입니다. 이 정보는 SEO 최적화를 위한 참고자료로 사용될 수 있습니다.
* 월간 ratio: 월별 검색 관심도 추이를 나타내는 데이터입니다. 이는 JSON 형식으로 저장되며, 시계열 분석과 시각화에 사용됩니다.

위 정보는 블로그 운영자가 키워드 전략을 수립하고 블로그 SEO(검색엔진 최적화) 최적화를 진행하는 데 매우 유용합니다. 각 열의 데이터는 키워드의 인기도, 경쟁 상황, 관련 검색어 등을 분석하여 최적의 콘텐츠를 생성하고 수익을 극대화하는 데 도움을 줄 수 있습니다.

## 📋 사용 라이브러리
```
pandas
matplotlib
requests
openpyxl
urllib
hashlib
datetime
```
