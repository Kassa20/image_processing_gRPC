from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImageProcessingRequest(_message.Message):
    __slots__ = ("input_image", "input_format", "output_format", "operations")
    INPUT_IMAGE_FIELD_NUMBER: _ClassVar[int]
    INPUT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    input_image: bytes
    input_format: str
    output_format: str
    operations: _containers.RepeatedCompositeFieldContainer[ImageOperation]
    def __init__(self, input_image: _Optional[bytes] = ..., input_format: _Optional[str] = ..., output_format: _Optional[str] = ..., operations: _Optional[_Iterable[_Union[ImageOperation, _Mapping]]] = ...) -> None: ...

class ImageOperation(_message.Message):
    __slots__ = ("flip_horizontal", "flip_vertical", "rotate_degrees", "convert_grayscale", "resize", "thumbnail", "rotate_left", "rotate_right")
    FLIP_HORIZONTAL_FIELD_NUMBER: _ClassVar[int]
    FLIP_VERTICAL_FIELD_NUMBER: _ClassVar[int]
    ROTATE_DEGREES_FIELD_NUMBER: _ClassVar[int]
    CONVERT_GRAYSCALE_FIELD_NUMBER: _ClassVar[int]
    RESIZE_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    ROTATE_LEFT_FIELD_NUMBER: _ClassVar[int]
    ROTATE_RIGHT_FIELD_NUMBER: _ClassVar[int]
    flip_horizontal: FlipHorizontal
    flip_vertical: FlipVertical
    rotate_degrees: RotateDegrees
    convert_grayscale: ConvertGrayscale
    resize: Resize
    thumbnail: Thumbnail
    rotate_left: RotateLeft
    rotate_right: RotateRight
    def __init__(self, flip_horizontal: _Optional[_Union[FlipHorizontal, _Mapping]] = ..., flip_vertical: _Optional[_Union[FlipVertical, _Mapping]] = ..., rotate_degrees: _Optional[_Union[RotateDegrees, _Mapping]] = ..., convert_grayscale: _Optional[_Union[ConvertGrayscale, _Mapping]] = ..., resize: _Optional[_Union[Resize, _Mapping]] = ..., thumbnail: _Optional[_Union[Thumbnail, _Mapping]] = ..., rotate_left: _Optional[_Union[RotateLeft, _Mapping]] = ..., rotate_right: _Optional[_Union[RotateRight, _Mapping]] = ...) -> None: ...

class FlipHorizontal(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FlipVertical(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RotateDegrees(_message.Message):
    __slots__ = ("angle",)
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    angle: float
    def __init__(self, angle: _Optional[float] = ...) -> None: ...

class ConvertGrayscale(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Resize(_message.Message):
    __slots__ = ("width", "height")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    width: int
    height: int
    def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...

class Thumbnail(_message.Message):
    __slots__ = ("max_width", "max_height")
    MAX_WIDTH_FIELD_NUMBER: _ClassVar[int]
    MAX_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    max_width: int
    max_height: int
    def __init__(self, max_width: _Optional[int] = ..., max_height: _Optional[int] = ...) -> None: ...

class RotateLeft(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RotateRight(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ImageProcessingResponse(_message.Message):
    __slots__ = ("output_image", "output_format", "width", "height", "thumbnail_image")
    OUTPUT_IMAGE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_IMAGE_FIELD_NUMBER: _ClassVar[int]
    output_image: bytes
    output_format: str
    width: int
    height: int
    thumbnail_image: bytes
    def __init__(self, output_image: _Optional[bytes] = ..., output_format: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., thumbnail_image: _Optional[bytes] = ...) -> None: ...
