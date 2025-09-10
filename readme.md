# 🎲 Visualizador de Resultados de Loterías

Este es un proyecto full-stack que extrae (scrapea) en tiempo real los resultados de varios juegos de lotería y quiniela de Argentina desde el sitio `quinieleando.com.ar`.

La aplicación presenta los datos a través de una API RESTful creada con **Python** y **Flask**, y los consume con una interfaz de usuario moderna, oscura y responsiva construida con **HTML, CSS y JavaScript** puros.

---

## ✨ Características Principales

-   **Scraping en Tiempo Real:** Obtiene los datos más recientes de 4 juegos populares:
    -   Quiniela Nacional
    -   Quiniela de Mendoza
    -   Telekino
    -   Quini 6
-   **Interfaz Interactiva:**
    -   Permite seleccionar el juego a visualizar.
    -   Incluye un selector de fecha (Hoy, Ayer y calendario) para las Quinielas.
    -   Diseño profesional y totalmente responsivo adaptable a cualquier dispositivo.
-   **Modo TV / Dashboard:**
    -   Una vista especial en `http://127.0.0.1:5000/tv` optimizada para pantallas grandes.
    -   Muestra los 4 juegos simultáneamente en una cuadrícula 2x2 sin necesidad de scroll.
    -   **Modo Carrusel:** Permite visualizar cada juego en pantalla completa, rotando automáticamente cada 15 segundos.
    -   **Actualización Automática:** Los datos en el Modo TV se actualizan solos cada 10 minutos.
    -   Soporte para pantalla completa nativa del navegador.

---

## 🛠️ Tecnologías Utilizadas

-   **Backend:**
    -   **Python 3**
    -   **Flask:** Para el servidor web y la API.
    -   **BeautifulSoup4:** Para el parseo del HTML.
    -   **Requests:** Para realizar las peticiones HTTP.
-   **Frontend:**
    -   **HTML5**
    -   **CSS3:** Uso avanzado de Flexbox, Grid, animaciones y variables para un diseño moderno.
    -   **JavaScript (ES6+):** Lógica del cliente, llamadas a la API con `fetch` y manipulación dinámica del DOM.

---

## 📂 Estructura del Proyecto

```
/
├── app.py              # Servidor Flask, API y toda la lógica de scraping
└── templates/
    ├── index.html      # Página principal interactiva con CSS y JS embebidos
    └── tv.html         # Página del modo TV/Dashboard con CSS y JS embebidos
```

---

## 🚀 Instalación y Puesta en Marcha

Para ejecutar este proyecto en tu máquina local, seguí estos pasos:

1.  **Clonar o descargar el proyecto:**
    Asegurate de tener todos los archivos (`app.py`, `templates/index.html`, `templates/tv.html`) en la misma carpeta.

2.  **Crear un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    ```

3.  **Activar el entorno virtual:**
    -   En Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    -   En macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Instalar las dependencias de Python:**
    ```bash
    pip install Flask requests beautifulsoup4 Flask-Cors
    ```

5.  **Ejecutar el servidor:**
    ```bash
    python app.py
    ```
    Si todo va bien, verás un mensaje indicando que el servidor está corriendo en `http://127.0.0.1:5000`.

6.  **Abrir la aplicación:**
    Andá a tu navegador y visitá la dirección **`http://127.0.0.1:5000`**.

---

## 🕹️ Cómo Usar la Aplicación

### Página Principal (`/`)

-   **Seleccionar Juego:** Hacé clic en uno de los botones de juego (Nacional, Mendoza, etc.) para cargar sus resultados.
-   **Seleccionar Fecha (solo para Quinielas):** Una vez seleccionado un juego de Quiniela, aparecerán los controles de fecha. Podés elegir "Hoy", "Ayer" o una fecha específica del calendario.
-   **Acceder al Modo TV:** Hacé clic en el ícono de la televisión (📺) en la esquina superior derecha para ir al dashboard.

### Modo TV (`/tv`)

-   **Vista General:** Por defecto, verás los 4 juegos en una cuadrícula. Los datos se actualizan cada 10 minutos.
-   **Modo Carrusel:** Hacé clic en el botón del carrusel (🎠) para que la vista cambie a pantalla completa y rote entre los juegos cada 15 segundos.
-   **Pantalla Completa:** Usá el botón (⛶) para que la aplicación ocupe toda la pantalla.
-   **Volver:** El botón (↩️) te llevará de regreso a la página principal.