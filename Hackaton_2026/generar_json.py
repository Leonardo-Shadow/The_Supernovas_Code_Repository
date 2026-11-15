import json
import pandas as pd
from modelo import entrenar_y_predecir_zona
from rutas import OptimizadorRutasMarte


def actualizar_json_por_seleccion(poi_id_seleccionado):
  df = pd.read_csv("CSV/dataset_marte_ml.csv")
  
  # Buscar la zona específica elegida por el usuario
  fila_zona = df[df["poi_id"] == poi_id_seleccionado]
  if fila_zona.empty:
    print(f"Zona {poi_id_seleccionado} no encontrada.")
    return

  row = fila_zona.iloc[0]
  lat = row["latitud"]
  lon = row["longitud"]
  elevacion = row["elevacion_m"]
  nombre_poi = row["poi_nombre"]

  # 1. Obtener predicciones de modelo.py (Módulo 3)
  resultado_ml = entrenar_y_predecir_zona(lat, lon, elevacion)

  # 2. Obtener recomendaciones tácticas de rutas.py (Módulo 4)
  optimizador = OptimizadorRutasMarte()
  pendiente_est = 14.0 if "Ridge" in nombre_poi or "Hill" in nombre_poi else 9.0
  
  recomendaciones_lista = optimizador._generar_recomendaciones_supervivencia(
      nivel_riesgo=resultado_ml["nivel_riesgo"],
      radiacion_mSv=resultado_ml["radiacion_estimada_mSv"],
      pendiente_grados=pendiente_est,
  )
  
  estrategia_completa = f"{resultado_ml['recomendacion_tactica']} " + " | ".join(recomendaciones_lista)

  # 3. Estructurar el JSON enfocado en la selección del usuario
  datos_seleccion = {
      poi_id_seleccionado: {
          "latitud": lat,
          "longitud": lon,
          "nombre_region": nombre_poi,
          "temperatura_promedio": f"{resultado_ml['temperatura_estimada_c']} °C",
          "nivel_radiacion": f"{resultado_ml['radiacion_estimada_mSv']} mSv/día",
          "riesgo_operativo": resultado_ml["nivel_riesgo"],
          "estrategia_ruta": estrategia_completa,
      }
  }

  # Guardar el JSON actualizado
  with open("predicciones.json", "w", encoding="utf-8") as f:
    json.dump(datos_seleccion, f, ensure_ascii=False, indent=4)

  print(f"¡JSON actualizado dinámicamente para la zona: {nombre_poi}!")


if __name__ == "__main__":
  # Prueba por defecto
  actualizar_json_por_seleccion("yellowknife_bay")