
import os
import sys

import grpc

from client.generated import image_processing_pb2, image_processing_pb2_grpc

_MAX_MESSAGE_SIZE = 16 * 1024 * 1024  # 16 MB

def create_channel(host = "localhost", port = 50051):
    return grpc.insecure_channel (
        f"{host}:{port}", 
        options=[
            ("grpc.max_send_message_length", _MAX_MESSAGE_SIZE),
            ("grpc.max_receive_message_length", _MAX_MESSAGE_SIZE),
        ],
    )    


def process_image(stub, image_bytes, operations, input_format, output_format):
    request = image_processing_pb2.ImageProcessingRequest(
        input_image=image_bytes,
        input_format=input_format,
        output_format=output_format,
        operations=operations,
    )
    return stub.ProcessImage(request)

def main():

    if len(sys.argv) < 2:
        print("Usage: python -m client.client <image_path> [output_path]")
        print("\nExample:")
        print("  python -m client.client input.jpg output.png")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.png"
    command_file = sys.argv[3]
    operations = []

    
    if not os.path.exists(input_path):
        print(f"Error: file not found: {input_path}")
        sys.exit(1)

    with open(input_path, "rb") as f:
        image_bytes = f.read()
    with open(command_file, "r") as f:
        user_commands = [line.strip() for line in f if line.strip()]
    
    print(user_commands)

    for command in user_commands:
        command = command.split(" ")
        if command[0] == 'rotate_right':
             operations.append(image_processing_pb2.ImageOperation(
                rotate_right=image_processing_pb2.RotateRight()
            ))
        elif command[0] == 'rotate_left':
            operations.append(image_processing_pb2.ImageOperation(
                rotate_left=image_processing_pb2.RotateLeft()
            ))
        elif command[0] == 'convert_grayscale':
            operations.append(image_processing_pb2.ImageOperation(
                convert_grayscale=image_processing_pb2.ConvertGrayscale()
            ))
        elif command[0] == 'flip_vertical':
            operations.append(image_processing_pb2.ImageOperation(
                flip_vertical=image_processing_pb2.FlipVertical()
            )) 
        elif command[0] == 'flip_horizontal':
            operations.append(image_processing_pb2.ImageOperation(
                flip_horizontal=image_processing_pb2.FlipHorizontal()
            )) 
        elif command[0] == 'rotate_degrees':
            operations.append(image_processing_pb2.ImageOperation(
                rotate_degrees=image_processing_pb2.RotateDegrees(angle=int(command[1]))
            ))
        elif command[0] == 'thumbnail':
            operations.append(image_processing_pb2.ImageOperation(
                thumbnail=image_processing_pb2.Thumbnail()
            )) 

    channel = create_channel()
    stub = image_processing_pb2_grpc.ImageProcessingServiceStub(channel)

    print(f"Sending {input_path} ({len(image_bytes)} bytes) with {len(operations)} operations...")
    response = process_image(
        stub, image_bytes, operations, input_format="JPEG", output_format="PNG"
    )

    with open(output_path, "wb") as f:
        f.write(response.output_image)

    if response.thumbnail_image:
        thumb_path = "thumbnail_" + output_path
        with open(thumb_path, "wb") as f:
            f.write(response.thumbnail_image)
        print("Thumbnail generated")

    print(f"Result saved to {output_path}")
    print(f"  Format: {response.output_format}")
    print(f"  Dimensions: {response.width}x{response.height}")
    print(f"  Size: {len(response.output_image)} bytes")


if __name__ == '__main__':
    main()