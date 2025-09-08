import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from imblearn.over_sampling import RandomOverSampler

df=pd.read_csv('fbref_PL_2024-25.csv')

#Variable a predecir

def crear_eficiencia(df):
    
    df_filtrado=df[df['Min']>=270].copy()
    
    df_filtrado['xG_safe']=df_filtrado['npxG'].replace(0,0.1)
    df_filtrado['xAG_safe']=df_filtrado['xAG'].replace(0,0.1)
    
    goles_sin_penales = df_filtrado['Gls']-df_filtrado['G-PK']
    eficiencia_goles=goles_sin_penales/df_filtrado['xG_safe']
    eficiencia_asistencias=df_filtrado['Ast']/df_filtrado['xAG_safe']
    
    eficiencia=[]
    for i in range(len(df_filtrado)):
        
         if eficiencia_goles.iloc[i]  > 1.2 or eficiencia_asistencias.iloc[i]>1.2:
            eficiencia.append('Alta')
         elif eficiencia_goles.iloc[i] < 0.7 or eficiencia_asistencias.iloc[i]<0.7:
            eficiencia.append('Baja')
         else:
             eficiencia.append('Media')       
    df_filtrado['Eficiencia']=eficiencia
    
    return df_filtrado
    
    
def preparar_variables(df):
    
    variables_numericas = [
        'Age',
        'Min',
        'PrgC',
        'PrgP'
    ]
    
    df['Minutos_por_partido']= df['Min'] / df['MP']
    df['Es_titular']=(df['Starts']/df['MP'])>0.7
    
    variables_numericas.append('Minutos_por_partido')
    
    pos_num={'DF':1,'MF':2,'FW':3}
    df['pos_numerada']=df['Pos'].map(pos_num)
    variables_numericas.append('pos_numerada')
    
    df['Es_titular_num']=df['Es_titular'].astype(int)
    variables_numericas.append('Es_titular_num')
    
    X = df[variables_numericas]
    y = df['Eficiencia']
    
    return X,y,variables_numericas

def entrenar_modelo(X,y):
    # Balancear las clases
    ros = RandomOverSampler(random_state=42)
    X_balanceado, y_balanceado = ros.fit_resample(X, y)
    
    # Partir los datos balanceados
    X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(
        X_balanceado, y_balanceado, test_size=0.2, random_state=42
    )
    
    modelo = DecisionTreeClassifier(
        max_depth=5,
        min_samples_leaf=5,
        random_state=42
    )
    
    modelo.fit(X_entrenamiento, y_entrenamiento)
    
    predicciones = modelo.predict(X_prueba)
    precision = accuracy_score(y_prueba, predicciones)
    
    return modelo, X_prueba, y_prueba, predicciones

def ver_resultado(y_real, y_predicho, modelo=None, X_prueba=None, nombres_variables=None):
    print(classification_report(y_real, y_predicho))

    # Matriz de confusión
    cm = confusion_matrix(y_real, y_predicho, labels=modelo.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=modelo.classes_)
    disp.plot(cmap=plt.cm.Blues)
    plt.title("Matriz de confusión")
    plt.show()

    # Importancia de variables
    if modelo is not None and nombres_variables is not None:
        importancias = modelo.feature_importances_
        plt.figure(figsize=(8, 4))
        plt.barh(nombres_variables, importancias)
        plt.xlabel("Importancia")
        plt.title("Importancia de variables")
        plt.tight_layout()
        plt.show()

def main():
    df_procesado = crear_eficiencia(df)
    X, y, nombres_variables = preparar_variables(df_procesado)
    modelo, X_prueba, Y_prueba, predicciones = entrenar_modelo(X, y)
    ver_resultado(Y_prueba, predicciones, modelo, X_prueba, nombres_variables)

if __name__ == "__main__":
    main()