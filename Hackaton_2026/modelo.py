import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures

def entrenar_y_predecir_zona(lat_nueva, lon_nueva, elevacion_nueva, ruta_csv="CSV/dataset_marte_ml.csv"):
    # 1. Cargar el dataset que generamos desde el CSV
    try:
        df = pd.read_csv(ruta_csv)
    except FileNotFoundError:
        print(
            f"Error: No se encontró el archivo '{ruta_csv}' en el directorio."
            " Verifique la ruta."
        )
        return None

    if df.empty:
        print("Aviso: El dataset está vacío.")
        return None

    # 2. Definir Variables Independientes (X) y Dependientes (y)
    X = df[["latitud", "longitud", "elevacion_m"]].values
    y_temp = df["temp_promedio_c"].values
    y_rad = df["radiacion_mSv_dia"].values

    # 3. Aplicar Regresión Polinomial (Grado 2) para capturar mejor las curvas físicas del terreno
    poly = PolynomialFeatures(degree=2, include_bias=False)
    X_poly = poly.fit_transform(X)

    # 4. Entrenar los modelos con Scikit-Learn
    modelo_temp = LinearRegression()
    modelo_temp.fit(X_poly, y_temp)

    modelo_rad = LinearRegression()
    modelo_rad.fit(X_poly, y_rad)

    # 5. Predecir para la nueva coordenada ingresada
    X_nuevo = np.array([[lat_nueva, lon_nueva, elevacion_nueva]])
    X_nuevo_poly = poly.transform(X_nuevo)

    temp_predicha = float(modelo_temp.predict(X_nuevo_poly)[0])
    rad_predicha = float(modelo_rad.predict(X_nuevo_poly)[0])

    # 6. Lógica de Riesgo (Módulo 3 del proyecto)
    if rad_predicha > 0.68 or temp_predicha < -52.0:
        nivel_riesgo = "Crítico"
        alerta = (
            "¡Alerta de modelo ML! Radiación elevada o temperatura extrema. Limitar"
            " EVA."
        )
    else:
        nivel_riesgo = "Moderado"
        alerta = "Condiciones estables de acuerdo al modelo histórico."

    # Resultado empaquetado listo para el pipeline
    resultado = {
        "coordenadas_consultadas": {"lat": lat_nueva, "lon": lon_nueva},
        "temperatura_estimada_c": round(temp_predicha, 2),
        "radiacion_estimada_mSv": round(rad_predicha, 2),
        "nivel_riesgo": nivel_riesgo,
        "recomendacion_tactica": alerta,
    }

    return resultado

# Ejemplo de prueba independiente
if __name__ == "__main__":
    print("--- PRUEBA UNITARIA DE MODELO.PY ---")
    punto_prueba = entrenar_y_predecir_zona(
        lat_nueva=-4.58, lon_nueva=137.44, elevacion_nueva=-4500
    )
    print(punto_prueba)