# EDA 데이터 조작 산출물

## 목적

기초통계 다음 단계로 주요 컬럼의 전체 목록을 저장하고, 제조설비 관점의 그룹 비교와 정렬을 수행한 결과를 관리한다.

## 분석 순서

1. 주요 수치형 독립변수 5개를 추출한다.
2. 추출한 10,000행 전체 목록을 CSV로 저장한다.
3. `Type`별로 표본 수와 주요 변수 평균을 집계한다.
4. `Machine failure`별로 표본 수와 주요 변수 평균을 집계한다.
5. `Tool wear [min]`과 `Rotational speed [rpm]`을 기준으로 오름차순·내림차순 정렬한다.
6. 기초통계와 데이터 조작 결과를 하나의 HTML 보고서로 정리한다.

## 파일 설명

- `selected_numeric_features.csv`: 주요 수치형 독립변수 5개의 전체 10,000행
- `group_by_type.csv`: `Type`별 표본 수와 주요 변수 평균
- `group_by_machine_failure.csv`: 정상·고장별 표본 수와 주요 변수 평균
- `tool_wear_sorted_ascending.csv`: 공구 마모 및 회전속도 오름차순 전체 목록
- `tool_wear_sorted_descending.csv`: 공구 마모 및 회전속도 내림차순 전체 목록
- `eda_report.html`: 데이터 구조, 기초통계, 그룹 연산, 정렬 결과와 해석을 정리한 통합 보고서

모든 CSV는 `utf-8-sig`, HTML은 UTF-8로 저장한다. 결과는 `src/eda_data_manipulation.py`를 실행해 다시 생성할 수 있다. 동일한 HTML은 GitHub Pages 게시용 `docs/index.html`에도 저장한다.

## 해석 시 주의사항

- 그룹 평균은 집단의 전반적인 차이를 보여주지만 개별 고장의 원인을 직접 증명하지 않는다.
- `Machine failure` 그룹 비교는 탐색 목적이며, 고장 결과 컬럼을 향후 모델 입력으로 사용하지 않는다.
- 정렬 결과는 극단적인 공구 마모 관측값을 찾기 위한 목록이며 고장 판정 기준 자체는 아니다.
- 현재 단계에는 시각화와 지도학습 모델링이 포함되지 않는다.
