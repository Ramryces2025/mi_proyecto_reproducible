from __future__ import annotations

import argparse
import pickle
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

FEATURES = ["age", "income", "years_experience", "gender"]
TARGET = "target"


def load_data(csv_path: Path) -> pd.DataFrame:
    # Falla rápido si la ruta del dataset es incorrecta.
    if not csv_path.exists():
        raise FileNotFoundError(f"Data file not found: {csv_path}")

    df = pd.read_csv(csv_path)

    # Valida columnas requeridas para evitar errores difíciles de rastrear.
    required = FEATURES + [TARGET]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in dataset: {missing}")

    # Normaliza valores de género si vienen como texto.
    if "gender" in df.columns and df["gender"].dtype == object:
        df["gender"] = (
            df["gender"].astype(str).str.strip().str.upper().map({"M": 0, "F": 1})
        )

    return df


def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    X = df[FEATURES].copy()
    y = df[TARGET]

    # Manejo básico de nulos: numérico -> mediana, no numérico -> valor centinela.
    for col in FEATURES:
        if X[col].isna().any():
            if X[col].dtype.kind in "biufc":
                X[col] = X[col].fillna(X[col].median())
            else:
                X[col] = X[col].fillna(-1)

    return X, y


def train_model(
    X: pd.DataFrame, y: pd.Series, test_size: float, random_state: int
) -> tuple[RandomForestClassifier, float, list[list[int]]]:
    # Estratifica cuando es posible para mantener el balance de clases.
    stratify = y if y.nunique() > 1 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=stratify
    )

    # random_state fijo para reproducibilidad.
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    cm = confusion_matrix(y_test, preds).tolist()

    return model, acc, cm


def save_model(model: RandomForestClassifier, path: Path) -> None:
    # Crea el directorio de salida si no existe.
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        pickle.dump(model, f)


def parse_args() -> argparse.Namespace:
    # Valores por defecto relativos a la raíz del proyecto.
    project_root = Path(__file__).resolve().parents[1]
    default_data = project_root / "data" / "raw" / "data_export.csv"
    default_model = project_root / "models" / "modelo_final_v2.pkl"

    parser = argparse.ArgumentParser(description="Train a RandomForest model.")
    parser.add_argument("--data", type=Path, default=default_data)
    parser.add_argument("--model-out", type=Path, default=default_model)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Pipeline completo de entrenamiento.
    df = load_data(args.data)
    X, y = prepare_features(df)
    model, acc, cm = train_model(X, y, args.test_size, args.seed)
    save_model(model, args.model_out)

    print("Training finished.")
    print(f"Accuracy: {acc:.4f}")
    print("Confusion Matrix:")
    print(cm)
    print(f"Model saved to: {args.model_out}")


if __name__ == "__main__":
    main()
