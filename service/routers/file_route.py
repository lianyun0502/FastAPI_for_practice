from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse
from typing import List


router = APIRouter()

@router.post("/file/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}



@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


@router.post("/files/")
async def create_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@router.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    return {"filenames": [file.filename for file in files]}

@router.get("/")
async def main():
    content = """
<body>
    <form action="/files/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    
    <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
</body>
    """
    return HTMLResponse(content=content)