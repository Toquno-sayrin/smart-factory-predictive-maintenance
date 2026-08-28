import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc, confusion_matrix
from sklearn.preprocessing import StandardScaler

class AutoEverSmartFactoryEngine:
    REQUIRED_COLUMNS = {
        'Air temperature [K]',
        'Process temperature [K]', 'Rotational speed [rpm]',
        'Torque [Nm]', 'Tool wear [min]', 'Machine failure'
    }

    def __init__(self):
        self.file_path = None
        self.df = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
        self.decision_threshold = 0.5
        self.X_test = None
        self.y_test = None
        self.test_indices = []

    def load_data(self, file_path):
        loaded_df = pd.read_csv(file_path, encoding='utf-8-sig')
        loaded_df.columns = loaded_df.columns.astype(str).str.strip()

        columns = set(loaded_df.columns)
        has_type = 'Type' in columns or {'Type_H', 'Type_L', 'Type_M'}.issubset(columns)
        missing_columns = sorted(self.REQUIRED_COLUMNS - columns)
        if not has_type:
            missing_columns.append('Type 또는 Type_H/Type_L/Type_M')
        if missing_columns:
            missing = ', '.join(missing_columns)
            raise ValueError(
                "스마트팩토리 센서 형식의 CSV가 아닙니다. "
                f"필수 컬럼이 없습니다: {missing}"
            )

        self.file_path = file_path
        self.df = loaded_df
        return self.df

    def run_pipeline(self, test_size=0.2, cv_setting="5-Fold"):
        if self.df is None:
            raise ValueError("로드된 데이터가 없습니다. 먼저 파일을 열어주세요.")

        df_work = self.df.rename(columns={
            'Air temperature [K]': 'Air_temperature',
            'Process temperature [K]': 'Process_temperature',
            'Rotational speed [rpm]': 'Rotational_speed',
            'Torque [Nm]': 'Torque',
            'Tool wear [min]': 'Tool_wear'
        })
        #파생변수 추가
        df_clean = df_work.drop(columns=['UDI', 'Product ID'], errors='ignore')
        df_clean['power'] = df_clean['Rotational_speed'] * df_clean['Torque']
        df_clean['temp_diff'] = df_clean['Process_temperature'] - df_clean['Air_temperature']
        df_clean['wear_torque'] = df_clean['Tool_wear'] * df_clean['Torque']

        df_clean['flag_heat'] = ((df_clean['temp_diff'] < 8.6) & (df_clean['Rotational_speed'] < 1380)).astype(int)
        df_clean['flag_power'] = ((df_clean['power'] < 3500) | (df_clean['power'] > 9000)).astype(int)
        df_clean['flag_wear'] = (df_clean['Tool_wear'] >= 200).astype(int)

        df_clean['risk_count'] = df_clean['flag_heat'] + df_clean['flag_power'] + df_clean['flag_wear']
        df_clean['power_dev'] = np.abs(df_clean['power'] - df_clean['power'].median())
        df_clean['wear_stage'] = pd.cut(
            df_clean['Tool_wear'],
            bins=[-1, 50, 100, 150, 200, 9999],
            labels=[0, 1, 2, 3, 4]
        ).astype(int)
        # ==========================================

        if 'Type' in df_clean.columns:
            df_clean = pd.get_dummies(df_clean, columns=['Type'])

        target = 'Machine failure'
        X = df_clean.drop(columns=[target, 'TWF', 'HDF', 'PWF', 'OSF', 'RNF'], errors='ignore')
        y = df_clean[target]

        numeric_cols = [
            'Air_temperature', 'Process_temperature', 'Rotational_speed', 'Torque', 'Tool_wear',
            'power', 'temp_diff', 'wear_torque', 'power_dev'  # 새로 추가한 수치형 피처들 추가
        ]
        X[numeric_cols] = self.scaler.fit_transform(X[numeric_cols])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42, stratify=y)

        neg_count = int((y_train == 0).sum())
        pos_count = int((y_train == 1).sum())
        self.model.set_params(scale_pos_weight=neg_count / pos_count)

        self.model.fit(X_train, y_train)
        y_proba = self.model.predict_proba(X_test)[:, 1]
        y_pred = (y_proba >= self.decision_threshold).astype(int)

        fpr, tpr, _ = roc_curve(y_test, y_proba)
        roc_auc = auc(fpr, tpr)
        cm = confusion_matrix(y_test, y_pred)

        results = {
            'Accuracy': accuracy_score(y_test, y_pred),
            'Precision': precision_score(y_test, y_pred, zero_division=0),
            'Recall': recall_score(y_test, y_pred, zero_division=0),
            'F1-Score': f1_score(y_test, y_pred, zero_division=0),
            'AUC': roc_auc,
            'FPR': fpr,
            'TPR': tpr,
            'CM': cm
        }

        if cv_setting != "None":
            n_splits = int(cv_setting.replace("-Fold", ""))
            cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
            cv_scores = cross_val_score(self.model, X, y, cv=cv, scoring='f1')
            results[f'CV Mean F1'] = cv_scores.mean()

        self.X_test = X_test
        self.y_test = y_test
        self.test_indices = X_test.index
        self.is_trained = True
        return results

    def analyze_sample_details(self, sample_idx):
        raw_sample = self.df.loc[sample_idx]
        X_sample = self.X_test.loc[[sample_idx]]

        probabilities = self.model.predict_proba(X_sample)[0]
        prediction = int(probabilities[1] >= self.decision_threshold)

        if 'Type' in raw_sample.index:
            machine_type = raw_sample['Type']
        else:
            type_columns = ['Type_H', 'Type_L', 'Type_M']
            machine_type = next((column[-1] for column in type_columns
                                 if column in raw_sample.index and raw_sample[column] == 1), 'Unknown')

        machine_info = {
            "UDI": raw_sample.get('UDI', sample_idx + 1),
            "Product ID": raw_sample.get('Product ID', f'Machine-{sample_idx + 1:05d}'),
            "Type": machine_type
        }

        action_guide = "특이사항 없음. 정상 가동 유지 중"
        problematic_features = []
        detected_failures = []

        if prediction == 1:
            tool_wear = raw_sample['Tool wear [min]']
            torque = raw_sample['Torque [Nm]']
            rpm = raw_sample['Rotational speed [rpm]']
            air_temp = raw_sample['Air temperature [K]']
            process_temp = raw_sample['Process temperature [K]']

            temp_diff = process_temp - air_temp
            power = torque * (rpm * 2 * np.pi / 60)
            osf_limit = 11000 if machine_type == 'L' else (12000 if machine_type == 'M' else 13000)

            if tool_wear >= 200:
                detected_failures.append("공구 마모 한계(TWF)")
                problematic_features.append("Tool Wear [min]")

            if (temp_diff < 8.6) and (rpm < 1380):
                detected_failures.append("방열 실패(HDF)")
                problematic_features.extend(["Air Temp [K]", "Process Temp [K]", "Speed [rpm]"])

            if power < 3500 or power > 9000:
                detected_failures.append("전력 이상(PWF)")
                problematic_features.extend(["Speed [rpm]", "Torque [Nm]"])

            if tool_wear * torque > osf_limit:
                detected_failures.append("과부하(OSF)")
                problematic_features.extend(["Torque [Nm]", "Tool Wear [min]"])

            if len(detected_failures) >= 2:
                failures_str = " + ".join(detected_failures)
                action_guide = f"⚠️ [복합 이상 징후] 다중 결함 발생 ({failures_str}) | 종합 점검 요망"
            elif len(detected_failures) == 1:
                f_name = detected_failures[0]
                if "TWF" in f_name:
                    action_guide = "⚠️ [공구 마모 한계(TWF)] 스핀들 가동 중지 및 공구 교체 요망"
                elif "HDF" in f_name:
                    action_guide = "⚠️ [방열 실패(HDF)] 쿨링 시스템 점검 요망"
                elif "PWF" in f_name:
                    action_guide = "⚠️ [전력 이상(PWF)] 가동 속도 및 절삭 부하 점검 요망"
                elif "OSF" in f_name:
                    action_guide = "⚠️ [과부하(OSF) 감지] 절삭 토크 하향 조정 요망"
            else:
                action_guide = "⚠️ [우발적 고장(RNF) 징후] 엔지니어 정밀 점검 요망"

        problematic_features = list(set(problematic_features))

        display_data = [
            ("설비 등급 (Type)", machine_type),
            ("Air Temp [K]", f"{raw_sample['Air temperature [K]']:.1f}"),
            ("Process Temp [K]", f"{raw_sample['Process temperature [K]']:.1f}"),
            ("Speed [rpm]", f"{raw_sample['Rotational speed [rpm]']:.0f}"),
            ("Torque [Nm]", f"{raw_sample['Torque [Nm]']:.1f}"),
            ("Tool Wear [min]", f"{raw_sample['Tool wear [min]']:.0f}")
        ]

        return machine_info, display_data, probabilities, prediction, action_guide, problematic_features
