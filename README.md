# Locality-Sensitive-Hashing-LSH-
This project utilizes Locality-Sensitive Hashing for audio data to efficiently detect duplicates and reduce data size, while maintaining integrity. It reads audio files, extracts MFCC features, and uses LSH for categorizing based on similarity. A Flask app processes uploads for similarity analysis, showcasing a novel approach in audio data handling


## Components
1. **queryProcessing.py**: Core script for preprocessing audio files, extracting MFCC features, and implementing LSH for similarity detection.
2. **databaseProcessing.py**: Script for reading and processing a collection of audio files, generating LSH buckets, and storing necessary data in pickle files.
3. **newFlask.py**: Flask web application for uploading audio files, processing them using LSH, and displaying similar audio files from the database.

## queryProcessing.py
This script is the backbone of the project, handling the preprocessing and analysis of audio files. It includes functionalities for:
- Reading audio files and extracting MFCC features.
- Standardizing data for uniformity in analysis.
- Implementing the LSH algorithm to categorize audio files into similarity-based buckets.
- Providing functions to process query audio files and compare them with the database using LSH and Jaccard similarity.

## databaseProcessing.py
This script initializes and processes the audio database. Its main functions are:
- Utilizing `queryProcessing.py` to read a collection of audio files.
- Standardizing these files and generating LSH buckets.
- Saving the processed data (buckets, audio names, and permutations) into pickle files for persistent storage.

## newFlask.py
This script integrates the project with a Flask web application, allowing user interaction. Its key features are:
- Enabling file upload for audio files through a web interface.
- Processing the uploaded files using `queryProcessing.py` for similarity analysis.
- Displaying the results of the similarity search on a web page.

## Features
- Efficient audio processing and feature extraction.
- Implementation of LSH for audio similarity detection.
- Web interface for easy interaction with the system.

## Installation
Requires Python 3.10 with libraries like `librosa`, `Flask`, `numpy`, `pandas`, and others. Install these dependencies via pip.

## Usage
- Run `databaseProcessing.py` to initialize the database.
- Start the Flask app in `newFlask.py` for the web interface.
- Upload audio files for similarity analysis.

## Contribution
Contributions are welcome. Feel free to submit pull requests or raise issues for enhancements or bug fixes.
