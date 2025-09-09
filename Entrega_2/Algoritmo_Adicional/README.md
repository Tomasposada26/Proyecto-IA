# <a name="header"></a><a name="content"></a><a name="x3f50b9aefac13653879f1d239bb0cec6f5e8f01"></a>Informe: Gradient Boosting sobre Jugadores de la Premier League
## <a name="descripción-del-dataset"></a>1. Descripción del dataset
- **Fuente:** Kaggle (Premier League Player Stats)
- **Registros:** 574 jugadores
- **Variables:** 36 columnas (edad, nacionalidad, posición, minutos jugados, goles, asistencias, métricas avanzadas, etc.)
- **Objetivo del problema:** Predicción de la métrica avanzada npxG+xAG.1 (expected goals sin penales + expected assists por 90 minutos).
## <a name="preprocesamiento-realizado"></a>2. Preprocesamiento realizado
- **a. Limpieza de datos faltantes:**
- Se eliminaron filas con valores nulos para asegurar la calidad de los datos.
- **b. Codificación de variables categóricas:**
- Se aplicó LabelEncoder a columnas de texto (ej. nombre, nacionalidad, posición, equipo).
- **c. Escalado/normalización:**
- Se utilizó StandardScaler para normalizar todas las variables predictoras numéricas.
- **d. División en train/test:**
- 80% de los datos para entrenamiento, 20% para prueba, usando train\_test\_split.
## <a name="entrenamiento-del-modelo"></a>3. Entrenamiento del modelo
- **Modelo:** GradientBoostingRegressor (scikit-learn)
- **Hiperparámetros principales:**
- n\_estimators = 300
- learning\_rate = 0.05
- max\_depth = 3
- subsample = 0.8
- random\_state = 42

El modelo se entrena de manera aditiva, donde cada nuevo árbol corrige los errores residuales del anterior.
## <a name="evaluación-de-resultados"></a>4. Evaluación de resultados
- **Métricas de rendimiento:**
- MSE (Error cuadrático medio) ≈ 0.0028
- R² (Coeficiente de determinación) ≈ 0.97
- **Visualización:**
- Se generó una gráfica de predicciones vs valores reales (gb\_predictions.png).

Gráfico de predicciones
## <a name="conclusiones"></a>5. Conclusiones
- El modelo Gradient Boosting logra una predicción muy precisa de la métrica avanzada npxG+xAG.1.
- Un R² cercano a 1 indica que explica la mayor parte de la variabilidad de los datos.
- Es una alternativa poderosa frente a un solo árbol de decisión y complementa bien el análisis frente a la red neuronal del punto 2.
- Como mejoras futuras:
- Ajuste de hiperparámetros con GridSearchCV o RandomizedSearchCV.
- Uso de librerías más avanzadas como **XGBoost** o **LightGBM**.
-----
## <a name="ejecución-paso-a-paso"></a>Ejecución paso a paso
1. **Ubícate en la carpeta del proyecto:**

   cd Entrega\_2/punto3
1. **Crea y activa el entorno virtual (recomendado):**

   python -m venv ..\.venv\
   ..\.venv\Scripts\activate   # En Windows\
   source ../.venv/bin/activate  # En Linux/Mac
1. **Instala las dependencias necesarias:**

   pip install pandas numpy scikit-learn matplotlib joblib
1. **Ejecuta el script principal:**

   python gradient\_boosting.py
1. **Archivos generados:**
1. gradient\_boosting\_model.pkl: modelo entrenado guardado.
1. gb\_predictions.png: gráfica de predicciones vs valores reales.
1. **Notas:**
1. El script imprime en consola métricas de evaluación (MSE y R²).
1. El entrenamiento es rápido, pero puede variar según el hardware.
-----
