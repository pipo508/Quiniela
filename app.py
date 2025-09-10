import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from datetime import datetime

# --- Configuración de la aplicación Flask ---
app = Flask(__name__)
CORS(app)

# --- SCRAPERS ---

def scrape_quiniela(url):
    """Scraper para Quinielas, ahora detecta si no hay sorteos."""
    resultados = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # DETECCIÓN DE "SIN SORTEOS"
        no_results_alert = soup.find('p', class_='alert-warning')
        if no_results_alert and "Aún no tenemos información" in no_results_alert.text:
            return [] # Devuelve una lista vacía si no hay resultados

        tablas_resultados = soup.find_all('table', class_='table-bordered')
        for tabla in tablas_resultados:
            h3_tag = tabla.find('h3')
            if not h3_tag: continue
            
            nombre_sorteo_completo = h3_tag.text.strip()
            partes_nombre = nombre_sorteo_completo.split(',')
            nombre_sorteo = partes_nombre[0].strip()
            fecha_str = nombre_sorteo_completo.split('.')[-1].strip() if '.' in nombre_sorteo_completo else "Fecha no disponible"
            
            numeros_tags = tabla.find_all('span', class_='nro')
            numeros_lista = [num.text.strip() for num in numeros_tags]
            
            if numeros_lista:
                resultados.append({"sorteo": nombre_sorteo, "fecha": fecha_str, "numeros": numeros_lista})
    except Exception as e:
        print(f"Error en scrape_quiniela ({url}): {e}")
        return None # Devuelve None si hay un error de conexión o scraping
    return resultados

def scrape_telekino(url):
    """Scraper para la página de Telekino."""
    resultados = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        fecha_general = soup.find('h3').text.strip() if soup.find('h3') else "Fecha no disponible"
        tablas = soup.find_all('table', class_='table-bordered')
        for tabla in tablas:
            caption_tag = tabla.find('caption')
            if not caption_tag: continue
            nombre_sorteo = caption_tag.text.strip()
            numeros_tags = tabla.find_all('span', class_='numero')
            numeros_lista = [num.text.strip() for num in numeros_tags]
            if numeros_lista:
                resultados.append({"sorteo": nombre_sorteo, "fecha": fecha_general, "numeros": numeros_lista})
    except Exception as e:
        print(f"Error en scrape_telekino: {e}")
        return None
    return resultados

def scrape_quini6(url):
    """Scraper para la página de Quini 6."""
    resultados = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        tabla_principal = soup.find('table', class_='table-striped')
        caption_general = tabla_principal.find('caption').text.strip() if tabla_principal.find('caption') else "Info no disponible"
        sorteos_th = tabla_principal.find_all('th', class_='lead')
        for th in sorteos_th:
            nombre_sorteo = th.text.strip()
            numeros_tr = th.find_parent('tr').find_next_sibling('tr')
            if "Pozo extra" in nombre_sorteo:
                numeros_lista = []
                siguiente_tr = numeros_tr
                for _ in range(3):
                    if siguiente_tr:
                        numeros_tags = siguiente_tr.find_all('span', class_='numero')
                        numeros_lista.extend([num.text.strip() for num in numeros_tags])
                        siguiente_tr = siguiente_tr.find_next_sibling('tr')
            else:
                numeros_tags = numeros_tr.find_all('span', class_='numero')
                numeros_lista = [num.text.strip() for num in numeros_tags]
            if numeros_lista:
                resultados.append({"sorteo": nombre_sorteo, "fecha": caption_general, "numeros": numeros_lista})
    except Exception as e:
        print(f"Error en scrape_quini6: {e}")
        return None
    return resultados

# --- Rutas ---
@app.route("/")
def home():
    """Ruta para la página principal interactiva."""
    return render_template("index.html")

@app.route("/tv")
def tv_mode():
    """Ruta para el modo TV."""
    return render_template("tv.html")

@app.route("/api/resultados/<juego>/<fecha>")
def get_resultados(juego, fecha):
    """API actualizada para manejar juegos y fechas."""
    datos = None
    
    if juego in ["nacional", "mendoza"]:
        base_url = f"https://quinieleando.com.ar/quinielas/{juego}"
        if fecha == "hoy":
            url = f"{base_url}/resultados-de-hoy"
        elif fecha == "ayer":
            url = f"{base_url}/resultados-de-ayer"
        else:
            # Asume que la fecha viene en formato YYYY-MM-DD y la convierte a DD-MM-YYYY
            try:
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
                fecha_formateada = fecha_obj.strftime("%d-%m-%Y")
                url = f"{base_url}/resultados-del-{fecha_formateada}"
            except ValueError:
                return jsonify({"error": "Formato de fecha inválido. Usar YYYY-MM-DD"}), 400
        datos = scrape_quiniela(url)
    
    elif juego == "telekino" and fecha == "ultimo":
        url = "https://quinieleando.com.ar/telekino/resultados/ultimo-sorteo"
        datos = scrape_telekino(url)
    
    elif juego == "quini6" and fecha == "ultimo":
        url = "https://quinieleando.com.ar/quini6/resultados/ultimo-sorteo"
        datos = scrape_quini6(url)
    
    else:
        return jsonify({"error": "Juego o fecha no válidos para la consulta"}), 404
        
    if datos is not None:
        return jsonify(datos)
    else:
        return jsonify({"error": f"No se pudieron obtener los resultados de {juego}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)