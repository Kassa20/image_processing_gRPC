from concurrent import futures
import grpc 
import logging 

from server.generated import image_processing_pb2_grpc
from server.servicer import ImageProcessingServicer

MAX_MESSAGE_SIZE = 16 * 1024 * 1024

def serve(port = 50051, max_workers = 10):

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers), 
        options=[
            ("grpc.max_send_message_length", MAX_MESSAGE_SIZE),
            ("grpc.max_receive_message_length", MAX_MESSAGE_SIZE),
        ],
    )

    image_processing_pb2_grpc.add_ImageProcessingServiceServicer_to_server(
        ImageProcessingServicer(), server
    )
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logging.info("Image processing server started on port %d", port)
    return server

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    server = serve()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.stop(grace=5)


if __name__ == "__main__":
    main()