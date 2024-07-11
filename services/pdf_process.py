from services.pdf_extract_text import PdfExtractText
import spacy
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()
class PdfProcess():
    curriculum = ""
    processing_event=asyncio.Event()
    isProcessing = False
    
    def pre_process(text):
        nlp = spacy.load('en_core_web_md')
        doc = nlp(text)
        
        tokens = [token for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
        
        lemma = [token.lemma_.lower() for token in tokens]
        
        text_lemma = " ".join(lemma)
        
        return text_lemma
    
    def process_pdf():
        PdfProcess.isProcessing = True
        PdfProcess.processing_event.clear()
        
        pdf_path = f"{os.getenv('pdf_path')}{os.getenv('pdf_name')}"
        text_cv = PdfExtractText.extract_text_from_pdf(pdf_path)
        PdfProcess.curriculum=str(PdfProcess.pre_process(text_cv))

        PdfProcess.processing_event.set()
        PdfProcess.isProcessing = False
        
    async def get_curriculum():
        await PdfProcess.wait_processing()
        
        if not PdfProcess.curriculum:
            return "Curriculum not found"
        return PdfProcess.curriculum
        
    async def wait_processing():
        if PdfProcess.isProcessing:
            await PdfProcess.processing_event.wait()
