# Análisis Comparativo de Modelos de Aprendizaje Supervisado sobre Jugadores de la Premier League

## 1. Descripción del dataset
- **Fuente:** Kaggle (Premier League Player Stats 2024-25)  
- **Registros:** 574 jugadores (tras filtrado en algunos modelos)  
- **Variables:** 36 columnas (edad, nacionalidad, posición, minutos jugados, goles, asistencias, métricas avanzadas, etc.)  
- **Objetivo del problema:**
  - Para regresión: predecir la métrica avanzada `npxG+xAG.1` (expected goals sin penales + expected assists por 90 minutos), que mide el aporte ofensivo esperado de cada jugador.
  - Para clasificación: categorizar la eficiencia ofensiva de los jugadores en "Alta", "Media" o "Baja" según su rendimiento ajustado por expectativas.

## 2. Preprocesamiento realizado
- **a. Limpieza de datos faltantes:**  
  Se eliminaron filas con valores nulos en todos los modelos para asegurar la calidad de los datos.
- **b. Codificación de variables categóricas:**  
  Se aplicó Label Encoding a columnas de texto (nombre, nacionalidad, posición, equipo) en todos los modelos.
- **c. Escalado / normalización:**  
  Se utilizó `StandardScaler` para normalizar todas las variables predictoras numéricas en los modelos de regresión y clasificación.
- **d. División en train/test:**  
  80% entrenamiento / 20% prueba (`train_test_split`).  
  En el modelo de clasificación se filtraron jugadores con ≥ 270 minutos y se balancearon las clases con `RandomOverSampler`.

## 3. Entrenamiento de los tres modelos con sus parámetros

### a. Árbol de Decisión (Clasificación)
- **Modelo:** `DecisionTreeClassifier`
- **Parámetros / Estrategias:**
  - Balanceo de clases con `RandomOverSampler`
  - Variables derivadas para representar eficiencia
- **Objetivo:** Clasificar la eficiencia ofensiva en tres categorías.

### b. Red Neuronal (Regresión)
- **Modelo:** Keras Sequential
- **Arquitectura:**
  - Dense(128, ReLU) + Dropout 0.3  
  - Dense(64, ReLU) + Dropout 0.2  
  - Dense(32, ReLU)  
  - Output: Dense(1) (regresión)
- **Parámetros:**
  - Optimizador: Adam
  - Loss: MSE
  - Métrica: MAE
  - EarlyStopping (patience=10)
  - Epochs máx: 100
  - Batch size: 32
- **Objetivo:** Predecir `npxG+xAG.1`.

### c. Gradient Boosting (Regresión)
- **Modelo:** `GradientBoostingRegressor`
- **Parámetros principales:**
  - `n_estimators = 300`
  - `learning_rate = 0.05`
  - `max_depth = 3`
  - `subsample = 0.8`
  - `random_state = 42`
- **Objetivo:** Predecir `npxG+xAG.1`.

## 4. Evaluación de resultados

### a. Árbol de Decisión (Clasificación)
- **Métricas:**
  - Accuracy: 0.73  
  - Macro F1: 0.73  
  - Weighted F1: 0.72  
  - Detalle por clase:

    | Clase | Precisión | Recall | F1-score | Soporte |
    |-------|-----------|--------|----------|---------|
    | Alta  | 0.60      | 0.52   | 0.55     | 64      |
    | Baja  | 0.61      | 0.69   | 0.64     | 70      |
    | Media | 1.00      | 1.00   | 1.00     | 60      |
- **Visualizaciones:**
  - Matriz de confusión (`matriz_confusion.png`)
  - Importancia de variables (`Variables.png`)

### b. Red Neuronal (Regresión)
- **Métricas:**
  - MSE ≈ 0.01  
  - R² ≈ 0.89
- **Visualización:** curva de entrenamiento (`training_plot.png`).

### c. Gradient Boosting (Regresión)
- **Métricas:**
  - MSE ≈ 0.0028  
  - R² ≈ 0.97
- **Visualización:** predicciones vs valores reales (`gb_predictions.png`).

## 5. Análisis comparativo

### 5.1 Desempeño (Integración ampliada)
- **Gradient Boosting** fue el modelo con mejor desempeño en regresión (R² ≈ 0.97, MSE ≈ 0.0028), mostrando una capacidad sobresaliente para predecir la métrica avanzada de aporte ofensivo. Su curva de predicción es la más alineada con los valores reales, ideal para escenarios donde la precisión es crítica (scouting profesional, valoración de transferencias o modelado de impacto esperado).
- **Red Neuronal** obtuvo un desempeño muy bueno (R² ≈ 0.89, MSE ≈ 0.01). Presenta robustez y buena generalización cuando existen relaciones no lineales complejas. Es una alternativa potente cuando se cuenta con recursos computacionales y se prevé escalabilidad (integrar más temporadas, features tácticos, tracking data, etc.).
- **Árbol de Decisión** (clasificación) alcanzó accuracy ≈ 0.73 y macro F1 ≈ 0.73. Útil para segmentar jugadores en categorías de eficiencia (rápido para análisis táctico o filtrado de talento). La clase “Media” fue perfectamente reconocida (F1=1.00), lo que sugiere posible sobreajuste o una frontera muy clara para esa clase tras el balanceo.

### 5.2 Comparación resumida de métricas
| Modelo               | Tarea           | Métrica Clave | Valor Aproximado | Observación |
|----------------------|-----------------|---------------|------------------|-------------|
| Gradient Boosting    | Regresión       | R²            | 0.97             | Máxima precisión predictiva |
| Gradient Boosting    | Regresión       | MSE           | 0.0028           | Error muy bajo |
| Red Neuronal         | Regresión       | R²            | 0.89             | Buen ajuste, menos preciso que GB |
| Red Neuronal         | Regresión       | MSE           | 0.01             | Mayor error relativo |
| Árbol de Decisión    | Clasificación   | Accuracy      | 0.73             | Desempeño aceptable |
| Árbol de Decisión    | Clasificación   | Macro F1      | 0.73             | Balance general adecuado |

### 5.3 Ventajas y desventajas (tabla consolidada)
| Modelo            | Ventajas                                                                 | Desventajas                                                                              |
|-------------------|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Árbol de Decisión | Interpretación clara, visualizable, rápido, útil para exploración        | Menor capacidad predictiva; sensible al desbalance; prone a sobreajuste sin pruning       |
| Red Neuronal      | Capta no linealidades complejas; flexible; escalable                     | Menos interpretable; requiere tuning y más cómputo; riesgo de sobre/underfitting          |
| Gradient Boosting | Alta precisión; robusto a outliers moderados; maneja interacciones       | Entrenamiento más lento; hiperparámetros sensibles; puede sobreajustar sin regularización |

### 5.4 Escenarios de aplicación (ampliados)
- **Árbol de Decisión:** Clasificación rápida, informes ejecutivos, filtros tácticos iniciales, explicación transparente a cuerpo técnico.
- **Red Neuronal:** Cuando se anticipa complejidad alta (features derivados de tracking, embeddings de texto, histórico multitemporal), prototipos extensibles o integraciones multimodales.
- **Gradient Boosting:** Predicción numérica crítica (valoración de potencial ofensivo, proyecciones de rendimiento, priorización de fichajes), donde interpretabilidad parcial (importancia de variables, SHAP) es aceptable a cambio de precisión.

### 5.5 Reflexión sobre el aprendizaje obtenido
El proceso permitió comparar enfoques clásicos (árbol), ensemble (boosting) y modernos (red neuronal). Se refuerzan aprendizajes clave:
1. No existe un modelo universalmente superior: depende del objetivo (clasificar vs estimar con máxima precisión) y del contexto.
2. La calidad del preprocesamiento (balanceo, normalización, codificación) influye tanto como el algoritmo.
3. La interpretabilidad es crítica para decisiones tácticas; la precisión lo es para decisiones estratégicas y de inversión.
4. Evaluar múltiples algoritmos aporta evidencia defendible ante stakeholders (técnicos, analistas, dirección deportiva).
5. El sobreajuste puede camuflarse como “desempeño perfecto” en una clase (caso de la clase Media); requiere validar con más datos o cross-validation.

### 5.6 Consideraciones adicionales y próximas mejoras
- Incorporar validación cruzada (k-fold) para robustecer las métricas.
- Probar modelos adicionales: XGBoost, LightGBM, CatBoost (probablemente mejoren aún más a Gradient Boosting estándar).
- Añadir ingeniería de atributos: ratios (goles/90, xG per shot), formas recientes (últimos n partidos).
- Evaluar interpretabilidad avanzada: SHAP para Gradient Boosting y permutation importance para NN.
- Integrar datos de temporadas previas para mejorar generalización temporal.
- Construir pipeline reproducible (scikit-learn Pipeline / MLflow).

## 6. Conclusiones (ampliadas e integradas)
- **Gradient Boosting** es la mejor técnica de las evaluadas para predicción numérica precisa y robusta del aporte ofensivo esperado (`npxG+xAG.1`), ideal para escenarios de scouting avanzado y toma de decisiones de alto impacto.
- **Red Neuronal** ofrece una alternativa flexible y escalable, apropiada si se planea incorporar datos más complejos (temporales, posicionales, embeddings) o ampliar la arquitectura.
- **Árbol de Decisión** aporta interpretabilidad inmediata y segmentación clara para tareas de clasificación de eficiencia, aunque su potencia predictiva en valores continuos es menor.
- El **preprocesamiento correcto** (limpieza, codificación, normalización, balanceo) fue un habilitador crítico del rendimiento alcanzado.
- **Lección clave:** la elección del modelo depende del objetivo final (explicar vs predecir con máxima exactitud), los recursos disponibles y el horizonte de uso (rápido análisis táctico vs proyección estratégica).

---
