from server import image_operations as operations

def build(user_operations):
    commands = []
    for op in user_operations:
        operation_type = op.WhichOneof("operation")

        if operation_type is None:
            raise ValueError("ImageOperation not legal")

        if operation_type == "rotate_right":
            commands.append(operations.rotate_right)
            
    return commands


def execute_commands(image, commands):
    for transform in commands:
        image = transform(image)
    return image