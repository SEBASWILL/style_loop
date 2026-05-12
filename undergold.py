

import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

url = "https://undergoldapparel.com/collections/all-hombre"

# Crear carpeta
os.makedirs("imagenes", exist_ok=True)

# Obtener HTML
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

links = []

# Buscar SOLO imágenes primary
imagenes = soup.select("img.product-card__image--primary")

for img in imagenes:
    src = img.get("src")

    if not src:
        continue

    # Convertir // en https://
    if src.startswith("//"):
        src = "https:" + src

    links.append(src)

# Quitar duplicados
links = list(set(links))

print(f"Descargando {len(links)} imágenes...\n")

# Descargar y guardar como PNG
for i, link in enumerate(links, start=1):
    try:
        print(f"[{i}/{len(links)}] Descargando...")

        img_response = requests.get(link)

        image = Image.open(BytesIO(img_response.content)).convert("RGBA")

        nombre = f"imagen_{i}.png"

        ruta = os.path.join("imagenes", nombre)

        image.save(ruta, "PNG")

        print(f"Guardada: {nombre}")

    except Exception as e:
        print(f"Error con {link}")
        print(e)

print("\nProceso terminado.")