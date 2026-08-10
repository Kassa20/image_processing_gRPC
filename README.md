# Image Processing Language Reference

<img width="490" height="345" alt="image" src="https://github.com/user-attachments/assets/ae2aa0c3-9005-4ad5-a02c-002a1b4f2f00" />

## Overview

The image processing service accepts a request describing an input image and an ordered
pipeline of operations to apply. Operations execute left-to-right; the output of each
step feeds into the next. The language is expressed as a Protobuf message (gRPC) or
equivalent JSON body (HTTP/REST at `POST /v1/image/process`).

## Request Fields

Field         | Required | Type | Default Description

`input_image` | **yes** | bytes | — Raw image file | needs to be **500 x 700** and less than **16MB**
 `input_format` | no | string | auto-detected Hint for the decoder. Ignored if image bytes are valid.  
 `output_format`| no | string | same as input format Format used to encode the result (e.g. `"PNG"`).  
 `operations` | **yes** | list | `[]` (no-op) Ordered pipeline of image transformations.

**Format strings** are matched case-insensitively. Supported values depend on the
underlying Pillow installation; common safe values: `JPEG`, `PNG`, `GIF`, `BMP`,
`WEBP`, `TIFF`.

---



---

## Request Fields

Field         | Required | Type | Default Description

`input_image` | **yes** | bytes | — Raw image file | needs to be **500 x 700** and less than **16MB**
 `input_format` | no | string | auto-detected Hint for the decoder. Ignored if image bytes are valid.  
 `output_format`| no | string | same as input format Format used to encode the result (e.g. `"PNG"`).  
 `operations` | **yes** | list | `[]` (no-op) Ordered pipeline of image transformations.

**Format strings** are matched case-insensitively. Supported values depend on the
underlying Pillow installation; common safe values: `JPEG`, `PNG`, `GIF`, `BMP`,
`WEBP`, `TIFF`.

---

## Operations

### `flip_horizontal`

**Parameters:** none

Flips the image along its horizontal axis — pixels move top-to-bottom (the image
appears upside-down). Equivalent to `ImageOps.flip` in Pillow.

```
flip_horizontal {}
```

---

### `flip_vertical`

**Parameters:** none

Flips the image along its vertical axis — pixels move left-to-right (mirror image).
Equivalent to `ImageOps.mirror` in Pillow.

```
flip_vertical {}
```

---

### `rotate_left`

**Parameters:** none

Rotates the image exactly **90 degrees counter-clockwise**. Canvas expands to fit.

```
rotate_left {}
```

---

### `rotate_right`

**Parameters:** none

Rotates the image exactly **90 degrees clockwise**. Canvas expands to fit.

```
rotate_right {}
```

---

### `rotate_degrees`

**Parameters:**

| Field   | Required | Type    | Legal Range                    | Description                             |
| ------- | -------- | ------- | ------------------------------ | --------------------------------------- |
| `angle` | **yes**  | integer | any IEEE 754 integer (−∞ … +∞) | Degrees to rotate **counter-clockwise** |

- Positive values → counter-clockwise rotation.
- Negative values → clockwise rotation.
- Values ≥ 360 or ≤ −360 wrap naturally (e.g. `angle = 370` behaves like `angle = 10`).
- `angle = 0` is a no-op (image is unchanged but still re-encoded).
- Canvas expands to fit rotated content (no cropping).
- No server-side range validation; any finite double is accepted.

```
rotate_degrees { angle = 45 }
rotate_degrees { angle = -90 }
```

---

### `convert_grayscale`

**Parameters:** none

Converts the image to grayscale and then back to RGB mode. The output is a
three-channel image where all channels are equal. Any alpha channel is discarded.

```
convert_grayscale {}
```

---

### `resize`

**Parameters:**

| Field     | Required | Type  | Legal Range    | Description                                    |
| --------- | -------- | ----- | -------------- | ---------------------------------------------- |
| `percent` | **yes**  | int32 | **1 … 10 000** | Scale factor as a percentage of original size. |

- `percent = 100` → no change in dimensions.
- `percent = 50` → half the original width and height.
- `percent = 200` → double the original width and height.
- **Practical minimum: 1.** A value of `0` produces a 0×0 image; negative values
  produce a 0×0 image (integer truncation). Both will cause an error during encoding.
  No server-side validation is performed — callers must enforce this constraint.
- **Practical maximum: 10 000** (×100 scale). Higher values are not rejected by the
  server but will likely exhaust memory.
- Uses LANCZOS resampling (high quality, anti-aliased).

```
resize { percent = 50 }
resize { percent = 150 }
```

---

### `thumbnail`

**Parameters:**

| Field        | Required | Type  | Legal Range | Description                             |
| ------------ | -------- | ----- | ----------- | --------------------------------------- |
| `max_width`  | **yes**  | int32 | 1 … 2^31−1  | Maximum width bound for the thumbnail.  |
| `max_height` | **yes**  | int32 | 1 … 2^31−1  | Maximum height bound for the thumbnail. |

> The thumbnail is always generated at a fixed bound of **300 × 300 pixels**

- Aspect ratio is always preserved; neither dimension exceeds the bound.
- The thumbnail is returned in the `thumbnail_image` field of the response alongside
  the fully processed `output_image`.
- This operation does **not** replace the main image — it produces a side-channel output.
- Uses LANCZOS resampling.

```
thumbnail { max_width = 128, max_height = 128 }
```

---

## Response Fields

| Field             | Type   | Description                                                     |
| ----------------- | ------ | --------------------------------------------------------------- |
| `output_image`    | bytes  | Processed image encoded in `output_format`.                     |
| `output_format`   | string | The format used to encode `output_image`.                       |
| `width`           | int32  | Width of `output_image` in pixels.                              |
| `height`          | int32  | Height of `output_image` in pixels.                             |
| `thumbnail_image` | bytes  | Thumbnail bytes (non-empty only when a `thumbnail` op was run). |

---

## Error Codes

| gRPC Status        | Condition                                                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| `INVALID_ARGUMENT` | `input_image` is empty, image bytes cannot be decoded, or an `ImageOperation` has no variant set.                               |
| `INTERNAL`         | Pipeline execution failed (e.g. unsupported mode conversion), or the processed image cannot be encoded in the requested format. |

---

## Pipeline Execution Notes

1. Operations are applied **in declaration order**; the list is a sequential pipeline,
   not a set.
2. **Animated images (GIF):** Every frame in the sequence is transformed independently.
   Frame durations are preserved. The loop count is reset to infinite (`loop = 0`).
3. An empty `operations` returns the image re-encoded in the
   requested format with no pixel changes.

---

## Examples

### Rotate 45° counter-clockwise then convert to grayscale

```json
{
  "input_image": "<base64>",
  "output_format": "PNG",
  "operations": [
    { "rotateDegrees": { "angle": 45 } },
    { "convertGrayscale": {} }
  ]
}
```

### Halve the image and generate a thumbnail

```json
{
  "input_image": "<base64>",
  "operations": [
    { "resize": { "percent": 50 } },
    { "thumbnail": { "max_width": 128, "max_height": 128 } }
  ]
}
```

### Flip vertically (mirror) then rotate 90° clockwise

```json
{
  "input_image": "<base64>",
  "operations": [{ "flipVertical": {} }, { "rotateRight": {} }]
}
```
