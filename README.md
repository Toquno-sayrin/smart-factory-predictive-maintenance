# smart-factory-predictive-maintenance

AI4I 2020 제조 데이터를 활용한 스마트팩토리 설비 고장 예측 및 데이터 분석

## 실행

```powershell
python -m pip install -r requirements.txt
python main2.py
```

프로그램이 열리면 `열기` 버튼에서 `data/ai4i2020_preprocessed.csv`를 선택한 뒤
`XGBoost 학습`을 누릅니다.

## 폴더 구조

- `main2.py`: 애플리케이션 실행 진입점
- `dashboard.py`: Tkinter 대시보드 화면
- `engine.py`: 데이터 로드, 전처리 데이터 처리, 모델 학습
- `data/ai4i2020_preprocessed.csv`: 전처리된 AI4I 데이터셋
