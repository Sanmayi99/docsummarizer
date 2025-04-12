from django.shortcuts import render
from transformers import pipeline
from docx import Document

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text_from_docx(file):
    doc = Document(file)
    full_text = [para.text for para in doc.paragraphs if para.text.strip() != '']
    return ' '.join(full_text)

def home(request):
    summary = ""
    if request.method == "POST" and request.FILES.get("doc_file"):
        doc_file = request.FILES["doc_file"]
        text = extract_text_from_docx(doc_file)
        result = summarizer(text, max_length=500, min_length=150, do_sample=False)
        summary = result[0]['summary_text']
    return render(request, "home.html", {"summary": summary})