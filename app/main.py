from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
import uuid
from app.utils.extract_text import extract_text_from_file

app = FastAPI(
    title="Text Extractor API",
    description="API for extracting text from various file formats",
    version="1.0.0",
    max_upload_size=50_000_000  # 50MB
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Create unique filename
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = UPLOAD_DIR / filename

        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Extract text
        extracted_text = extract_text_from_file(file_path)
        
        # Clean up
        file_path.unlink()
        
        return {
            "status": "success",
            "filename": file.filename,
            "text": extracted_text,
            "text_length": len(extracted_text)
        }

    except Exception as e:
        if 'file_path' in locals() and file_path.exists():
            file_path.unlink()
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "message": "Error processing file"}
        )

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "healthy"}