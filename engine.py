import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc, confusion_matrix
from sklearn.preprocessing import StandardScaler

class AutoEverSmartFactoryEngine:
    def __init__(self):
        self.file_path = None
        self.df = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
        self.X_test = None
        self.y_test = None
        self.test_indices = []

    def load_data(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
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

        df_clean = df_work.drop(columns=['UDI', 'Product ID'])
        df_clean = pd.get_dummies(df_clean, columns=['Type'])

        target = 'Machine failure'
        X = df_clean.drop(columns=[target, 'TWF', 'HDF', 'PWF', 'OSF', 'RNF'])
        y = df_clean[target]

        numeric_cols = ['Air_temperature', 'Process_temperature', 'Rotational_speed', 'Torque', 'Tool_wear']
        X[numeric_cols] = self.scaler.fit_transform(X[numeric_cols])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42, stratify=y)

        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)[:, 1]

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
        prediction = self.model.predict(X_sample)[0]

        machine_info = {
            "UDI": raw_sample['UDI'],
            "Product ID": raw_sample['Product ID'],
            "Type": raw_sample['Type']
        }

        action_guide = "특이사항 없음. 정상 가동 유지 중"
        problematic_features = []
        detected_failures = []

        if prediction == 1 or probabilities[1] >= 0.5:
            tool_wear = raw_sample['Tool wear [min]']
            torque = raw_sample['Torque [Nm]']
            rpm = raw_sample['Rotational speed [rpm]']
            air_temp = raw_sample['Air temperature [K]']
            process_temp = raw_sample['Process temperature [K]']

            temp_diff = process_temp - air_temp
            power = torque * (rpm * 2 * np.pi / 60)
            osf_limit = 11000 if raw_sample['Type'] == 'L' else (12000 if raw_sample['Type'] == 'M' else 13000)

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
            ("설비 등급 (Type)", raw_sample['Type']),
            ("Air Temp [K]", f"{raw_sample['Air temperature [K]']:.1f}"),
            ("Process Temp [K]", f"{raw_sample['Process temperature [K]']:.1f}"),
            ("Speed [rpm]", f"{raw_sample['Rotational speed [rpm]']:.0f}"),
            ("Torque [Nm]", f"{raw_sample['Torque [Nm]']:.1f}"),
            ("Tool Wear [min]", f"{raw_sample['Tool wear [min]']:.0f}")
        ]

        return machine_info, display_data, probabilities, prediction, action_guide, problematic_features