import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import shutil

# Crear la carpeta "libros" si no existe
if not os.path.exists("libros"):
    os.makedirs("libros")

# Crear la carpeta "temporal" si no existe
if not os.path.exists("temporal"):
    os.makedirs("temporal")

# URL base
base_url = "https://www.conaliteg.sep.gob.mx/"

# URL de la página principal
main_url = "https://www.conaliteg.sep.gob.mx/primaria.html"

# Realizar solicitud HTTP a la página principal
response = requests.get(main_url)
soup = BeautifulSoup(response.content, "html.parser")

# Encontrar y almacenar enlaces
links = soup.find_all("a", href=True)
valid_links = []

for link in links:
    if "2023/" in link["href"] and link["href"].endswith(".htm"):
        file_name = link["href"].split("/")[-1]
        folder_name = file_name.split(".")[0][-5:]
        valid_links.append(folder_name)

# Crear subcarpetas con los nombres almacenados
for folder_name in valid_links:
    subfolder_path = os.path.join("libros", folder_name)
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

# URL base de las imágenes
image_base_url = "https://www.conaliteg.sep.gob.mx/2023/c/{}/{}.jpg"

# Descargar y guardar las imágenes en la carpeta "temporal"
for folder_name in valid_links:
    for image_number in range(401):
        image_download_url = image_base_url.format(folder_name, str(image_number).zfill(3))
        image_response = requests.get(image_download_url)
        if image_response.status_code == 200:
            image_path = os.path.join("temporal", "{}_{:03d}.jpg".format(folder_name, image_number))
            with open(image_path, "wb") as f:
                f.write(image_response.content)

print("Descargas completadas")
# Mover archivos de la carpeta temporal a las subcarpetas correspondientes en "libros"
def move_files_to_folders():
    temporal_folder = "temporal"
    libros_folder = "libros"
    
    # Listar los archivos en la carpeta temporal
    for file_name in os.listdir(temporal_folder):
        if file_name.endswith(".jpg"):
            # Obtener la cadena de 5 letras del nombre de archivo
            folder_name = file_name.split("_")[0]
            
            # Obtener la ruta completa del archivo en temporal
            temp_file_path = os.path.join(temporal_folder, file_name)
            
            # Obtener la ruta completa de la subcarpeta en libros
            subfolder_path = os.path.join(libros_folder, folder_name)
            
            # Crear la subcarpeta si no existe
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
            
            # Mover el archivo a la subcarpeta en libros
            new_file_path = os.path.join(subfolder_path, file_name)
            shutil.move(temp_file_path, new_file_path)
            
    print("Movimiento de archivos completado.")

move_files_to_folders()