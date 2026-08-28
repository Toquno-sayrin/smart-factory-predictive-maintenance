# 🏭 Smart Factory Predictive Maintenance
> **AI4I 2020 제조 데이터를 활용한 스마트 팩토리 설비 고장 예측 및 실시간 관제 대시보드**

본 프로젝트는 제조 공정의 센서 데이터를 분석하여 설비 고장을 사전에 예측하고, 물리적 도메인 규칙(Domain Rules)을 결합해 관리자에게 직관적인 대응 가이드를 제공하는 데스크톱 애플리케이션입니다.

## ✨ 주요 기능 (Key Features)
* **탐색적 데이터 분석 (EDA):** 기준 데이터 요약, 센서 변수 간 상관관계(Heatmap) 및 세부 고장 유형 빈도 시각화
* **머신러닝 예측 (XGBoost):** 센서 데이터를 바탕으로 설비 고장 여부 학습 및 재현율(Recall) 중심의 모델 성능 평가
* **실시간 설비 관제:** 불량 확률이 높은 위험 설비를 스캔하고, 문제 센서 검출 및 즉각적인 대응 가이드라인(Rules) 제공

## 🛠 기술 스택 (Tech Stack)
* **Language:** Python 3.x
* **ML/Data:** XGBoost, Scikit-learn, Pandas, NumPy
* **GUI/Visualization:** Tkinter, Matplotlib, Seaborn


```
## 🚀 실행 방법 (How to Run)

**1. 패키지 설치**
bash
python -m pip install -r requirements.txt

**2. 애플리케이션 실행**
Bash
python src/dashboard.py
사용 안내: 프로그램이 열리면 좌측 상단의 열기 버튼을 눌러 ai4i2020.csv 파일을 선택한 뒤, [XGBoost 학습] 및 [전체 관제 스캔] 버튼을 차례로 클릭하여 분석을 진행


📂 프로젝트 구조 (Directory Structure)
Plaintext
smart-factory-predictive-maintenance/
├── 📂 assets/                 
│   └── fonts/                 # 대시보드 UI 폰트 리소스
├── 📂 data/
│   └── ai4i2020.csv           # 원본 및 전처리된 센서 데이터셋
├── 📂 notebooks/
│   └── 밀링머신_데이터분석.ipynb  # 데이터 탐색(EDA) 및 모델링 실험 주피터 노트북
├── 📂 src/
│   ├── dashboard.py           # Tkinter 기반 GUI 대시보드 메인 실행 파일
│   └── engine.py              # 데이터 로드 및 XGBoost 파이프라인 엔진
├── 📄 requirements.txt        # 프로젝트 구동에 필요한 패키지 목록
└── 📄 README.md               # 프로젝트 설명서


