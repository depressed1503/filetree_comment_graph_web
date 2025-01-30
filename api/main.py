from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging
import tempfile
import shutil
import zipfile
import subprocess
from pathlib import Path


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn.error")


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (not safe for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.post("/upload")
async def upload_zip(indent: str = Form(...), ignore: List[str] = Form(...), file: UploadFile = File(...)):
    # Creating a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdir = Path(tmpdirname)
        zip_path = tmpdir / file.filename
        
        # Save the uploaded file
        with zip_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract the zip file
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(tmpdir)
        
        # Run the command in the directory
        new_zip_dir = [f for f in tmpdir.iterdir() if f.is_dir()][0]
        command = ["python", "-m", "filetree_comment_graph", str(new_zip_dir)]
        if indent:
            command.extend(["-i", indent])
        if ignore:
            command.extend(["-n"] + ignore)
        
        # Run the subprocess command
        result = subprocess.run(command, cwd=tmpdir, capture_output=True, text=True)
        
        # Return the result
        return {"output": result.stdout or result.stderr}
