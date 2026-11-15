import json
import numpy as np

class OptimizadorRutasMarte:
    def __init__(self, archivo_json="predicciones.json"):
        try:
            with open(archivo_json, "r", encoding="utf-8") as f:
                self.datos_marte = json.load(f)
        except FileNotFoundError:
            self.datos_marte = {}
            print(
                f"Aviso: No se encontró '{archivo_json}'. Asegúrate de generarlo"
                " primero."
            )

    def _generar_recomendaciones_supervivencia(self, nivel_riesgo, radiacion_mSv, pendiente_grados):
        recomendaciones = []
        # 1. Protocolo de Radiación (Basado en datos del Módulo 3)
        if radiacion_mSv > 0.68:
            recomendaciones.append(
                "⚠️ ALERTA DE RADIACIÓN: Niveles elevados detectados. Mantenerse"
                " cerca de formaciones rocosas protectoras. Límite estricto de"
                " excursión EVA: 4 horas máx."
            )
        else:
            recomendaciones.append(
            "✔️ Radiación en niveles operacionales estables para tránsito"
            " estándar."
            )

        # 2. Protocolo Topográfico y de Pendientes
        if pendiente_grados > 15:
            recomendaciones.append(
            "🛑 PELIGRO TOPOGRÁFICO: Pendiente superior a 15° (terreno irregular o"
            " dunas inestables). Se prohíbe el tránsito sin arnés de sujeción o"
            " apoyo de rover de carga."
            )
        else:
            recomendaciones.append(
                "✔️ Terreno con pendiente transitable para desplazamiento a pie con"
                " equipo estándar."
            )

        # 3. Protocolo Operativo ante Tormentas de Polvo y Visibilidad
        recomendaciones.append(
            "🌪️ PROTOCOLO EÓLICO: En caso de reducción de visibilidad por"
            " levantamiento de polvo (Dust Devils o tormenta), abortar objetivos"
            " secundarios y activar baliza de retorno inmediato al hábitat."
        )

        # 4. Gestión Térmica del Traje (PLSS)
        recomendaciones.append(
            "🌡️ GESTIÓN TÉRMICA: Retornar antes de agotar el 50% de la reserva"
            " energética del traje para garantizar margen ante descensos térmicos"
            " nocturnos extremos."
        )

        return recomendaciones

    def calcular_ruta_segura(self, origen_id, destino_id, pendiente_estimada_grados=10.0):
        if (
            origen_id not in self.datos_marte or destino_id not in self.datos_marte):
            return {"error": "Punto de origen o destino no encontrado en el dataset."}

        origen = self.datos_marte[origen_id]
        destino = self.datos_marte[destino_id]

        # Extracción segura de coordenadas geográficas
        lat1, lon1 = (
            origen["coordenadas_consultadas"]["lat"],
            origen["coordenadas_consultadas"]["lon"],
        )
        lat2, lon2 = (
            destino["coordenadas_consultadas"]["lat"],
            destino["coordenadas_consultadas"]["lon"],
        )

        # Simulación de distancia euclidiana basada en coordenadas a kilómetros en Marte
        distancia_base_km = np.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) * 59.5
        
        # Evaluando penalizaciones por riesgo ambiental del destino (Módulo 3)
        nivel_riesgo_destino = destino.get("nivel_riesgo", "Moderado")
        radiacion_destino = destino.get("radiacion_estimada_mSv", 0.70)

        penalizacion_riesgo = 1.0
        if "Crítico" in nivel_riesgo_destino or radiacion_destino > 0.68:
            penalizacion_riesgo = 2.0  # Penaliza rutas hacia zonas peligrosas

        distancia_ponderada = distancia_base_km * penalizacion_riesgo

        # Generación de puntos intermedios (Lista de coordenadas para la ruta)
        puntos_intermedios = [
            {
                "lat": lat1,
                "lon": lon1,
                "etapa": f"Inicio en {origen.get('nombre', origen_id)}",
            },
            {
                "lat": round((lat1 + lat2) / 2, 4),
                "lon": round((lon1 + lon2) / 2, 4),
                "etapa": "Punto de Control Táctico (Evasión de obstáculos)",
            },
            {
                "lat": lat2,
                "lon": lon2,
                "etapa": f"Llegada a {destino.get('nombre', destino_id)}",
            },
        ]

        # Generar el bloque completo de recomendaciones tácticas
        estrategias_supervivencia = self._generar_recomendaciones_supervivencia(
            nivel_riesgo=nivel_riesgo_destino,
            radiacion_mSv=radiacion_destino,
            pendiente_grados=pendiente_estimada_grados,
        )

        # RF-4.3: Reporte o resumen táctico de la ruta
        reporte_tactico = {
            "mision_origen": origen.get("nombre", origen_id),
            "mision_destino": destino.get("nombre", destino_id),
            "distancia_estimada_km": round(distancia_base_km, 2),
            "distancia_ponderada_riesgo": round(distancia_ponderada, 2),
            "nivel_dificultad": (
                "Alto" if penalizacion_riesgo > 1.0 else "Moderado-Bajo"
            ),
            "evaluacion_riesgo_destino": nivel_riesgo_destino,
            "coordenadas_ruta_geojson": puntos_intermedios,
            "protocolos_supervivencia_eva": estrategias_supervivencia,
        }

        return reporte_tactico

# Ejemplo de prueba si ejecutas este archivo directamente
if __name__ == "__main__":
  optimizador = OptimizadorRutasMarte()
  print("--- PRUEBA DE CÁLCULO DE RUTA TÁCTICA Y SUPERVIVENCIA ---")
  resultado_ruta = optimizador.calcular_ruta_segura(
      origen_id="bradbury_landing",
      destino_id="yellowknife_bay",
      pendiente_estimada_grados=12.0,
  )
  print(json.dumps(resultado_ruta, indent=4, ensure_ascii=False))
