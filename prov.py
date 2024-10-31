import os
import random
import requests
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def check_for_updates(current_version):
    """
    Kontrollerar om en ny version är tillgänglig på GitHub.
    Returnerar True om en uppdatering finns, annars False.
    """
    version_url = "https://raw.githubusercontent.com/Gulhashsoppa/Prov-ssy020/main/Version.txt"
    response = requests.get(version_url)
    
    # Kontrollera att begäran var framgångsrik innan bearbetning
    if response.status_code == 200:
        latest_version = response.text.strip()
        if latest_version != current_version:
            print(f"Ny version tillgänglig: {latest_version} (Nuvarande version: {current_version})")
            return True
    else:
        print("Kunde inte kontrollera uppdateringar.")
    
    print("Programmet är redan uppdaterat.")
    return False

def download_latest_version():
    """
    Laddar ner den senaste .exe-filen från GitHub.
    """
    exe_url = "https://github.com/Gulhashsoppa/Prov-ssy020/releases/latest/download/program.exe"
    response = requests.get(exe_url)
    
    if response.status_code == 200:
        with open("program_ny.exe", "wb") as file:
            file.write(response.content)
        print("Den senaste versionen har laddats ner som 'program_ny.exe'.")
        
        # Byt ut den gamla .exe-filen med den nya
        os.replace("program_ny.exe", "program.exe")
        print("Programmet har uppdaterats.")
    else:
        print("Kunde inte ladda ner den senaste versionen.")

def get_random_images_from_folders(base_folder, max_images=7):
    selected_images = []
    
    for i in range(1, 11):
        folder_path = os.path.join(base_folder, str(i))
        print("Looking in folder:", folder_path)
        if os.path.isdir(folder_path):
            images = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
            print("Found images:", images)
            if images:
                selected_image = random.choice(images[:max_images])
                selected_images.append(os.path.join(folder_path, selected_image))
        else:
            print(f"Warning: Folder {folder_path} is missing or empty.")
    
    return selected_images

def create_pdf_with_images(image_paths, output_pdf_path):
    pdf = canvas.Canvas(output_pdf_path, pagesize=A4)
    width, height = A4
    current_y = height - 50
    max_width = width - 100
    
    for img_path in image_paths:
        img = Image.open(img_path)
        
        img_width, img_height = img.size
        scaling_factor = min(max_width / img_width, 1)
        new_width = int(img_width * scaling_factor)
        new_height = int(img_height * scaling_factor)
        img = img.resize((new_width, new_height), Image.LANCZOS)

        if current_y - new_height < 50:
            pdf.showPage()
            current_y = height - 50
        
        pdf.drawImage(img_path, 50, current_y - new_height, width=new_width, height=new_height)
        current_y -= new_height + 20
        
    pdf.save()

# Ange din nuvarande version
current_version = "1.0.0"

# Kontrollera om en uppdatering finns
if check_for_updates(current_version):
    download_latest_version()
    print("Programmet startas om efter uppdatering.")
    os.execv("program.exe", ["program.exe"])  # Starta om programmet efter uppdatering
else:
    base_folder = "d:\Prov"
    output_pdf_path = "slumpmässiga_frågor.pdf"

    selected_images = get_random_images_from_folders(base_folder)
    print("Selected images:", selected_images)

    create_pdf_with_images(selected_images, output_pdf_path)

    print("En ny PDF har skapats med slumpmässigt valda frågebilder!")
