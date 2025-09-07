import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import os


# Cargar el dataset con la ruta correcta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, 'player_stats.csv')
df = pd.read_csv(DATASET_PATH)

# Exploración básica
def explore_data(df):
    print('Primeras filas:')
    print(df.head())
    print('\nInfo:')
    print(df.info())
    print('\nDescripción:')
    print(df.describe())
    print('\nValores nulos por columna:')
    print(df.isnull().sum())

explore_data(df)

# Selección de variable objetivo automáticamente (numérica)
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if 'value' in numeric_cols:
    target_col = 'value'
else:
    target_col = numeric_cols[-1]  # Última columna numérica

print(f'Variable objetivo seleccionada: {target_col}')

# Preprocesamiento
def preprocess_data(df, target_col):
    df = df.copy()
    # Eliminar filas con valores nulos
    df = df.dropna()
    # Codificar variables categóricas
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = LabelEncoder().fit_transform(df[col])
    # Separar variables predictoras y objetivo
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    # Normalizar
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y, scaler

X, y, scaler = preprocess_data(df, target_col)

# Separar en train y test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Definir la red neuronal
def build_model(input_dim):
    model = Sequential([
        Dense(128, activation='relu', input_dim=input_dim),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(1)  # Regresión
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

model = build_model(X_train.shape[1])

# Entrenamiento
es = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
history = model.fit(
    X_train, y_train,
    validation_split=0.2,
    epochs=100,
    batch_size=32,
    callbacks=[es],
    verbose=1
)

# Evaluación
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'MSE: {mse:.2f}, R2: {r2:.2f}')

# Guardar el modelo y la gráfica en la misma carpeta que el script
MODEL_PATH = os.path.join(BASE_DIR, 'player_model.h5')
PLOT_PATH = os.path.join(BASE_DIR, 'training_plot.png')
model.save(MODEL_PATH)
print(f'Modelo guardado como {MODEL_PATH}')

# Graficar el entrenamiento
plt.plot(history.history['loss'], label='train_loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.legend()
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Entrenamiento de la Red Neuronal')
plt.savefig(PLOT_PATH)
plt.show()
print(f'Gráfica guardada como {PLOT_PATH}')
