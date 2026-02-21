"""Script to generate Python gRPC code from .proto files."""

import subprocess
import sys
import os


def generate():
    proto_dir = os.path.join(os.path.dirname(__file__), "protos")
    proto_file = os.path.join(proto_dir, "image_processing.proto")

    # Output directories for generated code
    output_dirs = [
        os.path.join(os.path.dirname(__file__), "server", "generated"),
        os.path.join(os.path.dirname(__file__), "client", "generated"),
    ]

    for output_dir in output_dirs:
        os.makedirs(output_dir, exist_ok=True)

        third_party_dir = os.path.join(os.path.dirname(__file__), "third_party")
        cmd = [
            sys.executable, "-m", "grpc_tools.protoc",
            f"--proto_path={proto_dir}",
            f"--proto_path={third_party_dir}",
            f"--python_out={output_dir}",
            f"--pyi_out={output_dir}",
            f"--grpc_python_out={output_dir}",
            proto_file,
        ]

        print(f"Generating protobuf code in {output_dir} ...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error: {result.stderr}", file=sys.stderr)
            sys.exit(1)

        grpc_file = os.path.join(output_dir, "image_processing_pb2_grpc.py")
        if os.path.exists(grpc_file):
            with open(grpc_file, "r") as f:
                content = f.read()
            content = content.replace(
                "import image_processing_pb2",
                "from . import image_processing_pb2",
            )
            with open(grpc_file, "w") as f:
                f.write(content)

        print(f"  Done: {output_dir}")

    print("Proto generation complete.")


if __name__ == "__main__":
    generate()
