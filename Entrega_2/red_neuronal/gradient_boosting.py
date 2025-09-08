"""
Modulo: gradient_boosting

Este script implementa un modelo de Gradient Boosting para resolver el
tercer punto del proyecto de análisis de rendimiento de jugadores. El
objetivo es predecir la última columna numérica del conjunto de datos
(`npxG+xAG.1`), que se selecciona automáticamente como variable objetivo
si el archivo de estadísticas no incluye una columna llamada ``value``.

Pasos principales:

1. Cargar los datos del archivo ``player_stats.csv`` ubicado en el mismo
   directorio que este script.
2. Realizar exploración básica para entender la estructura del dataset.
3. Identificar la columna objetivo (``value`` si existe, o la última
   columna numérica en caso contrario).
4. Preprocesar los datos:
   - Eliminar filas con valores nulos.
   - Codificar variables categóricas mediante ``LabelEncoder``.
   - Normalizar las variables predictoras mediante ``StandardScaler``.
5. Separar los datos en conjuntos de entrenamiento y prueba.
6. Entrenar un modelo ``GradientBoostingRegressor`` con hiperparámetros
   razonables.
7. Evaluar el modelo utilizando MSE y R² en el conjunto de prueba.
8. Guardar el modelo entrenado y una gráfica de dispersión de las
   predicciones frente a los valores reales.

Para ejecutar este script:

```
python gradient_boosting.py
```

Se generarán dos archivos en el directorio del script:
``gradient_boosting_model.pkl`` y ``gb_predictions.png``.
"""

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
    """Imprime información básica del DataFrame para exploración.

    Args:
        data (pd.DataFrame): Conjunto de datos cargado.
    """
    print('Dimensiones:', data.shape)
    print('\nPrimeras filas:')
    print(data.head())
    print('\nInformación del DataFrame:')
    print(data.info())
    print('\nValores nulos por columna:')
    print(data.isnull().sum())


def select_target_column(data: pd.DataFrame) -> str:
    """Selecciona la columna objetivo para la predicción.

    Si el DataFrame incluye una columna denominada ``value``, ésta
    se elige como objetivo; de lo contrario, se elige la última
    columna numérica disponible.

    Args:
        data (pd.DataFrame): Conjunto de datos cargado.

    Returns:
        str: Nombre de la columna objetivo seleccionada.
    """
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    if 'value' in numeric_cols:
        return 'value'
    # Si no existe ``value``, seleccionar la última columna numérica
    return numeric_cols[-1]


def preprocess_data(data: pd.DataFrame, target: str) -> tuple:
    """Preprocesa los datos para su uso en el modelo.

    - Elimina filas con valores nulos.
    - Codifica variables categóricas con LabelEncoder.
    - Escala las variables predictoras usando StandardScaler.

    Args:
        data (pd.DataFrame): Conjunto de datos cargado.
        target (str): Nombre de la columna objetivo.

    Returns:
        tuple: (X_train, X_test, y_train, y_test, scaler)
    """
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
    """Entrena un modelo GradientBoostingRegressor con hiperparámetros fijos.

    Args:
        X_train (np.ndarray): Matriz de entrenamiento de características.
        y_train (pd.Series): Serie de valores objetivo de entrenamiento.

    Returns:
        GradientBoostingRegressor: Modelo entrenado.
    """
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
    """Evalúa el modelo en el conjunto de prueba y devuelve métricas.

    Args:
        model (GradientBoostingRegressor): Modelo entrenado.
        X_test (np.ndarray): Matriz de características de prueba.
        y_test (pd.Series): Valores objetivo reales de prueba.

    Returns:
        tuple: (mse, r2, y_pred) donde mse es el error cuadrático medio,
        r2 es el coeficiente de determinación y y_pred las predicciones.
    """
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2, y_pred


def save_results(model: GradientBoostingRegressor, y_test: pd.Series, y_pred: np.ndarray) -> None:
    """Guarda el modelo y una gráfica de predicciones.

    Args:
        model (GradientBoostingRegressor): Modelo entrenado.
        y_test (pd.Series): Valores reales de prueba.
        y_pred (np.ndarray): Predicciones generadas por el modelo.
    """
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