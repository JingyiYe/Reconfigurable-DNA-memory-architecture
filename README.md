# Reconfigurable DNA Memory Architecture
This repository contains the source code for the paper **"A reconfigurable DNA memory architecture for hierarchical data management via programmable phase transitions"**. 
It provides a complete computational pipeline for encoding digital information (images) into DNA sequences and decoding DNA sequencing reads back into the original images.

## Repository Structure
* `Encoding/`: Contains the script (`encoding.py`) for converting digital images into DNA sequences, and the demo input image (`picture.png`).
* `Decoding/`: Contains scripts for recovering image data from DNA sequencing reads (`recovery.py`, `picture_recovery.py`, `to_picture.py`).
* `settings.json`: An environment configuration for VS Code.

### System requirements and Installation
This package is supported for Windows. The package has been tested on Windows 10/11. The codes were implemented in Python (version 3.8 or higher). To run the scripts, you need to install the `numpy` and `Pillow` packages (e.g., via `pip install numpy Pillow`). Typical install time is less than 2 minutes on a normal desktop computer.

### Demo and Instructions for use
**Encoding:** To encode a digital image into DNA sequences, change the working directory to `~/Encoding/` and run `encoding.py`. It takes about several seconds to generate the DNA sequences (`DNA.csv`) and related matrix files from the provided demo image (`picture.png`).

**Decoding:** To convert sequencing information back into an image, a decoding demo dataset is available in figshare ([这里填入你的figshare链接]). Download the sequencing file and place it in the `~/Decoding/` folder. Change the working directory to `~/Decoding/` and sequentially run `recovery.py`, `picture_recovery.py`, and `to_picture.py`. It may take about 15 seconds to get the reconstructed image.

To run the software on your own data, simply replace the `picture.png` in the Encoding folder or the `low_freq_5_percent.txt` in the Decoding folder with your own files.

### License
This project is covered under the Apache License 2.0.
