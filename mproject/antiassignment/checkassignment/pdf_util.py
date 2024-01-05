from PyPDF2 import PdfReader
from django.shortcuts import render
from PyPDF2 import PdfReader
import pytesseract
import difflib
import io
from PIL import Image
from checkassignment.models import Assignment

def pdf_to_text(pdf_path):
    # Use PyPDF2 to read the PDF
    pdf_reader = PdfReader(pdf_path)
    extracted_text = ""

    for page in pdf_reader.pages:
        # Check if the page contains any text content
        if '/Font' in page['/Resources']:
            extracted_text += page.extract_text()
        else:
            # If no text content, try to extract images and OCR them
            xObject = page['/Resources']['/XObject'].get_object()
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                    data = xObject[obj].get_object().get_data()
                    image = Image.open(io.BytesIO(data))
                    extracted_text += pytesseract.image_to_string(image)

    return extracted_text

def calculate_text_similarity(text1, text2):
    matcher = difflib.SequenceMatcher(None, text1, text2)
    similarity_ratio = matcher.ratio()
    return similarity_ratio

if __name__ == "__main__":
    # Retrieve all assignments from the database
    assignments = Assignment.objects.all()

    # Set a threshold for similarity (e.g., 70%)
    similarity_threshold = 0.7

    similar_assignments = []

    for assignment in assignments:
        # Extract text content from the stored PDF
        stored_text = pdf_to_text(assignment.file.path)

        # Obtain the path to the handwritten PDF from the assignment
        handwritten_pdf_path = assignment.handwritten_pdf.path

        # Extract text content from the handwritten PDF
        handwritten_text = pdf_to_text(handwritten_pdf_path)

        # Calculate similarity
        similarity_percentage = calculate_text_similarity(handwritten_text, stored_text)

        if similarity_percentage >= similarity_threshold:
            similar_assignments.append(assignment)

    if similar_assignments:
        print("These assignments are similar:")
        for assignment in similar_assignments:
            print(f"- Assignment ID: {assignment.id}, Title: {assignment.title}")
    else:
        print("No similar assignments found.")
