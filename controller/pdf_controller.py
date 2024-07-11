from services.pdf_process import PdfProcess
from services.pdf_service import PdfService
from fastapi import APIRouter, File, UploadFile, BackgroundTasks


class PdfController:

    router = APIRouter(tags=['pdf'])
    
    @router.post("/pdf")
    async def upload_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)): 
        await PdfService.create_upload_pdf(file)
        background_tasks.add_task(PdfProcess.process_pdf)
        return {"message": "PDF uploaded successfully"}

    @router.get("/pdf/{filename}")
    def get_pdf(filename: str): 
        return PdfService.get_pdf(filename)

    @router.get("/pdf")
    def list_pdfs(): 
        return {"files": PdfService.list_pdfs()}
        
    @router.delete("/pdf/{filename}")
    def delete_pdf(filename: str): 
        PdfService.delete_pdf(filename)
        return {"detail": f"File {filename} deleted successfully"}

