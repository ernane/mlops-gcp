import argparse
import os

import joblib
import numpy as np
import pandas as pd
from google.cloud import storage
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def train_model(data_path, model_dir):
    """
    Treina um modelo de regressão linear com pré-processamento e métricas de avaliação.
    """
    # Ler os dados
    df = pd.read_csv(data_path)
    print("Dados carregados com sucesso.")

    # Separar features e target
    X = df.drop("vendas", axis=1)  # Variáveis independentes
    y = df["vendas"]  # Variável dependente (target)

    # Dividir os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Definir pré-processamento
    numeric_features = ["mes", "dia_da_semana"]  # Colunas numéricas
    categorical_features = ["promocao"]  # Colunas categóricas

    # Pipeline de pré-processamento
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                StandardScaler(),
                numeric_features,
            ),  # Normalização para colunas numéricas
            (
                "cat",
                OneHotEncoder(),
                categorical_features,
            ),  # Codificação one-hot para colunas categóricas
        ]
    )

    # Pipeline completo (pré-processamento + modelo)
    model = Pipeline(
        steps=[("preprocessor", preprocessor), ("regressor", LinearRegression())]
    )

    # Treinar o modelo
    model.fit(X_train, y_train)
    print("Modelo treinado com sucesso.")

    # Avaliar o modelo no conjunto de teste
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    print(f"RMSE no conjunto de teste: {rmse}")
    print(f"R² no conjunto de teste: {r2}")

    # Validação cruzada
    cv_scores = cross_val_score(model, X, y, cv=5, scoring="neg_mean_squared_error")
    cv_rmse = np.sqrt(-cv_scores.mean())
    print(f"RMSE com validação cruzada: {cv_rmse}")

    # Salvar o modelo localmente
    model_filename = "model.joblib"
    gcs_model_path = os.path.join(model_filename)
    joblib.dump(model, gcs_model_path)
    print(f"Modelo salvo localmente em: {gcs_model_path}")

    # # Fazer upload do modelo para o Cloud Storage
    upload_model_to_gcs(gcs_model_path, model_dir)


def upload_model_to_gcs(local_path, gcs_path):
    """
    Faz upload do modelo treinado para o Cloud Storage.
    """
    client = storage.Client()
    bucket_name, blob_name = gcs_path.replace("gs://", "").split("/", 1)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_path)
    print(f"Modelo salvo em: {gcs_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-path", type=str, required=True, help="Caminho para o arquivo de dados."
    )
    parser.add_argument(
        "--model-dir",
        dest="model_dir",
        default=os.getenv("AIP_MODEL_DIR"),
        help="Caminho no GCS para salvar o modelo.",
    )
    args = parser.parse_args()

    # Treinar e salvar o modelo
    train_model(args.data_path, args.model_dir)
