from fastapi import APIRouter, UploadFile, File, HTTPException
from ...src.data.gcp_utils import gcp_utils
from ..services.rabbitmq_service import publish_image_buffer

router = APIRouter()

@router.post("/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read the image file into memory
        image_buffer = await file.read()
        
        # Upload the image to GCP bucket
        gcp_connection=gcp_utils()
        gcp_image_path = await gcp_connection.upload_to_gcp(file.filename, image_buffer)

        # Publish the image buffer to RabbitMQ for prediction
        publish_image_buffer(image_buffer, file.filename)

        return {"message": "Image uploaded successfully.", "gcp_path": gcp_image_path}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
