from fastapi import APIRouter
from services.pdf_process import PdfProcess
from services.curriculum_classifier import CurriculumClassifier
from services.curriculum_classifier import CurriculumClassifier

class CurriculumController:
    
    router = APIRouter(tags=['curriculum'])
    
    @router.get("/curriculum")
    async def getInfo(): 
        return await PdfProcess.get_curriculum()
    
    @router.get("/curriculum/classification")
    async def get_classification(): 
        return await CurriculumClassifier.predict()

