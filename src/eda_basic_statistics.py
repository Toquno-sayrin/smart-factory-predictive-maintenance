from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "ai4i2020.csv"
OUTPUT_DIR = PROJECT_ROOT / "artifacts" / "basic_statistics"

NUMERIC_FEATURES = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
]
TARGET = "Machine failure"


def main() -> None:
    """AI4I 데이터의 EDA 1단계 기초통계를 출력하고 저장한다."""
    df = pd.read_csv(DATA_PATH)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 데이터 구조와 품질 확인
    print("[1] 데이터 크기")
    print(df.shape)
    print("\n[2] 전체 컬럼명")
    print(df.columns.tolist())
    print("\n[3] 데이터 타입")
    print(df.dtypes)
    print("\n[4] 컬럼별 결측치 개수")
    print(df.isna().sum())

    # 요청된 주요 수치형 독립변수만 선택
    numeric_df = df[NUMERIC_FEATURES]
    means = numeric_df.mean()
    summary = numeric_df.describe()

    print("\n[5] 주요 수치형 독립변수 평균")
    print(means)
    print("\n[6] 주요 수치형 독립변수 기초통계")
    print(summary)

    # 정상/고장 건수와 전체 대비 비율 산출
    failure_counts = df[TARGET].value_counts().sort_index()
    failure_distribution = pd.DataFrame(
        {
            "count": failure_counts,
            "ratio": failure_counts / len(df),
            "percentage": failure_counts / len(df) * 100,
        }
    )
    failure_distribution.index.name = TARGET

    print("\n[7] Machine failure 분포")
    print(failure_distribution)

    # 후속 분석에서 바로 활용할 수 있도록 표 형태로 저장
    summary_by_feature = summary.T
    summary_by_feature.index.name = "feature"
    summary_by_feature.to_csv(
        OUTPUT_DIR / "numeric_summary.csv", encoding="utf-8-sig"
    )
    failure_distribution.to_csv(
        OUTPUT_DIR / "machine_failure_distribution.csv", encoding="utf-8-sig"
    )

    data_overview = pd.DataFrame(
        {
            "dtype": df.dtypes.astype(str),
            "missing_count": df.isna().sum(),
        }
    )
    data_overview.index.name = "column"
    data_overview.to_csv(OUTPUT_DIR / "data_overview.csv", encoding="utf-8-sig")


if __name__ == "__main__":
    main()
