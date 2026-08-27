import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import seaborn as sns

from engine import AutoEverSmartFactoryEngine

FONT_FAMILY = "Pretendard"
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


class AutoEverDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("현대오토에버 SW스쿨 - 스마트 팩토리 예지보전 시스템")
        self.root.geometry("1450x900")
        self.root.config(bg="#F4F6F9")

        self.engine = AutoEverSmartFactoryEngine()
        self.setup_styles()
        self.create_main_layout()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.layout('TNotebook.Tab', [
            ('Notebook.tab', {
                'sticky': 'nswe',
                'children': [
                    ('Notebook.padding', {
                        'sticky': 'nswe',
                        'children': [
                            ('Notebook.label', {'sticky': 'nswe'})
                        ]
                    })
                ]
            })
        ])

        style.configure('TNotebook', background='#F4F6F9', borderwidth=0)
        style.configure('TNotebook.Tab', font=(FONT_FAMILY, 10, 'bold'), padding=[15, 10], background='#E2E8F0',
                        foreground='#334155')

        style.map('TNotebook.Tab',
                  background=[('selected', '#0A192F')],
                  foreground=[('selected', '#FFFFFF')],
                  expand=[('selected', [0, 0, 0, 0])],
                  padding=[('selected', [15, 10])],
                  focuscolor=[('selected', '#0A192F')])

        style.configure('TEntry', padding=5, font=(FONT_FAMILY, 10))
        style.configure('TCombobox', padding=5, font=(FONT_FAMILY, 10))
        style.configure("Treeview.Heading", font=(FONT_FAMILY, 9, "bold"), background="#E2E8F0", foreground="#0A192F")
        style.configure("Treeview", font=(FONT_FAMILY, 9), rowheight=24)

    def create_main_layout(self):
        banner_frame = tk.Frame(self.root, bg="#0A192F", height=60)
        banner_frame.pack(side="top", fill="x")
        banner_frame.pack_propagate(False)

        tk.Label(banner_frame, text="HYUNDAI AUTOEVER  |  Smart Factory Predictive Maintenance System",
                 font=(FONT_FAMILY, 12, "bold"), fg="#38BDF8", bg="#0A192F").pack(side="left", padx=20)
        tk.Label(banner_frame, text="제조 AI 분석 대시보드", font=(FONT_FAMILY, 10), fg="#94A3B8", bg="#0A192F").pack(
            side="right", padx=20)

        main_container = tk.Frame(self.root, bg="#F4F6F9")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_container, width=330, bg="#FFFFFF", relief="solid", bd=1)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        left_frame.pack_propagate(False)

        tk.Label(left_frame, text="1. 데이터 및 문제 정의", font=(FONT_FAMILY, 12, "bold"), bg="#FFFFFF", fg="#0A192F",
                 anchor="w").pack(fill="x", padx=15, pady=(20, 5))

        file_frame = tk.Frame(left_frame, bg="#FFFFFF")
        file_frame.pack(fill="x", padx=15, pady=5)
        self.file_entry = ttk.Entry(file_frame, font=(FONT_FAMILY, 10), width=22)
        self.file_entry.pack(side="left", padx=(0, 5), ipady=3)
        ttk.Button(file_frame, text="열기", width=7, command=self.load_file_action, takefocus=0).pack(side="right",
                                                                                                    ipady=2)

        tk.Label(left_frame, text="타깃 변수 (Target)", font=(FONT_FAMILY, 10, "bold"), bg="#FFFFFF", fg="#64748B",
                 anchor="w").pack(fill="x", padx=15, pady=(10, 5))
        self.target_box = ttk.Combobox(left_frame, values=["Machine failure (0:정상/1:고장)"], state="readonly",
                                       font=(FONT_FAMILY, 10), takefocus=0)
        self.target_box.current(0)
        self.target_box.pack(fill="x", padx=15, ipady=3)

        tk.Label(left_frame, text="2. 학습/검증 설정", font=(FONT_FAMILY, 12, "bold"), bg="#FFFFFF", fg="#0A192F",
                 anchor="w").pack(fill="x", padx=15, pady=(15, 5))
        setting_frame = tk.Frame(left_frame, bg="#FFFFFF")
        setting_frame.pack(fill="x", padx=15, pady=5)
        setting_frame.columnconfigure(0, weight=1)
        setting_frame.columnconfigure(1, weight=1)

        tk.Label(setting_frame, text="테스트 비율", bg="#FFFFFF", font=(FONT_FAMILY, 10, "bold"), fg="#334155").grid(row=0,
                                                                                                                column=0,
                                                                                                                sticky="w",
                                                                                                                pady=5)
        self.test_ratio = ttk.Combobox(setting_frame, values=["0.2", "0.25", "0.3"], width=9, state="readonly",
                                       font=(FONT_FAMILY, 10), takefocus=0)
        self.test_ratio.current(0)
        self.test_ratio.grid(row=0, column=1, sticky="e", pady=5, ipady=2)

        tk.Label(setting_frame, text="교차검증", bg="#FFFFFF", font=(FONT_FAMILY, 10, "bold"), fg="#334155").grid(row=1,
                                                                                                              column=0,
                                                                                                              sticky="w",
                                                                                                              pady=5)
        self.cv_box = ttk.Combobox(setting_frame, values=["None", "3-Fold", "5-Fold", "10-Fold"], width=9,
                                   state="readonly", font=(FONT_FAMILY, 10), takefocus=0)
        self.cv_box.current(2)
        self.cv_box.grid(row=1, column=1, sticky="e", pady=5, ipady=2)

        btn_frame = tk.Frame(left_frame, bg="#FFFFFF")
        btn_frame.pack(fill="x", padx=15, pady=(15, 10))
        tk.Button(btn_frame, text="XGBoost 학습", font=(FONT_FAMILY, 10, "bold"), bg="#0052CC", fg="#FFFFFF", width=12,
                  height=2, command=self.start_training, takefocus=0, bd=0).pack(side="left", padx=2)
        tk.Button(btn_frame, text="전체 관제 스캔", font=(FONT_FAMILY, 10, "bold"), bg="#0EA5E9", fg="#FFFFFF", width=10,
                  height=2, command=self.start_prediction, takefocus=0, bd=0).pack(side="right", padx=2)

        rule_frame = tk.LabelFrame(left_frame, text=" 도메인 물리 규칙 (AI4I Rules) ", font=(FONT_FAMILY, 9, "bold"),
                                   bg="#FFFFFF", fg="#0A192F", padx=10, pady=5)
        rule_frame.pack(fill="x", padx=15, pady=(5, 10))

        rules_text = (
            "• TWF (공구마모): 마모도 ≥ 200 min\n"
            "• HDF (방열실패): 온도차 < 8.6K & RPM < 1380\n"
            "• PWF (전력이상): 전력 < 3.5kW or > 9.0kW\n"
            "• OSF (과부하): 마모도 × 토크 한계 초과"
        )
        tk.Label(rule_frame, text=rules_text, font=(FONT_FAMILY, 8), fg="#334155", bg="#FFFFFF", justify="left").pack(
            anchor="w", pady=2)

        warning_text = "※ 데이터 불균형: 정확도보다 '재현율(Recall)' 중점 모니터링"
        tk.Label(left_frame, text=warning_text, font=(FONT_FAMILY, 8), fg="#EF4444", bg="#FFFFFF", justify="left",
                 anchor="w").pack(side="bottom", fill="x", padx=15, pady=(0, 15))

        right_parent = tk.Frame(main_container, bg="#F4F6F9")
        right_parent.pack(side="right", fill="both", expand=True)

        self.notebook = ttk.Notebook(right_parent)
        self.notebook.pack(fill="both", expand=True)

        self.tab_input = tk.Frame(self.notebook, bg="#F4F6F9")
        self.tab_preprocess = tk.Frame(self.notebook, bg="#FFFFFF")
        self.tab_eda = tk.Frame(self.notebook, bg="#F4F6F9")
        self.tab_eval = tk.Frame(self.notebook, bg="#FFFFFF")
        self.tab_predict = tk.Frame(self.notebook, bg="#F4F6F9")

        self.notebook.add(self.tab_input, text=" 기준 데이터 분석 ")
        self.notebook.add(self.tab_preprocess, text=" 전처리 및 파이프라인 ")
        self.notebook.add(self.tab_eda, text=" 시각화(EDA) 및 의사결정 ")
        self.notebook.add(self.tab_eval, text=" 모델 평가 ")
        self.notebook.add(self.tab_predict, text=" 실시간 설비 관제 (모니터링) ")

        self.build_initial_input_tab()
        self.build_preprocess_tab_content()
        self.build_eda_tab_content()
        self.build_predict_tab_content()

    def build_initial_input_tab(self):
        for widget in self.tab_input.winfo_children(): widget.destroy()
        tk.Label(self.tab_input, text="[ 기준 데이터 분석 대기 중 ]", font=(FONT_FAMILY, 15, "bold"), fg="#0A192F",
                 bg="#F4F6F9").pack(pady=(40, 10), anchor="w", padx=30)
        tk.Label(self.tab_input, text="좌측 패널의 [열기] 버튼을 눌러 분석할 CSV 파일을 선택해주세요.", font=(FONT_FAMILY, 12), fg="#64748B",
                 bg="#F4F6F9").pack(anchor="w", padx=30)

    def load_file_action(self):
        file_path = filedialog.askopenfilename(
            title="CSV 파일 선택",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            try:
                self.engine.load_data(file_path)
                self.build_input_tab_content()
                self.build_preprocess_tab_content()
                self.build_eda_tab_content()
                messagebox.showinfo("데이터 연동", f"파일이 성공적으로 로드되었습니다.\n({file_path})")
            except Exception as e:
                messagebox.showerror("에러", f"파일을 읽는 중 오류 발생:\n{str(e)}")

    def start_training(self):
        if self.engine.df is None:
            messagebox.showwarning("경고", "먼저 [열기] 버튼을 눌러 CSV 파일을 선택해주세요!")
            return
        try:
            test_size_val = float(self.test_ratio.get())
            cv_val = self.cv_box.get()
            results = self.engine.run_pipeline(test_size=test_size_val, cv_setting=cv_val)
            self.build_evaluation_tab_content(results)
            messagebox.showinfo("학습 완료", "XGBoost 모델 학습 및 평가가 완료되었습니다!")
            self.notebook.select(self.tab_eval)
        except Exception as e:
            messagebox.showerror("에러", f"학습 중 오류 발생:\n{str(e)}")

    def start_prediction(self):
        if not self.engine.is_trained:
            messagebox.showwarning("경고", "먼저 [XGBoost 학습] 버튼을 눌러 모델을 학습시켜주세요!")
            return
        self.notebook.select(self.tab_predict)
        self.run_realtime_prediction()

    def build_input_tab_content(self):
        for widget in self.tab_input.winfo_children(): widget.destroy()

        df_load = self.engine.df
        total_len = len(df_load)
        fail_len = df_load['Machine failure'].sum()
        normal_len = total_len - fail_len
        missing_len = df_load.isnull().sum().sum()

        tk.Label(self.tab_input, text="[ 기준 데이터 요약 및 시각화 ]", font=(FONT_FAMILY, 15, "bold"), fg="#0A192F",
                 bg="#F4F6F9").pack(pady=(20, 10), anchor="w", padx=30)

        kpi_frame = tk.Frame(self.tab_input, bg="#F4F6F9")
        kpi_frame.pack(fill="x", padx=25, pady=5)

        def make_card(parent, title, value, subtext, color):
            card = tk.Frame(parent, bg="#FFFFFF", relief="solid", bd=1)
            card.pack(side="left", fill="both", expand=True, padx=5)
            tk.Label(card, text=title, font=(FONT_FAMILY, 10, "bold"), fg="gray", bg="#FFFFFF").pack(anchor="w",
                                                                                                     padx=15,
                                                                                                     pady=(12, 2))
            tk.Label(card, text=value, font=(FONT_FAMILY, 16, "bold"), fg=color, bg="#FFFFFF").pack(anchor="w", padx=15,
                                                                                                    pady=0)
            tk.Label(card, text=subtext, font=(FONT_FAMILY, 9), fg="gray", bg="#FFFFFF").pack(anchor="w", padx=15,
                                                                                              pady=(0, 12))

        make_card(kpi_frame, "전체 레코드", f"{total_len:,}", "분석 가능 100% (10,000건)", "#1E293B")
        make_card(kpi_frame, "정상 데이터", f"{normal_len:,}", f"{(normal_len / (total_len or 1) * 100):.1f}%", "#16A34A")
        make_card(kpi_frame, "이상(고장) 데이터", f"{fail_len:,}", f"{(fail_len / (total_len or 1) * 100):.1f}% (Minority)",
                  "#EF4444")
        make_card(kpi_frame, "결측 레코드", f"{missing_len:,}", "결측치 0건 (Clean Data)", "#0A192F")

        table_frame = tk.Frame(self.tab_input, bg="#FFFFFF", bd=1, relief="solid")
        table_frame.pack(fill="both", expand=True, padx=30, pady=10)
        tk.Label(table_frame, text="📋 상위 데이터 미리보기", font=(FONT_FAMILY, 11, "bold"), bg="#FFFFFF").pack(anchor="w",
                                                                                                       padx=10, pady=5)

        tree_container = tk.Frame(table_frame, bg="#FFFFFF")
        tree_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        columns = ("UDI", "Type", "Air Temp", "Process Temp", "RPM", "Torque", "Tool Wear", "Failure")
        tree = ttk.Treeview(tree_container, columns=columns, show="headings", height=10)

        scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=90, anchor="center")

        for row_index, r in df_load.iterrows():
            if 'Type' in r.index:
                type_value = r['Type']
            else:
                type_value = next((column[-1] for column in ('Type_H', 'Type_L', 'Type_M')
                                   if column in r.index and r[column] == 1), 'Unknown')
            udi_value = r.get('UDI', row_index + 1)
            fail_str = "1 (고장)" if r['Machine failure'] == 1 else "0 (정상)"
            tree.insert("", "end", values=(udi_value, type_value, r['Air temperature [K]'], r['Process temperature [K]'],
                                           r['Rotational speed [rpm]'], r['Torque [Nm]'], r['Tool wear [min]'],
                                           fail_str))

    def build_preprocess_tab_content(self):
        for widget in self.tab_preprocess.winfo_children(): widget.destroy()

        tk.Label(self.tab_preprocess, text="[ 데이터 전처리 및 파이프라인 요약 ]", font=(FONT_FAMILY, 15, "bold"), fg="#0A192F",
                 bg="#FFFFFF").pack(pady=(15, 10), anchor="w", padx=30)

        summary_frame = tk.Frame(self.tab_preprocess, bg="#F8FAFC", bd=1, relief="solid")
        summary_frame.pack(fill="x", padx=30, pady=5, ipady=5)

        df_load = self.engine.df
        if df_load is None:
            texts = ["데이터를 먼저 열어주세요."]
        else:
            missing_len = int(df_load.isnull().sum().sum())
            identifier_status = "있음 (학습 시 제외)" if {'UDI', 'Product ID'} & set(df_load.columns) else "없음 (전처리 파일)"
            type_status = "원-핫 인코딩 완료" if {'Type_H', 'Type_L', 'Type_M'}.issubset(df_load.columns) else "Type 컬럼 자동 인코딩"
            texts = [
                f"✅ 1. 결측치 검증: {missing_len:,}건",
                f"✅ 2. 식별자 컬럼: {identifier_status}",
                f"✅ 3. 범주형 컬럼: {type_status}",
                "✅ 4. 수치형 컬럼: 학습 시 StandardScaler 적용"
            ]
        for t in texts:
            tk.Label(summary_frame, text=t, font=(FONT_FAMILY, 10, "bold"), fg="#0052CC", bg="#F8FAFC").pack(anchor="w",
                                                                                                             padx=20,
                                                                                                             pady=4)

        table_frame = tk.Frame(self.tab_preprocess, bg="#FFFFFF", bd=1, relief="solid")
        table_frame.pack(fill="both", expand=True, padx=30, pady=10)

        tk.Label(table_frame, text="📋 AI4I 2020 데이터셋 주요 컬럼 정의", font=(FONT_FAMILY, 11, "bold"), fg="#0A192F",
                 bg="#FFFFFF").pack(anchor="w", padx=10, pady=8)

        col_container = tk.Frame(table_frame, bg="#FFFFFF")
        col_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        cols = ("컬럼명 (Feature)", "데이터 타입", "설명 및 단위")
        tree_col = ttk.Treeview(col_container, columns=cols, show="headings", height=8)

        for col in cols:
            tree_col.heading(col, text=col)
            tree_col.column(col, width=200, anchor="center")
        tree_col.column("설명 및 단위", width=450, anchor="w")

        scrollbar_col = ttk.Scrollbar(col_container, orient="vertical", command=tree_col.yview)
        tree_col.configure(yscrollcommand=scrollbar_col.set)

        tree_col.pack(side="left", fill="both", expand=True)
        scrollbar_col.pack(side="right", fill="y")

        column_descriptions = [
            ("UDI", "고유 번호 (Integer)", "1부터 10,000까지의 데이터 순번 식별자"),
            ("Product ID", "문자열 (String)", "품질 등급(L, M, H)과 제품 일련번호 조합"),
            ("Type", "범주형 (Categorical)", "제품 품질 등급 (L: Low 50%, M: Medium 30%, H: High 20%)"),
            ("Air temperature [K]", "수치형 (Float)", "대기 온도 (Kelvin 단위, 약 298K 내외)"),
            ("Process temperature [K]", "수치형 (Float)", "공정 작동 온도 (대기 온도보다 항상 높음)"),
            ("Rotational speed [rpm]", "수치형 (Integer)", "스핀들 회전 속도 (분당 회전수)"),
            ("Torque [Nm]", "수치형 (Float)", "회전축에 걸리는 토크(힘) (Nm 단위)"),
            ("Tool wear [min]", "수치형 (Integer)", "공구 마모 시간 (분 단위, 200분 이상 시 마모 한계)"),
            ("Machine failure", "타깃 (Binary)", "설비 고장 여부 (0: 정상, 1: 고장 / 불균형 약 3.4%)")
        ]

        if self.engine.df is not None:
            available_columns = set(self.engine.df.columns)
            for item in column_descriptions:
                if item[0] in available_columns or item[0] in {"UDI", "Product ID", "Type"}:
                    tree_col.insert("", "end", values=item)

    def build_eda_tab_content(self):
        for widget in self.tab_eda.winfo_children(): widget.destroy()

        df_load = self.engine.df
        total_len = len(df_load) if df_load is not None else 0
        fail_len = int(df_load['Machine failure'].sum()) if df_load is not None else 0
        missing_len = int(df_load.isnull().sum().sum()) if df_load is not None else 0
        if df_load is not None and 'Type' in df_load.columns:
            type_summary = ' | '.join(f'{key}: {value / total_len:.0%}'
                                      for key, value in df_load['Type'].value_counts().items())
        elif df_load is not None:
            type_summary = ' | '.join(f'{column[-1]}: {df_load[column].mean():.0%}'
                                      for column in ('Type_L', 'Type_M', 'Type_H')
                                      if column in df_load.columns)
        else:
            type_summary = '-'

        top_frame = tk.Frame(self.tab_eda, bg="#F4F6F9")
        top_frame.pack(fill="x", padx=15, pady=(15, 5))

        tk.Label(top_frame, text="Overview & Analytics", font=(FONT_FAMILY, 15, "bold"), fg="#0A192F",
                 bg="#F4F6F9").pack(side="left", padx=5)

        kpi_container = tk.Frame(self.tab_eda, bg="#F4F6F9")
        kpi_container.pack(fill="x", padx=15, pady=5)

        def make_kpi_card(parent, title, val, sub, is_good=True):
            card = tk.Frame(parent, bg="#FFFFFF", relief="solid", bd=1, height=75)
            card.pack(side="left", fill="both", expand=True, padx=5)
            card.pack_propagate(False)
            tk.Label(card, text=title, font=(FONT_FAMILY, 9, "bold"), fg="#64748B", bg="#FFFFFF").pack(anchor="w",
                                                                                                       padx=15,
                                                                                                       pady=(8, 2))
            tk.Label(card, text=val, font=(FONT_FAMILY, 13, "bold"), fg="#0A192F", bg="#FFFFFF").pack(anchor="w",
                                                                                                      padx=15)
            color = "#10B981" if is_good else "#EF4444"
            tk.Label(card, text=sub, font=(FONT_FAMILY, 8, "bold"), fg=color, bg="#FFFFFF").pack(anchor="w", padx=15,
                                                                                                 pady=(2, 5))

        make_kpi_card(kpi_container, "전체 공정 레코드", f"{total_len:,} 건", f"결측치 {missing_len:,}건",
                      is_good=missing_len == 0)
        make_kpi_card(kpi_container, "누적 고장 발생 (Failure)", f"{fail_len:,} 건",
                      f"전체의 {fail_len / (total_len or 1):.2%}", is_good=False)
        make_kpi_card(kpi_container, "설비 등급 (Type)", type_summary or "-", "현재 데이터 분포", is_good=True)
        mode_counts = {mode: int(df_load[mode].sum()) for mode in ('HDF', 'OSF', 'PWF', 'TWF', 'RNF')
                       if df_load is not None and mode in df_load.columns}
        if mode_counts:
            top_mode, top_count = max(mode_counts.items(), key=lambda item: item[1])
            mode_text = f"{top_mode} ({top_count:,}건)"
            mode_subtext = "고장 원인 컬럼 기준"
        else:
            mode_text = "전처리로 제거됨"
            mode_subtext = "Machine failure만 사용"
        make_kpi_card(kpi_container, "주요 고장 원인", mode_text, mode_subtext, is_good=False)

        mid_frame = tk.Frame(self.tab_eda, bg="#F4F6F9")
        mid_frame.pack(fill="both", expand=True, padx=15, pady=(5, 5))

        stats_frame = tk.Frame(mid_frame, bg="#FFFFFF", relief="solid", bd=1)
        stats_frame.pack(side="left", fill="both", expand=True, padx=(5, 5))

        tk.Label(stats_frame, text="📋 주요 센서 기초 통계 요약", font=(FONT_FAMILY, 11, "bold"), fg="#0052CC", bg="#FFFFFF").pack(
            anchor="w", padx=15, pady=(10, 5))

        cols = ("센서 (Feature)", "최솟값 (Min)", "평균치 (Mean)", "최댓값 (Max)")
        stats_tree = ttk.Treeview(stats_frame, columns=cols, show="headings", height=5)
        for c in cols: stats_tree.heading(c, text=c)
        stats_tree.column("센서 (Feature)", width=150, anchor="w")
        stats_tree.column("최솟값 (Min)", width=100, anchor="center")
        stats_tree.column("평균치 (Mean)", width=100, anchor="center")
        stats_tree.column("최댓값 (Max)", width=100, anchor="center")
        stats_tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        sensor_columns = [
            ("Air Temperature [K]", "Air temperature [K]"),
            ("Process Temp [K]", "Process temperature [K]"),
            ("Rotational Speed [rpm]", "Rotational speed [rpm]"),
            ("Torque [Nm]", "Torque [Nm]"),
            ("Tool Wear [min]", "Tool wear [min]")
        ]
        if df_load is not None:
            for label, column in sensor_columns:
                values = df_load[column]
                stats_tree.insert("", "end", values=(label, f"{values.min():.2f}",
                                                       f"{values.mean():.2f}", f"{values.max():.2f}"))

        chart_frame = tk.Frame(mid_frame, bg="#FFFFFF", relief="solid", bd=1)
        chart_frame.pack(side="right", fill="both", expand=True, padx=(5, 5))

        fig_bar, ax_bar = plt.subplots(figsize=(5, 2.3))
        f_modes = ['HDF\n(방열)', 'OSF\n(과부하)', 'PWF\n(전력)', 'TWF\n(마모)', 'RNF\n(우발)']
        f_counts = [int(df_load[mode].sum()) if df_load is not None and mode in df_load.columns else 0
                for mode in ('HDF', 'OSF', 'PWF', 'TWF', 'RNF')]
        colors = ['#0A192F', '#1E3A8A', '#0052CC', '#3B82F6', '#93C5FD']

        bars = ax_bar.bar(f_modes, f_counts, color=colors, width=0.55)
        ax_bar.set_title("세부 고장 유형(Failure Modes) 발생 빈도", fontsize=10, fontweight="bold")
        ax_bar.grid(axis='y', linestyle='--', alpha=0.3)
        ax_bar.spines['top'].set_visible(False)
        ax_bar.spines['right'].set_visible(False)
        for b in bars:
            ax_bar.text(b.get_x() + b.get_width() / 2., b.get_height() + 2, f'{b.get_height()}건', ha='center',
                        va='bottom', fontsize=8, fontweight='bold', color='#1E293B')

        plt.tight_layout()
        canvas_bar = FigureCanvasTkAgg(fig_bar, master=chart_frame)
        canvas_bar.draw()
        canvas_bar.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

        bot_frame = tk.Frame(self.tab_eda, bg="#F4F6F9")
        bot_frame.pack(fill="both", expand=True, padx=15, pady=(5, 10))

        hm_frame = tk.Frame(bot_frame, bg="#FFFFFF", relief="solid", bd=1)
        hm_frame.pack(side="left", fill="both", expand=True, padx=(5, 5))

        fig_hm, ax_hm = plt.subplots(figsize=(5, 2.3))
        if self.engine.df is not None:
            cols_hm = ['Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]',
                       'Tool wear [min]', 'Machine failure']
            corr = self.engine.df[cols_hm].corr()
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", cbar=False, ax=ax_hm, annot_kws={"size": 8})
            ax_hm.set_title("핵심 변수 상관관계 (Heatmap)", fontsize=10, fontweight="bold", pad=5)
            short_cols = ['Air', 'Process', 'RPM', 'Torque', 'Wear', 'Failure']
            ax_hm.set_xticklabels(short_cols, rotation=0, fontsize=8)
            ax_hm.set_yticklabels(short_cols, rotation=0, fontsize=8)
        else:
            ax_hm.text(0.5, 0.5, "데이터를 먼저 열어주세요", ha='center', va='center', fontsize=10, color='gray')
            ax_hm.axis('off')

        plt.tight_layout()
        canvas_hm = FigureCanvasTkAgg(fig_hm, master=hm_frame)
        canvas_hm.draw()
        canvas_hm.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

        guide_frame = tk.Frame(bot_frame, bg="#FFFFFF", relief="solid", bd=1)
        guide_frame.pack(side="right", fill="both", expand=True, padx=(5, 5))

        tk.Label(guide_frame, text="💡 관리자 의사결정 및 대응 가이드 (Rules)", font=(FONT_FAMILY, 11, "bold"), fg="#0052CC",
                 bg="#FFFFFF").pack(anchor="w", padx=15, pady=(10, 5))

        cols_guide = ("고장 유형", "위험 임계치", "대응 가이드")
        guide_tree = ttk.Treeview(guide_frame, columns=cols_guide, show="headings", height=5)
        for c in cols_guide: guide_tree.heading(c, text=c)
        guide_tree.column("고장 유형", width=100, anchor="center")
        guide_tree.column("위험 임계치", width=160, anchor="center")
        guide_tree.column("대응 가이드", width=250, anchor="w")
        guide_tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        guide_tree.insert("", "end", values=("공구 마모 (TWF)", "마모 시간 ≥ 200 min", "🔴 스핀들 정지 및 절삭 공구 즉시 교체"))
        guide_tree.insert("", "end", values=("과부하 (OSF)", "마모 × 토크 한계 초과", "🔴 절삭 파라미터(Feed Rate) 하향 조정"))
        guide_tree.insert("", "end", values=("방열 실패 (HDF)", "Temp 차 < 8.6K & RPM < 1380", "🟠 쿨링팬 및 방열 시스템 긴급 점검"))
        guide_tree.insert("", "end", values=("전력 이상 (PWF)", "Power < 3.5kW or > 9.0kW", "🟠 전력 공급망 및 모터 부하율 점검"))

    def build_evaluation_tab_content(self, res):
        for widget in self.tab_eval.winfo_children(): widget.destroy()
        tk.Label(self.tab_eval, text="[ XGBoost 성능 평가 요약 ]", font=(FONT_FAMILY, 15, "bold"), fg="#0A192F",
                 bg="#FFFFFF").pack(pady=20, anchor="w", padx=30)

        metrics_frame = tk.Frame(self.tab_eval, bg="#FFFFFF", relief="solid", bd=1)
        metrics_frame.pack(fill="x", padx=30, pady=5, ipady=10)

        keys = ["Accuracy (정확도)", "Precision (정밀도)", "Recall (재현율)", "F1-Score", "ROC-AUC"]
        vals = [res['Accuracy'], res['Precision'], res['Recall'], res['F1-Score'], res['AUC']]

        for i, (k, v) in enumerate(zip(keys, vals)):
            box = tk.Frame(metrics_frame, bg="#FFFFFF")
            box.pack(side="left", expand=True, fill="both")
            tk.Label(box, text=k, font=(FONT_FAMILY, 10, "bold"), fg="gray", bg="#FFFFFF").pack(pady=(10, 0))
            color = "#EF4444" if "Recall" in k else "#1E293B"
            tk.Label(box, text=f"{v:.4f}", font=(FONT_FAMILY, 18, "bold"), fg=color, bg="#FFFFFF").pack(pady=(0, 10))

        fig_frame = tk.Frame(self.tab_eval, bg="#FFFFFF")
        fig_frame.pack(fill="both", expand=True, padx=30, pady=15)
        fig = plt.figure(figsize=(10, 4))

        ax1 = fig.add_subplot(1, 2, 1)
        sns.heatmap(res['CM'], annot=True, fmt='d', cmap='Reds', ax=ax1, cbar=False, xticklabels=['정상(0)', '고장(1)'],
                    yticklabels=['정상(0)', '고장(1)'])
        ax1.set_title("XGBoost 혼동행렬 (Confusion Matrix)", fontweight="bold")
        ax1.set_xlabel("AI 예측")
        ax1.set_ylabel("실제 정답")

        ax2 = fig.add_subplot(1, 2, 2)
        ax2.plot(res['FPR'], res['TPR'], label=f"XGBoost (AUC={res['AUC']:.3f})", color="#0052CC", linewidth=2.5)
        ax2.plot([0, 1], [0, 1], 'k--', alpha=0.5)
        ax2.set_title("XGBoost ROC Curve", fontweight="bold")
        ax2.set_xlabel("False Positive Rate")
        ax2.set_ylabel("True Positive Rate")
        ax2.legend()

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=fig_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def build_predict_tab_content(self):
        for widget in self.tab_predict.winfo_children(): widget.destroy()

        header_frame = tk.Frame(self.tab_predict, bg="#F4F6F9")
        header_frame.pack(fill="x", pady=(15, 5), padx=25)
        tk.Label(header_frame, text="[ 스마트 팩토리 실시간 위험 설비 통합 관제 ]", font=(FONT_FAMILY, 14, "bold"), fg="#0A192F",
                 bg="#F4F6F9").pack(side="left")
        self.lbl_scan_count = tk.Label(header_frame, text="스캔된 위험 설비: 0대", font=(FONT_FAMILY, 11, "bold"), fg="#EF4444",
                                       bg="#F4F6F9")
        self.lbl_scan_count.pack(side="right")

        content_pane = tk.Frame(self.tab_predict, bg="#F4F6F9")
        content_pane.pack(fill="both", expand=True, padx=25, pady=5)

        left_pane = tk.Frame(content_pane, bg="#FFFFFF", relief="solid", bd=1, width=420)
        left_pane.pack(side="left", fill="y", padx=(0, 10))
        left_pane.pack_propagate(False)

        tk.Label(left_pane, text="🚨 고장 징후 포착 설비 목록 (클릭하여 상세 조회)", font=(FONT_FAMILY, 10, "bold"), fg="#0A192F",
                 bg="#FFFFFF").pack(anchor="w", padx=10, pady=10)

        list_container = tk.Frame(left_pane, bg="#FFFFFF")
        list_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        cols = ("UDI", "Product ID", "불량 확률")
        self.tree_risk = ttk.Treeview(list_container, columns=cols, show="headings", height=18)
        self.tree_risk.heading("UDI", text="UDI")
        self.tree_risk.heading("Product ID", text="설비 ID")
        self.tree_risk.heading("불량 확률", text="불량 확률")
        self.tree_risk.column("UDI", width=60, anchor="center")
        self.tree_risk.column("Product ID", width=140, anchor="center")
        self.tree_risk.column("불량 확률", width=110, anchor="center")

        scrollbar_risk = ttk.Scrollbar(list_container, orient="vertical", command=self.tree_risk.yview)
        self.tree_risk.configure(yscrollcommand=scrollbar_risk.set)

        self.tree_risk.pack(side="left", fill="both", expand=True)
        scrollbar_risk.pack(side="right", fill="y")

        self.tree_risk.bind("<<TreeviewSelect>>", self.on_risk_machine_selected)

        right_pane = tk.Frame(content_pane, bg="#F4F6F9")
        right_pane.pack(side="right", fill="both", expand=True)

        self.status_frame = tk.Frame(right_pane, bg="#FFFFFF", relief="solid", bd=2)
        self.status_frame.pack(fill="x", pady=(0, 10), ipady=12)

        self.lbl_target_machine = tk.Label(self.status_frame, text="설비를 선택해주세요", font=(FONT_FAMILY, 12, "bold"),
                                           fg="#0052CC", bg="#FFFFFF")
        self.lbl_target_machine.pack(pady=(5, 2))

        self.lbl_predict_res = tk.Label(self.status_frame, text="● 위험 설비 목록에서 기계를 선택하세요",
                                        font=(FONT_FAMILY, 14, "bold"), fg="#64748B", bg="#FFFFFF")
        self.lbl_predict_res.pack(pady=2)

        self.lbl_action_guide = tk.Label(self.status_frame, text="-", font=(FONT_FAMILY, 10), fg="#334155",
                                         bg="#FFFFFF", justify="center")
        self.lbl_action_guide.pack(pady=(2, 5))

        table_frame = tk.Frame(right_pane, bg="#FFFFFF", bd=1, relief="solid")
        table_frame.pack(fill="both", expand=True, pady=(0, 5))
        tk.Label(table_frame, text="📊 선택 설비 실시간 센서 수치 (문제 수치는 붉은색 표시)", font=(FONT_FAMILY, 10, "bold"),
                 bg="#FFFFFF").pack(anchor="w", padx=10, pady=8)

        style = ttk.Style()
        style.map('Treeview', background=[('selected', '#0A192F')], foreground=[('selected', '#FFFFFF')])

        val_cols = ("분석 피처 (Feature)", "실제 측정값")
        self.tree_predict = ttk.Treeview(table_frame, columns=val_cols, show="headings", height=8)
        self.tree_predict.heading("분석 피처 (Feature)", text="분석 피처 (Feature)")
        self.tree_predict.heading("실제 측정값", text="실제 측정값")
        self.tree_predict.column("분석 피처 (Feature)", anchor="center")
        self.tree_predict.column("실제 측정값", anchor="center")
        self.tree_predict.pack(fill="x", padx=10, pady=(0, 10))

        self.tree_predict.tag_configure('danger', background='#FEE2E2', foreground='#B91C1C')

        self.risk_data_store = {}

    def run_realtime_prediction(self):
        if not self.engine.is_trained:
            messagebox.showwarning("경고", "먼저 [XGBoost 학습] 버튼을 눌러주세요!")
            return

        for item in self.tree_risk.get_children(): self.tree_risk.delete(item)
        self.risk_data_store.clear()

        risk_count = 0
        for idx in self.engine.test_indices:
            machine_info, display_data, probabilities, prediction, action_guide, problematic_features = self.engine.analyze_sample_details(
                idx)
            p1 = probabilities[1]

            if prediction == 1 or p1 >= 0.5:
                risk_count += 1
                prob_str = f"{p1 * 100:.1f}% (위험)"
                item_id = self.tree_risk.insert("", "end",
                                                values=(machine_info['UDI'], machine_info['Product ID'], prob_str))

                self.risk_data_store[item_id] = {
                    "machine_info": machine_info,
                    "display_data": display_data,
                    "probabilities": probabilities,
                    "prediction": prediction,
                    "action_guide": action_guide,
                    "problematic_features": problematic_features
                }

        self.lbl_scan_count.config(text=f"스캔된 위험 설비: {risk_count}대")
        if risk_count > 0:
            first_item = self.tree_risk.get_children()[0]
            self.tree_risk.selection_set(first_item)
            self.on_risk_machine_selected(None)
        else:
            messagebox.showinfo("관제 결과", "현재 테스트 셋 내에 위험 임계점을 넘은 설비가 없습니다.")

    def on_risk_machine_selected(self, event):
        selected_items = self.tree_risk.selection()
        if not selected_items: return

        item_id = selected_items[0]
        data = self.risk_data_store.get(item_id)
        if not data: return

        machine_info = data["machine_info"]
        display_data = data["display_data"]
        probabilities = data["probabilities"]
        prediction = data["prediction"]
        action_guide = data["action_guide"]
        problematic_features = data["problematic_features"]
        p0, p1 = probabilities[0], probabilities[1]

        self.lbl_target_machine.config(
            text=f"대상 설비 ID: {machine_info['Product ID']} (UDI: {machine_info['UDI']}, Type: {machine_info['Type']})")

        for item in self.tree_predict.get_children(): self.tree_predict.delete(item)

        for d in display_data:
            feature_name = d[0]
            if feature_name in problematic_features:
                self.tree_predict.insert("", "end", values=d, tags=('danger',))
            else:
                self.tree_predict.insert("", "end", values=d)

        if prediction == 1 or p1 >= 0.5:
            self.status_frame.config(bg="#FEF2F2", highlightbackground="#EF4444")
            self.lbl_predict_res.config(text=f"⚠️ [위험] 고장 징후 포착! (불량 확률: {p1 * 100:.1f}%)", fg="#EF4444", bg="#FEF2F2")
            self.lbl_action_guide.config(text=action_guide, fg="#B91C1C", bg="#FEF2F2", font=(FONT_FAMILY, 10, "bold"))
        else:
            self.status_frame.config(bg="#F0FDF4", highlightbackground="#16A34A")
            self.lbl_predict_res.config(text=f"✅ [정상] 설비 가동 양호 (정상 확률: {p0 * 100:.1f}%)", fg="#16A34A", bg="#F0FDF4")
            self.lbl_action_guide.config(text=action_guide, fg="#15803D", bg="#F0FDF4", font=(FONT_FAMILY, 10))


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoEverDashboardApp(root)
    root.mainloop()