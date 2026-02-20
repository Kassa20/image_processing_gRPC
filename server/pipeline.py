from server import image_operations as operations

def build(user_operations):
    commands = []
    for op in user_operations:
        operation_type = op.WhichOneof("operation")

        if operation_type is None:
            raise ValueError("ImageOperation not legal")

        if operation_type == "rotate_right":
            commands.append(operations.rotate_right)
        elif operation_type == "rotate_left":
            commands.append(operations.rotate_left)
        elif operation_type == "flip_vertical":
            commands.append(operations.flip_vertical)
        elif operation_type == "convert_grayscale":
            commands.append(operations.convert_grayscale)
        elif operation_type == "flip_horizontal":
            commands.append(operations.flip_horizontal)
        elif operation_type == "rotate_degrees":
            commands.append(operations.rotate_degrees(45))


    return commands


def execute_commands(image, commands):
    for transform in commands:
        image = transform(image)
    return image