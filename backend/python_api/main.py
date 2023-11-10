import os

from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from operator import itemgetter
from uuid import uuid4
from typing_extensions import Annotated

from classes.file_converter import FileConverter

description = """
Simple app to demonstrate converting files using FastAPI.
"""
app = FastAPI(title="FileConverterApp",
              description=description,
              version="0.1")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Ensure the temporary directory exists
temp_dir = "temp_files"
os.makedirs(temp_dir, exist_ok=True)


@app.post('/convert')
def convert_file(file: Annotated[UploadFile, Form()], from_format: Annotated[str, Form()], to_format: Annotated[str, Form()]):
    print('Converting file from', from_format,"to", to_format)    
    converter = FileConverter()
    supported_formats = converter.get_supported_formats()    
    if (from_format, to_format) not in supported_formats:
        return JSONResponse(content={"error": "Conversion not supported"})
    
    filename = file.filename.split('.')[0]
    # Generate unique filenames
    input_uuid = str(uuid4())
    input_file = f"{input_uuid}_{filename}.{from_format}"
    output_uuid = str(uuid4())
    output_file = f"{output_uuid}_{filename}.{to_format}"
    
    # Combine directory and filename
    input_path = os.path.join(temp_dir, input_file)
    output_path = os.path.join(temp_dir, output_file)
    
    # Save the uploaded file as input.
    with open(input_path, "wb") as f:
        f.write(file.file.read())
    
    # Perform the conversion using the FileConverter class
    (success, media_type) = converter.convert(from_format, to_format, input_path, output_path)
    if success:
        print(f"Conversion successful.. Returning {output_file} as {media_type}")
        return FileResponse(output_path, media_type=media_type, headers={"Content-Disposition": f"attachment; filename={output_file}"})
    else:
        return JSONResponse(content={"error": "Conversion failed"})


@app.get("/")
def read_root():
    return "Welcome to File Converter FastAPI!"
