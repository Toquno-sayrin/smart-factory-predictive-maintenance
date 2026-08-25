from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "ai4i2020.csv"
OUTPUT_DIR = PROJECT_ROOT / "artifacts" / "data_manipulation"
PAGES_DIR = PROJECT_ROOT / "docs"

NUMERIC_FEATURES = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
]
TARGET = "Machine failure"
SORT_COLUMN = "Tool wear [min]"


def add_sample_count(grouped_means: pd.DataFrame, counts: pd.Series) -> pd.DataFrame:
    """그룹별 평균표 앞에 표본 수를 추가한다."""
    result = grouped_means.copy()
    result.insert(0, "sample_count", counts)
    return result


def table_html(df: pd.DataFrame, *, index: bool = True) -> str:
    """보고서에서 공통으로 사용할 HTML 표를 만든다."""
    return df.to_html(
        index=index,
        classes="data-table",
        border=0,
        float_format=lambda value: f"{value:.6f}",
    )


def build_html_report(
    df: pd.DataFrame,
    numeric_df: pd.DataFrame,
    type_summary: pd.DataFrame,
    failure_summary: pd.DataFrame,
    sorted_ascending: pd.DataFrame,
    sorted_descending: pd.DataFrame,
) -> str:
    """기초통계와 데이터 조작 결과를 하나의 HTML 보고서로 구성한다."""
    overview = pd.DataFrame(
        {
            "dtype": df.dtypes.astype(str),
            "missing_count": df.isna().sum(),
        }
    )
    overview.index.name = "column"

    failure_distribution = pd.DataFrame(
        {
            "count": df[TARGET].value_counts().sort_index(),
            "percentage": (
                df[TARGET].value_counts(normalize=True).sort_index() * 100
            ),
        }
    )
    failure_distribution.index.name = TARGET

    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI4I 2020 EDA 데이터 조작 보고서</title>
<style>
  body {{ font-family: "Malgun Gothic", sans-serif; margin: 40px; color: #222; background: #f7f9fc; }}
  main {{ max-width: 1200px; margin: 0 auto; }}
  h1 {{ border-bottom: 3px solid #4472c4; padding-bottom: 10px; }}
  h2 {{ margin-top: 42px; color: #2e4a7d; border-left: 5px solid #4472c4; padding-left: 10px; }}
  h3 {{ margin-top: 28px; color: #374f78; }}
  .meta, .note {{ color: #5d6470; font-size: 14px; }}
  .cards {{ display: flex; gap: 16px; flex-wrap: wrap; margin: 20px 0; }}
  .card {{ background: #fff; border: 1px solid #dce3ef; border-radius: 8px; padding: 16px; min-width: 180px; }}
  .card strong {{ display: block; color: #2e4a7d; font-size: 22px; margin-top: 6px; }}
  .table-wrap {{ overflow-x: auto; background: #fff; border: 1px solid #dce3ef; border-radius: 8px; padding: 8px; }}
  table.data-table {{ border-collapse: collapse; width: 100%; }}
  .data-table th, .data-table td {{ border: 1px solid #ddd; padding: 7px 10px; font-size: 13px; text-align: right; white-space: nowrap; }}
  .data-table th {{ background: #4472c4; color: #fff; }}
  .data-table td:first-child, .data-table th:first-child {{ text-align: left; }}
  .insight {{ background: #eef4ff; border-left: 4px solid #4472c4; padding: 12px 16px; line-height: 1.7; }}
  code {{ background: #edf0f5; padding: 2px 5px; border-radius: 4px; }}
</style>
</head>
<body>
<main>
<h1>AI4I 2020 EDA 데이터 조작 보고서</h1>
<p class="meta">EDA 범위: 컬럼 추출·기초통계·전체 목록 저장·그룹 연산·오름차순/내림차순 정렬</p>

<div class="cards">
  <div class="card">전체 행<strong>{len(df):,}</strong></div>
  <div class="card">전체 컬럼<strong>{df.shape[1]}</strong></div>
  <div class="card">결측치<strong>{int(df.isna().sum().sum())}</strong></div>
  <div class="card">고장 비율<strong>{df[TARGET].mean() * 100:.2f}%</strong></div>
</div>

<h2>1. 전체 컬럼 목록과 데이터 품질</h2>
<p class="note">전체 컬럼의 데이터 타입과 결측치 개수를 확인했다.</p>
<div class="table-wrap">{table_html(overview)}</div>

<h2>2. 주요 수치형 컬럼 추출</h2>
<p class="note">추출한 5개 컬럼의 전체 10,000행은 <code>selected_numeric_features.csv</code>에 저장했으며 아래에는 처음 10행만 표시한다.</p>
<div class="table-wrap">{table_html(numeric_df.head(10), index=False)}</div>

<h2>3. 추출 컬럼 기초통계</h2>
<div class="table-wrap">{table_html(numeric_df.describe().T)}</div>

<h2>4. 그룹별 컬럼 집계</h2>
<h3>4.1 제품 품질 유형(Type)별 평균</h3>
<div class="table-wrap">{table_html(type_summary)}</div>
<h3>4.2 설비 정상·고장별 평균</h3>
<div class="table-wrap">{table_html(failure_summary)}</div>

<h2>5. 정렬 결과</h2>
<p class="note"><code>{SORT_COLUMN}</code>을 우선 기준으로, 동일한 값에서는 <code>Rotational speed [rpm]</code>을 보조 기준으로 정렬했다. 전체 결과는 각 CSV에 저장했다.</p>
<h3>5.1 오름차순 상위 10행</h3>
<div class="table-wrap">{table_html(sorted_ascending.head(10), index=False)}</div>
<h3>5.2 내림차순 상위 10행</h3>
<div class="table-wrap">{table_html(sorted_descending.head(10), index=False)}</div>

<h2>6. Machine failure 분포</h2>
<div class="table-wrap">{table_html(failure_distribution)}</div>

<h2>7. 제조설비 관점 해석</h2>
<div class="insight">
  <ul>
    <li>전체 컬럼에서 결측치가 발견되지 않아 이번 단계에서는 결측치 처리로 인한 표본 손실이 없다.</li>
    <li>정상 96.61%, 고장 3.39%로 클래스 불균형이 크므로 이후 예측에서 Accuracy만으로 성능을 판단하면 안 된다.</li>
    <li><code>Type</code>별 평균은 제품 품질 유형에 따른 운전 조건 차이를 비교하는 자료로 활용할 수 있다.</li>
    <li>정상·고장별 평균은 고장 집단에서 온도, 회전속도, 토크, 공구 마모가 어떻게 달라지는지 확인하는 출발점이다.</li>
    <li>공구 마모 기준 정렬 결과는 마모가 가장 적거나 큰 설비 관측값을 빠르게 점검하는 데 활용할 수 있다.</li>
  </ul>
</div>

<p class="meta">식별 컬럼과 고장 원인 결과 컬럼은 모델 입력 분석에서 제외했으며, 이 보고서에는 지도학습이나 시각화를 포함하지 않았다.</p>
</main>
</body>
</html>
"""


def main() -> None:
    """그룹 연산과 정렬을 수행하고 CSV 및 HTML 보고서를 저장한다."""
    df = pd.read_csv(DATA_PATH)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PAGES_DIR.mkdir(parents=True, exist_ok=True)

    # 분석 대상 컬럼을 추출하고 전체 목록을 별도 파일로 저장
    numeric_df = df[NUMERIC_FEATURES]
    numeric_df.to_csv(
        OUTPUT_DIR / "selected_numeric_features.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Type과 고장 여부별로 주요 수치형 변수의 평균과 표본 수를 계산
    type_summary = add_sample_count(
        df.groupby("Type")[NUMERIC_FEATURES].mean(),
        df.groupby("Type").size(),
    )
    failure_summary = add_sample_count(
        df.groupby(TARGET)[NUMERIC_FEATURES].mean(),
        df.groupby(TARGET).size(),
    )
    type_summary.to_csv(OUTPUT_DIR / "group_by_type.csv", encoding="utf-8-sig")
    failure_summary.to_csv(
        OUTPUT_DIR / "group_by_machine_failure.csv", encoding="utf-8-sig"
    )

    # 제조설비 상태 확인에 필요한 문맥 컬럼을 포함해 공구 마모 기준으로 정렬
    output_columns = ["Type", *NUMERIC_FEATURES, TARGET]
    sort_columns = [SORT_COLUMN, "Rotational speed [rpm]"]
    sorted_ascending = df[output_columns].sort_values(
        sort_columns, ascending=[True, True], kind="stable"
    )
    sorted_descending = df[output_columns].sort_values(
        sort_columns, ascending=[False, False], kind="stable"
    )
    sorted_ascending.to_csv(
        OUTPUT_DIR / "tool_wear_sorted_ascending.csv",
        index=False,
        encoding="utf-8-sig",
    )
    sorted_descending.to_csv(
        OUTPUT_DIR / "tool_wear_sorted_descending.csv",
        index=False,
        encoding="utf-8-sig",
    )

    report = build_html_report(
        df,
        numeric_df,
        type_summary,
        failure_summary,
        sorted_ascending,
        sorted_descending,
    )
    report_path = OUTPUT_DIR / "eda_report.html"
    pages_path = PAGES_DIR / "index.html"
    report_path.write_text(report, encoding="utf-8")
    pages_path.write_text(report, encoding="utf-8")

    print("[1] Type별 주요 변수 평균")
    print(type_summary)
    print("\n[2] Machine failure별 주요 변수 평균")
    print(failure_summary)
    print(f"\n[3] {SORT_COLUMN} 오름차순 상위 10행")
    print(sorted_ascending.head(10))
    print(f"\n[4] {SORT_COLUMN} 내림차순 상위 10행")
    print(sorted_descending.head(10))
    print(f"\nHTML 보고서: {report_path}")
    print(f"GitHub Pages 게시 파일: {pages_path}")


if __name__ == "__main__":
    main()
