from server import image_operations as operations
from PIL import Image, ImageSequence



def build(user_operations):
    commands = []
    for op in user_operations:
        operation_type = op.WhichOneof("operation")

        if operation_type is None:
            raise ValueError("ImageOperation not legal")

        if operation_type == "rotate_right":
            commands.append(("n", operations.rotate_right))
        elif operation_type == "rotate_left":
            commands.append(("n", operations.rotate_left))
        elif operation_type == "flip_vertical":
            commands.append(("n", operations.flip_vertical))
        elif operation_type == "convert_grayscale":
            commands.append(("n", operations.convert_grayscale))
        elif operation_type == "flip_horizontal":
            commands.append(("n", operations.flip_horizontal))
        elif operation_type == "rotate_degrees":
            commands.append(("n", operations.rotate_degrees(op.rotate_degrees.angle)))
        elif operation_type == "resize":
            commands.append(("n", operations.resize(op.resize.percent)))
        elif operation_type == "thumbnail":
            commands.append(("thumb", operations.thumbnail(300, 300)))

    return commands


def execute_commands(image: Image.Image, commands):
    thumbnail = None
    n_frames = getattr(image, 'n_frames', 1)

    if n_frames > 1:
        frames = []
        durations = []
        for frame in ImageSequence.Iterator(image):
            frame = frame.copy()
            durations.append(frame.info.get('duration', 100))
            for command in commands:
                if command[0] == "thumb":
                    thumbnail = command[1](frame)
                else:
                    frame = command[1](frame)
            frames.append(frame)
        return frames[0], thumbnail, frames[1:], durations
    else:
        for command in commands:
            transform = command[1]
            if command[0] == "thumb":
                thumbnail = transform(image)
            else:
                image = transform(image)
        return image, thumbnail, [], []




