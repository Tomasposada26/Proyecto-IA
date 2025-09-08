
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


def explore_data(data: pd.DataFrame) -> None:

    print('Dimensiones:', data.shape)
    print('\nPrimeras filas:')
    print(data.head())
    print('\nInformación del DataFrame:')
    print(data.info())
    print('\nValores nulos por columna:')
    print(data.isnull().sum())


def select_target_column(data: pd.DataFrame) -> str:
  
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    if 'value' in numeric_cols:
        return 'value'
    # Si no existe ``value``, seleccionar la última columna numérica
    return numeric_cols[-1]


def preprocess_data(data: pd.DataFrame, target: str) -> tuple:

    # Eliminar filas con valores nulos
    df = data.dropna().copy()

    # Codificar columnas categóricas
    for col in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

    # Separar variables predictoras y objetivo
    X = df.drop(columns=[target])
    y = df[target]

    # Escalar características
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Dividir en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test, scaler


def train_gradient_boosting(X_train: np.ndarray, y_train: pd.Series) -> GradientBoostingRegressor:

    model = GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=3,
        subsample=0.8,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(model: GradientBoostingRegressor, X_test: np.ndarray, y_test: pd.Series) -> tuple:
  
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2, y_pred


def save_results(model: GradientBoostingRegressor, y_test: pd.Series, y_pred: np.ndarray) -> None:
    
    # Obtener rutas relativas del directorio actual
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'gradient_boosting_model.pkl')
    plot_path = os.path.join(base_dir, 'gb_predictions.png')

    # Guardar el modelo con joblib
    joblib.dump(model, model_path)
    print(f'Modelo guardado como {model_path}')

    # Generar gráfica de dispersión de predicciones vs valores reales
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, alpha=0.6)
    plt.xlabel('Valor real')
    plt.ylabel('Predicción')
    plt.title('Gradient Boosting - Predicciones vs Valores reales')
    plt.tight_layout()
    # Guardar la figura en disco. No se llama a plt.show() para evitar
    # problemas en entornos sin interfaz gráfica.
    plt.savefig(plot_path)
    plt.close()
    print(f'Gráfica guardada como {plot_path}')


def main():
    """Función principal para ejecutar el flujo completo del script."""
    # Cargar el dataset utilizando la ruta relativa al script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, 'player_stats.csv')
    data = pd.read_csv(dataset_path)

    # Exploración básica (opcional)
    explore_data(data)

    # Seleccionar la columna objetivo
    target_col = select_target_column(data)
    print(f'Variable objetivo seleccionada: {target_col}')

    # Preprocesamiento
    X_train, X_test, y_train, y_test, scaler = preprocess_data(data, target_col)

    # Entrenamiento del modelo
    model = train_gradient_boosting(X_train, y_train)

    # Evaluación
    mse, r2, y_pred = evaluate_model(model, X_test, y_test)
    print(f'\nResultados de evaluación:')
    print(f'MSE: {mse:.4f}')
    print(f'R²: {r2:.4f}')

    # Guardar resultados (modelo y gráfica)
    save_results(model, y_test, y_pred)


if __name__ == '__main__':
    main()