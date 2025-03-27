# collage-images

### Description
This project generates a character mosaic image by combining small images into a larger image based on a text mask.

### Prerequisites
- Python 3.8 or higher
- Install dependencies using `pip install Pillow`

### Setup Virtual Environment
To resolve potential Pillow version issues:
```bash
python -m venv venv
```

### Activate Virtual Environment
`./venv/Scripts/activate`

### Run
`python main.py`

Configuration
Edit the conf.py file to customize the following parameters:

* TARGET_TEXT: The text to be displayed in the mosaic.
* SMALL_IMAGES_DIR: Directory containing small images.
* OUTPUT_PATH: Path to save the generated mosaic image.
* OUTPUT_SIZE: Size of the output image (width, height).
* SMALL_IMG_SIZE: Size of each small image (width, height).
* FONT_PATH: Path to the font file (optional).
* FONT_SIZE: Font size for the text.
