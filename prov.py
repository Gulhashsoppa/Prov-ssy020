import os
import random
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def get_random_images_from_folders(base_folder, max_images=7):
    selected_images = []
    
    # Loop through folders `1`, `2`, etc., up to the number of categories in base_folder
    for i in range(1, 11):  # Adjust the range to match your subfolder count if it's 1-3
        folder_path = os.path.join(base_folder, str(i))
        print("Looking in folder:", folder_path)  # Debug: show folder path
        if os.path.isdir(folder_path):
            images = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
            print("Found images:", images)  # Debug: show found images
            if images:
                selected_image = random.choice(images[:max_images])
                selected_images.append(os.path.join(folder_path, selected_image))
        else:
            print(f"Warning: Folder {folder_path} is missing or empty.")
    
    return selected_images

def create_pdf_with_images(image_paths, output_pdf_path):
    pdf = canvas.Canvas(output_pdf_path, pagesize=A4)
    width, height = A4
    current_y = height - 50  # Start position for images
    max_width = width - 100  # Width margin
    
    for img_path in image_paths:
        img = Image.open(img_path)
        
        # Resize image if it's wider than page width
        img_width, img_height = img.size
        scaling_factor = min(max_width / img_width, 1)  # Scale down if larger than max_width
        new_width = int(img_width * scaling_factor)
        new_height = int(img_height * scaling_factor)
        img = img.resize((new_width, new_height), Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS

        # Check if there's enough space on the page
        if current_y - new_height < 50:
            pdf.showPage()  # Start a new page if space is insufficient
            current_y = height - 50  # Reset position for the new page
        
        pdf.drawImage(img_path, 50, current_y - new_height, width=new_width, height=new_height)
        current_y -= new_height + 20  # Move position down for the next image
        
    pdf.save()

# Set base_folder to the folder name in the same directory
base_folder = "d:\Prov"  # Use raw string to avoid invalid escape sequence issues
output_pdf_path = "slumpmässiga_frågor.pdf"

# Step 1: Select random images from folders
selected_images = get_random_images_from_folders(base_folder)
print("Selected images:", selected_images)  # Debug: show selected images

# Step 2: Create PDF with the selected images
create_pdf_with_images(selected_images, output_pdf_path)

print("A new PDF has been created with randomly selected question images!")
