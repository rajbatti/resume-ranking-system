
import os
import mimetypes
from PyPDF2 import PdfReader 

import docx
from PIL import Image
import pytesseract
import pandas as pd

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file) 
    print(len(reader.pages)) 
        
        # getting a specific page from the pdf file 
    page = reader.pages[0] 
        
        # extracting text from page 
    text = page.extract_text() 
    print(text)
    return text



   
    

    
        

# Function to extract text from Word document
def extract_text_from_docx(file_path):
    text = ""
    doc = docx.Document(file_path)
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    
    return text
    
# Function to extract text from an image (requires pytesseract)
def extract_text_from_image(file_path):
    text = ""
    try:
        with Image.open(file_path) as img:
            text = pytesseract.image_to_string(img)
    except Exception as e:
        print(f"Error extracting text from image: {e}")
    return text

resume_dir = r"C:\Users\B RAJESH\Desktop\resume2"

folder_path =resume_dir
data=[]
# Traverse the folder and detect file types
for root, dirs, files in os.walk(folder_path):
    for filename in files:
        file_path = os.path.join(root, filename)
        mime_type, _ = mimetypes.guess_type(file_path)
        print(file_path)
        if mime_type is not None:
            if mime_type == 'application/pdf':
                text = extract_text_from_pdf(file_path)
                data.append(text)
            elif file_path.endswith(".docx"):
                text = extract_text_from_docx(file_path)
                data.append(text)
            elif mime_type.startswith('image/'):
                text = extract_text_from_image(file_path)
                data.append(text)
            else:
                text = "Unsupported file type"
            print(text)
          
dt={}
for i in range(len(data)):
    dt[str(i)]=data[i]
df = pd.DataFrame(data,columns=["text"])
print(df)

# Save the dataset to a CSV file
df.to_csv("resall.csv", index=False)
            


