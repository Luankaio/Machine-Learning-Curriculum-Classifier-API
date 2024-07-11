import os
from dotenv import load_dotenv
from fastapi import UploadFile
from services.exceptions import  ErrorType, CustomException
import shutil
from fastapi.responses import FileResponse

load_dotenv()
pdf_path = os.getenv('pdf_path')

class PdfService():
    
    async def upload_pdf_treatment(file:any):
        if not file.content_type == "application/pdf":
            raise CustomException(error_type=ErrorType.FILE_ERROR, detail="Archive is not a pdf")
        if not os.path.exists(pdf_path):
            os.makedirs(pdf_path)
            
    def path_exists(path:any):
        if not os.path.exists(path):
                raise CustomException(error_type=ErrorType.FILE_NOT_FOUND)
    
    async def create_upload_pdf(file: UploadFile):
        archive_name = os.getenv("pdf_name")     
        path = os.path.join(pdf_path, archive_name)
        
        try:
            with open(path, "wb") as file_object:
                shutil.copyfileobj(file.file, file_object)
        except CustomException:
            raise CustomException(error_type=ErrorType.FILE_ERROR, detail=f"Could not save file")

        return {"filename": file.filename}
    
    def get_pdf(filename: str):
            path = f"{pdf_path}{filename}"
            
            PdfService.path_exists(path)
             
            headers = {"Content-Disposition": f"inline; filename={filename}"}           
            return FileResponse(path, media_type="application/pdf", headers=headers)
        
    def delete_pdf(filename: str):
            path = f"{pdf_path}{filename}"  
            PdfService.path_exists(path)   
            try:
                os.remove(path)
            except CustomException:
                raise CustomException(error_type=ErrorType.FILE_ERROR)
    
    def list_pdfs():
        if not os.path.exists(pdf_path):
            return []
        
        files = [f for f in os.listdir(pdf_path) if f.endswith('.pdf')]
        return files
    
