import io
import logging 

import grpc 
from PIL import Image 

from server.generated import image_processing_pb2, image_processing_pb2_grpc
from server.pipeline import build, execute_commands

logger = logging.getLogger(__name__)

class ImageProcessingServicer(image_processing_pb2_grpc.ImageProcessingServiceServicer):

    def ProcessImage(self, request, context):
        
        if not request.input_image:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("input_image is empty")
            return image_processing_pb2.ImageProcessingResponse()
        
        #Decode
        try:
            image = Image.open(io.BytesIO(request.input_image))
            image.load()  # force full decode
        except Exception as exc:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Cannot decode image: {exc}")
            return image_processing_pb2.ImageProcessingResponse()
        
        detected_format = image.format or "PNG"
        input_format = request.input_format.upper() if request.input_format else detected_format
        output_format = request.output_format.upper() if request.output_format else input_format

        try:
            commands = build(request.operations)
        except ValueError as err:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(exc))
            return image_processing_pb2.ImageProcessingResponse()

        try:
            image, thumbnail = execute_commands(image, commands)
        except Exception as exc:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Pipeline execution failed: {exc}")
            return image_processing_pb2.ImageProcessingResponse()      
        if output_format == "JPEG" and image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        
        buffer = io.BytesIO()
        thumb_buffer = io.BytesIO()
        try:
            image.save(buffer, format=output_format)
            thumbnail.save(thumb_buffer, format=output_format)
        except Exception as exc:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Cannot encode image as {output_format}: {exc}")
            return image_processing_pb2.ImageProcessingResponse()

        logger.info(
            "Processed image: %dx%d %s -> %dx%d %s, %d operations",
            image.width, image.height, input_format,
            image.width, image.height, output_format,
            len(commands),
        )

        return image_processing_pb2.ImageProcessingResponse(
            output_image=buffer.getvalue(),
            output_format=output_format,
            width=image.width,
            height=image.height,
            thumbnail_image=thumb_buffer.getvalue(),
        )
    