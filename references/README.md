# 출처 및 분석 근거

## 데이터 출처

- [UCI Machine Learning Repository: AI4I 2020 Predictive Maintenance Dataset](https://archive.ics.uci.edu/dataset/601/ai4i)
- [데이터셋 DOI: 10.24432/C5HS5C](https://doi.org/10.24432/C5HS5C)

UCI 설명에 따르면 AI4I 2020은 산업 현장의 예지보전 데이터를 반영하도록 만든 합성 데이터셋이다. 10,000개 관측값을 제공하며 공식 페이지에는 결측치가 없다고 명시돼 있다.

## 라이선스와 인용

- 라이선스: Creative Commons Attribution 4.0 International (`CC BY 4.0`)
- 권장 인용: *AI4I 2020 Predictive Maintenance Dataset* (2020), UCI Machine Learning Repository
- DOI: `10.24432/C5HS5C`

데이터를 재배포하거나 결과물에 사용할 때는 UCI 데이터셋과 DOI를 함께 표기한다.

## pandas 분석 근거

- [`pandas.read_csv`](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html): CSV 데이터 불러오기
- [`DataFrame.describe`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html): count, mean, std, 사분위수, min, max 산출
- [`DataFrame.groupby`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html): `Type`, `Machine failure` 그룹 연산
- [`DataFrame.sort_values`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html): 오름차순·내림차순 정렬

## 프로젝트 분석 원칙

- `Machine failure`을 예측 대상으로 사용한다.
- `UDI`, `Product ID`는 식별용이므로 모델 입력에서 제외한다.
- `TWF`, `HDF`, `PWF`, `OSF`, `RNF`는 고장 결과를 직접 나타내므로 데이터 누수를 방지하기 위해 모델 입력에서 제외한다.
- 고장 데이터가 적은 클래스 불균형 구조이므로 Accuracy보다 Precision, Recall, F1-score, AUPRC를 우선 평가한다.
- 그룹 평균과 정렬 결과는 탐색 근거이며 인과관계나 고장 판정 기준으로 단정하지 않는다.
