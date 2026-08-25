# GitHub Pages 게시 파일

## 목적

GitHub 저장소에서 EDA HTML 보고서를 웹페이지 형태로 바로 열람하기 위한 게시 폴더다.

## 파일 설명

- `index.html`: `artifacts/data_manipulation/eda_report.html`과 동일한 GitHub Pages 진입 파일
- `.nojekyll`: 정적 HTML을 Jekyll 변환 없이 게시하기 위한 설정 파일

`index.html`은 직접 수정하지 않고 `src/eda_data_manipulation.py`를 실행해 분석 결과와 함께 갱신한다.

## GitHub 설정

저장소의 **Settings → Pages → Build and deployment**에서 다음과 같이 선택한다.

- Source: `Deploy from a branch`
- Branch: `eda` (Pull Request 병합 후에는 `main` 권장)
- Folder: `/docs`

저장 후 Pages 배포가 끝나면 다음 주소에서 보고서를 확인할 수 있다.

`https://toquno-sayrin.github.io/smart-factory-predictive-maintenance/`
