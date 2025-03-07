import requests
from bs4 import BeautifulSoup
import logging
import asyncio




# Variables de seguimiento
estadisticas = {
    "total_ofertas": 0,
    "actualizaciones": 0,
    "ultima_actualizacion": "No disponible"
}

# Función para obtener ofertas de empleo
def obtener_ofertas():
    url_base = "https://co.computrabajo.com/empleos-en-cartagena-de-indias?p="
    headers = {"User-Agent": "Mozilla/5.0"}
    ofertas = []  # Se mantiene fuera del bucle para almacenar todas las ofertas
    max_pages = 130  

    for pagina in range(1, max_pages + 1):
        url = url_base + str(pagina)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')
        job_offers = soup.find_all('article', class_='box_offer')
        if not job_offers:
            break  

        # **Se elimina la reinicialización de la lista ofertas aquí**
        
        for offer in job_offers:
            title_tag = offer.find("h1", class_="fwB fs24 mb5 box_detail w100_m")
            title = title_tag.text.strip() if title_tag else None

            if not title:
                title_h2_tag = offer.find("h2", class_="fs18 fwB")
                title = title_h2_tag.a.text.strip() if title_h2_tag and title_h2_tag.a else "Título no disponible"

            company_tag = offer.find("a", class_="fc_base t_ellipsis")
            company = company_tag.text.strip() if company_tag else "Empresa no disponible"

            link_tag = offer.find("a", class_="js-o-link")
            link = "https://co.computrabajo.com" + link_tag["href"] if link_tag else "Enlace no disponible"

            location_tag = offer.find("p", class_="fs16 fc_base mt5")
            location_span = location_tag.find("span", class_="mr10") if location_tag else None
            location = location_span.text.strip() if location_span else "Ubicación no disponible"

            salary_tag = offer.find("div", class_="fs13 mt15")
            salary_span = salary_tag.find("span", class_="dIB mr10") if salary_tag else None
            salary = salary_span.text.strip() if salary_span else "Sueldo no especificado"

            time_tag = offer.find("p", class_="fs13 fc_aux mt15")
            time_posted = time_tag.text.strip() if time_tag else "Tiempo de publicación no disponible"

            featured_tag = offer.find("div", class_="list_dot mb15")
            featured_text = featured_tag.find("span", class_="fc_dest") if featured_tag else None
            offer_type = featured_text.text.strip() if featured_text else "Oferta estándar"

            ofertas.append({
                'Título': title,
                'Empresa': company,
                'Ubicación': location,
                'Sueldo': salary,
                'Publicado': time_posted,
                'Tipo': offer_type,
                'Enlace': link
            })

    estadisticas["total_ofertas"] = len(ofertas)
    return ofertas

# Función para actualizar ofertas

async def tarea_programada():
    print(" Actualizando ofertas...")
    nuevas_ofertas = obtener_ofertas()

    if nuevas_ofertas:
        actualizar_html(nuevas_ofertas)
        mensaje = f"✅ Nueva actualización con {estadisticas['total_ofertas']} ofertas"
        await (mensaje)
    else:
        print("⚠️ No se encontraron nuevas ofertas.")


async def actualizar_periodicamente():
    while True:
        await tarea_programada()
        await asyncio.sleep(3 * 60 * 60)  # Espera 3 horas (en segundos)
        
def actualizar_html(ofertas):
    contenido_html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NeedWork - Ofertas</title>
        <link rel="icon" href="camello.png" type="image/png">

        <style>
            body {{
                font-family: sans-serif;
                margin: 20px;
                background-color: #f4f4f4; /* Color de fondo suave */
            }}
            h1 {{
                text-align: center;
                color: #333; /* Color de texto principal */
            }}
             #job-list-container {{ /* Contenedor para la lista */
                width: 50%; /* Ancho del 50% */
                margin: 0 auto; /* Centrar horizontalmente */
            }}
            .job-item {{
                background-color: white;
                border: 1px solid #ddd; /* Borde sutil */
                margin-bottom: 10px;
                padding: 15px;
                border-radius: 5px; /* Bordes redondeados */
                box-shadow: 2px 2px 5px rgba(0,0,0,0.1); /* Sombra ligera */
                transition: transform 0.2s; /* Transición suave al pasar el mouse */
            }}
            .job-item:hover {{
                transform: scale(1.02); /* Ligero aumento de tamaño al pasar el mouse */
            }}
            .job-title {{
                font-weight: bold;
                margin-bottom: 5px;
                color: #333;
            }}
            .job-details {{
                color: #666; /* Color de texto secundario */
                margin-bottom: 10px;
            }}
            .job-link {{
                display: inline-block;
                background-color: #007bff; /* Color de fondo del enlace */
                color: white;
                padding: 8px 15px;
                text-decoration: none;
                border-radius: 5px;
                transition: background-color 0.3s; /* Transición suave del color de fondo */
            }}
            .job-link:hover {{
                background-color: #0056b3; /* Color de fondo más oscuro al pasar el mouse */
            }}
            #search-container {{
                margin-bottom: 20px;
            }}
            #search-input {{
                width: 100%;
                padding: 10px;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <h1>NeedWork - Colombia</h1>

        <div id="search-container">
            <input type="text" id="search-input" placeholder="Buscar ofertas...">
        </div>
<div id="job-list-container">
        <ul id="job-list">
    """

    for oferta in ofertas:
        contenido_html += f"""
            <li class="job-item">
                <div class="job-title">{oferta['Título']}</div>
                <div class="job-details">
                    <p><strong>Empresa:</strong> {oferta['Empresa']}</p>
                    <p><strong>Ubicación:</strong> {oferta['Ubicación']}</p>
                    <p><strong>Sueldo:</strong> {oferta['Sueldo']}</p>
                    <p><strong>Publicado:</strong> {oferta['Publicado']}</p>
                    <p><strong>Tipo:</strong> {oferta['Tipo']}</p>
                </div>
                <a class="job-link" href="{oferta['Enlace']}" target="_blank">Postularme</a>
            </li>
        """

    contenido_html += """
        </ul>

        <script>
            const searchInput = document.getElementById('search-input');
            const jobList = document.getElementById('job-list');
            const jobItems = jobList.querySelectorAll('.job-item');

            searchInput.addEventListener('input', function(event) {
                const searchTerm = event.target.value.toLowerCase();

                jobItems.forEach(item => {
                    const text = item.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        </script>

    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(contenido_html)

