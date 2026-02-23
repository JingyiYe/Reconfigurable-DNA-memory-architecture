# Reconfigurable DNA Memory Architecture
This repository contains the source code for the paper **"A reconfigurable DNA memory architecture for hierarchical data management via programmable phase transitions"**. 
It provides a complete computational pipeline for encoding digital information (images) into DNA sequences and decoding DNA sequencing reads back into the original images.

## Repository Structure
* `Encoding/`: Contains the script (`encoding.py`) for converting digital images into DNA sequences, and the demo input image (`picture.png`).
* `Decoding/`: Contains scripts for recovering image data from DNA sequencing reads (`recovery.py`, `picture_recovery.py`, `to_picture.py`).
* `settings.json`: An environment configuration for VS Code.



## 1. System Requirements

### Hardware requirements
The code can run on a standard desktop computer. No special hardware is required. 

### Software requirements
* **OS**: Windows 10/11.
* **Python**: Version 3.8 or higher.
* **Dependencies**: 
  The following Python packages are required to run the scripts:
  * `numpy`
  * `Pillow` (PIL)



## 2. Installation Guide

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/JingyiYe/Reconfigurable-DNA-memory-architecture.git
   cd Reconfigurable-DNA-memory-architecture
