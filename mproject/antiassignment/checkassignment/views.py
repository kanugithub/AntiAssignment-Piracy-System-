from django.http import HttpResponse
from django.shortcuts import redirect, render
from checkassignment.forms import StudentRegistrationForm
from checkassignment.models import Assignment,Student

from PyPDF2 import PdfReader
import difflib
import io
from PIL import Image
import pytesseract
import nltk
from nltk.tokenize import sent_tokenize



nltk.download('punkt')
  #  for sentence tokenization
def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = StudentRegistrationForm()
    return render(request, 'signup.html', {'form': form})

# students/views.py

def student_login(request):
    if request.method == 'POST':
        roll_no = request.POST['roll_no']
        password = request.POST['password']
        student = Student.objects.filter(student_roll_no = roll_no, student_password=password)
        if student:
        
            return redirect('compare_form') 
        else:
            
            return redirect('login')
    return render(request, 'login.html')


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
from checkassignment.models import Assignment



def calculate_text_similarity(text1, text2):
    if not isinstance(text1, (str, bytes)) or not isinstance(text2, (str, bytes)):
        return 0
    sentences1 = sent_tokenize(text1)
    sentences2 = sent_tokenize(text2)

    # Initialize a list to store similarity ratios for each sentence
    sentence_similarity_ratios = []

    for sentence1 in sentences1:
        for sentence2 in sentences2:
            matcher = difflib.SequenceMatcher(None, sentence1, sentence2)
            similarity_ratio = matcher.ratio()
            sentence_similarity_ratios.append(similarity_ratio)

    # Calculate the average similarity ratio for all sentences
    if sentence_similarity_ratios:
        average_similarity = sum(sentence_similarity_ratios) / len(sentence_similarity_ratios)
    else:
        average_similarity = 0

    return average_similarity

   
from django.db.models import F  # Import F for database queries

def compare_form(request):
    if request.method == "POST":
        if 'assignment_pdf' in request.FILES:
            assignment_pdf = request.FILES['assignment_pdf']
            title = request.POST.get('title')
            text = pdf_to_text(assignment_pdf)

            # Check if there are any stored assignments in the database
            stored_assignments = Assignment.objects.all()

            if not stored_assignments:
                # If no stored assignments, save the new assignment without checking
                user = request.user
                new_assignment = Assignment(user=user, extracted_text=text)
                new_assignment.save()
                return HttpResponse("Assignment saved successfully")

            # Check for 100% similarity (exact match) with any stored assignment
            for assignment in stored_assignments:
                if text == assignment.extracted_text:
                    result_message = "Reject (100% Similarity)"
                    return HttpResponse(result_message)

            # If no exact match is found, proceed with similarity checking
            similarity_threshold = 0.7 

            is_similar = False
            for assignment in stored_assignments:
                similarity = calculate_text_similarity(text, assignment.extracted_text)
                if similarity >= similarity_threshold:
                    is_similar = True
                    break  # If it's similar to any stored assignment, exit the loop

            if is_similar:
                similarity_percentage = similarity * 100
                result_message = f"Reject (Similarity: {similarity_percentage:.2f}%)"
                return HttpResponse(result_message)
            else:
                # Accept the assignment and save it to the database
                user = request.user
                new_assignment = Assignment(user=user, extracted_text=text)
                new_assignment.save()
                similarity_percentage = calculate_text_similarity(text, new_assignment.extracted_text) * 100
                result_message = f"Accept (Similarity: {similarity_percentage:.2f}%)"
                return HttpResponse(result_message)

    return render(request, 'compare_form.html')
