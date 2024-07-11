from fastapi import FastAPI
from controller.pdf_controller import PdfController
from controller.curriculum_controller import CurriculumController



app = FastAPI()

app.include_router(PdfController.router)
app.include_router(CurriculumController.router)
