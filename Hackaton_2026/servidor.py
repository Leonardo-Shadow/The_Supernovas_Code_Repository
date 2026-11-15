from datetime import datetime
import json
from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
from modelo import entrenar_y_predecir_zona
from rutas import OptimizadorRutasMarte

app = Flask(__name__)
CORS(app)

optimizador = OptimizadorRutasMarte()


# Ruta principal que sirve tu página web
@app.route("/")
def inicio():
    with open("index_generado.html", "r", encoding="utf-8") as f:
        return f.read()


# Ruta que recibe el clic del mapa, ejecuta ML y actualiza el JSON
@app.route("/predecir", methods=["POST"])
def predecir_zona():
    datos_entrada = request.json
    lat = float(datos_entrada.get("latitud", 0))
    lon = float(datos_entrada.get("longitud", 0))
    elevacion = float(datos_entrada.get("elevacion", -2500))
    nombre_poi = datos_entrada.get("nombre_region", "Zona Desconocida")
    poi_id = datos_entrada.get("poi_id", "zona_seleccionada")

    # 1. Ejecutar Módulo 3 (Machine Learning en vivo)
    resultado_ml = entrenar_y_predecir_zona(lat, lon, elevacion)

    # 2. Ejecutar Módulo 4 (Rutas y supervivencia en vivo)
    pendiente_est = (
        14.0 if ("Ridge" in nombre_poi or "Hill" in nombre_poi) else 9.0
    )
    recs = optimizador._generar_recomendaciones_supervivencia(
        nivel_riesgo=resultado_ml["nivel_riesgo"],
        radiacion_mSv=resultado_ml["radiacion_estimada_mSv"],
        pendiente_grados=pendiente_est,
    )
    estrategia = f"{resultado_ml['recomendacion_tactica']} " + " | ".join(recs)

    # 3. Estructurar la respuesta
    resultado_final = {
        "ultima_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "poi_id": poi_id,
        "nombre_region": nombre_poi,
        "latitud": lat,
        "longitud": lon,
        "temperatura_promedio": f"{resultado_ml['temperatura_estimada_c']} °C",
        "nivel_radiacion": f"{resultado_ml['radiacion_estimada_mSv']} mSv/día",
        "riesgo_operativo": resultado_ml["nivel_riesgo"],
        "estrategia_ruta": estrategia,
    }

    # 4. Escribir y actualizar físicamente el archivo predicciones.json en tu carpeta
    with open("predicciones.json", "w", encoding="utf-8") as f:
        json.dump(resultado_final, f, ensure_ascii=False, indent=4)

    print(f"✅ Archivo predicciones.json actualizado para: {nombre_poi}")
    return jsonify(resultado_final)


if __name__ == "__main__":
    print("🚀 Servidor Táctico NASA iniciado en: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)