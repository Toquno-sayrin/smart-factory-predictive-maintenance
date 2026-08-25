# Smart Factory Predictive Maintenance

AI4I 2020 제조 데이터를 활용해 설비 고장 특성을 탐색하고, 향후 지도학습으로 `Machine failure`을 예측하는 스마트팩토리 데이터 분석 프로젝트다.

## 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 문제 | 제조설비 고장을 사전에 식별할 수 있는 데이터 특성 파악 |
| 데이터 | AI4I 2020 Predictive Maintenance Dataset |
| 데이터 특성 | 산업 예지보전 환경을 반영한 합성 데이터, 10,000행 × 14열 |
| 예측 대상 | `Machine failure` (`0`: 정상, `1`: 고장) |
| 현재 단계 | EDA 기초통계·그룹 연산·정렬 완료 |
| 다음 단계 | 시각화 및 지도학습 모델링 |

실제 제조 현장에서는 고장 데이터가 정상 데이터보다 적어 단순 정확도만으로 모델을 평가하기 어렵다. 이 프로젝트는 데이터 구조와 고장 집단의 특성을 먼저 파악하고, 이후 클래스 불균형을 고려한 예측 모델을 만드는 것을 목표로 한다.

## 기술 스택

- Python 3.14
- pandas 3.0.5
- Git · GitHub
- HTML · Markdown

## 진행 과정

| 단계 | 작업 | 상태 | 상세 자료 |
|---|---|---|---|
| 1 | 데이터 구조·타입·결측치 확인 | 완료 | [기초통계 분석](artifacts/basic_statistics/README.md) |
| 2 | 주요 컬럼 추출, 평균·`describe()` 산출 | 완료 | [기초통계 산출물](artifacts/basic_statistics/) |
| 3 | 전체 목록 저장, 그룹 연산, 정렬 | 완료 | [데이터 조작 분석](artifacts/data_manipulation/README.md) |
| 4 | HTML EDA 보고서 생성 | 완료 | [HTML 보고서 파일](artifacts/data_manipulation/eda_report.html) |
| 5 | 시각화 3개 이상 및 결과 해석 | 예정 | 다음 작업 |
| 6 | 지도학습 고장 예측 및 모델 평가 | 예정 | 다음 작업 |

## 핵심 결과

### 데이터 품질과 클래스 분포

| 항목 | 결과 |
|---|---:|
| 전체 데이터 | 10,000행 × 14열 |
| 전체 결측치 | 0개 |
| 정상(`0`) | 9,661건 (96.61%) |
| 고장(`1`) | 339건 (3.39%) |

고장 비율이 3.39%로 낮아 클래스 불균형이 뚜렷하다. 이후 모델 평가에서는 Accuracy만 사용하지 않고 Precision, Recall, F1-score, AUPRC를 우선 확인한다.

### 정상·고장 집단 비교

| 변수 | 정상 평균 | 고장 평균 | 관찰 결과 |
|---|---:|---:|---|
| Air temperature [K] | 299.974 | 300.886 | 고장 집단이 약 0.912 K 높음 |
| Process temperature [K] | 309.996 | 310.290 | 고장 집단이 약 0.295 K 높음 |
| Rotational speed [rpm] | 1,540.260 | 1,496.487 | 고장 집단이 약 43.773 rpm 낮음 |
| Torque [Nm] | 39.630 | 50.168 | 고장 집단이 약 10.538 Nm 높음 |
| Tool wear [min] | 106.694 | 143.782 | 고장 집단이 약 37.088분 높음 |

고장 집단에서 토크와 공구 마모 평균이 특히 높고 회전속도 평균은 낮게 나타났다. 다만 이는 집단 평균의 차이이며 개별 고장의 원인이나 인과관계를 의미하지 않는다.

## 변수 구성과 데이터 누수 방지

| 역할 | 컬럼 | 처리 원칙 |
|---|---|---|
| 모델 입력 후보 | `Type`, 온도 2종, 회전속도, 토크, 공구 마모 | 설비 운전 조건을 나타내는 변수로 사용 |
| 예측 대상 | `Machine failure` | 정상·고장 이진 분류 |
| 식별 정보 | `UDI`, `Product ID` | 모델 입력에서 제외 |
| 고장 결과 정보 | `TWF`, `HDF`, `PWF`, `OSF`, `RNF` | 데이터 누수 방지를 위해 모델 입력에서 제외 |

변수의 공식 정의와 라이선스는 [출처 및 분석 근거](references/README.md)에 정리했다.

## 결과물 안내

- [기초통계 분석 설명과 CSV 목록](artifacts/basic_statistics/README.md)
- [그룹 연산·정렬 분석 설명과 CSV 목록](artifacts/data_manipulation/README.md)
- [통합 HTML EDA 보고서](artifacts/data_manipulation/eda_report.html)
- [공식 데이터 출처와 분석 근거](references/README.md)

## 프로젝트 구조

```text
smart-factory-predictive-maintenance/
├─ data/                             # 원본 데이터(로컬 관리)
├─ src/
│  ├─ eda_basic_statistics.py       # 컬럼 추출과 기초통계
│  └─ eda_data_manipulation.py      # 그룹 연산, 정렬, HTML 생성
├─ artifacts/
│  ├─ basic_statistics/             # 기초통계 CSV와 상세 설명
│  └─ data_manipulation/             # 그룹·정렬 CSV와 HTML 보고서
├─ docs/                             # GitHub Pages 게시 파일
├─ references/                       # 출처, 라이선스, 분석 근거
└─ README.md                         # 프로젝트 전체 흐름
```

각 산출물 폴더의 `README.md`에서 분석 방법, 파일 역할, 해석 시 주의사항을 확인할 수 있다.

## 실행 방법

### 1. 데이터 준비

[UCI 공식 데이터 페이지](https://archive.ics.uci.edu/dataset/601/ai4i)에서 `ai4i2020.csv`를 내려받아 다음 경로에 둔다.

```text
data/ai4i2020.csv
```

### 2. 의존성 설치

```powershell
python -m pip install pandas
```

### 3. 분석 실행

```powershell
python src\eda_basic_statistics.py
python src\eda_data_manipulation.py
```

첫 번째 스크립트는 기초통계 결과를 생성한다. 두 번째 스크립트는 그룹·정렬 결과와 HTML 보고서를 생성한다.

## 다음 계획

1. 주요 변수 분포와 고장 관계를 보여주는 시각화 3개 이상 작성
2. 제조설비 관점에서 각 시각화 결과 해석
3. 학습·평가 데이터 분리와 범주형 변수 처리
4. 클래스 불균형을 고려한 지도학습 모델 비교
5. Precision, Recall, F1-score, AUPRC 중심의 최종 평가

## 데이터 출처

- [UCI Machine Learning Repository — AI4I 2020 Predictive Maintenance Dataset](https://archive.ics.uci.edu/dataset/601/ai4i)
- [Dataset DOI: 10.24432/C5HS5C](https://doi.org/10.24432/C5HS5C)
- License: Creative Commons Attribution 4.0 International (`CC BY 4.0`)
