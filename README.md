# Healthcare Translation Web App

## Description
This project is a **Healthcare Translation Web App** that transcribes, translates, and converts speech to text. It supports multiple languages and provides efficient processing for long audio files using Whisper and Faster-Whisper models.

## Features
- **Speech-to-Text (STT)** using Whisper and Faster-Whisper
- **Translation** between multiple languages using MarianMT
- **Text-to-Speech (TTS)** for translated text
- **Supports multiple languages** including English, Spanish, French, German, Russian, Chinese, Japanese, Arabic, Portuguese, Italian, Korean, and Dutch
- **Fast Processing** using optimized Whisper models
- **Gradio Web Interface** for easy interaction

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.10.11
- pip package manager
- CUDA (if using GPU acceleration)

### Clone the Repository
```sh
git clone <repository-url>
cd <project-folder>
```

### Create Virtual Environment
```sh
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

## Usage
Run the application using the following command:
```sh
streamlit run app.py
```
This will launch the Gradio web interface where users can upload audio files, choose languages, and process speech translation.

## Easy Implementation

```sh
Run the first two cells in the file that Colab file has provided, then obtain a streamlit link and utilize it.
```
## Video Demonstration for the entire System

```sh
https://www.loom.com/share/81318aa025f04b6085c8602182193e72?sid=7ec047ef-5471-40f7-b210-3eb3eaff903e
```

## Configuration
### Language Mapping
The application supports the following languages:
- English (`en`)
- Spanish (`es`)
- French (`fr`)
- German (`de`)
- Russian (`ru`)
- Chinese (`zh`)
- Japanese (`ja`)
- Arabic (`ar`)
- Portuguese (`pt`)
- Italian (`it`)
- Korean (`ko`)
- Dutch (`nl`)
- You can add more, but it is primarily implemented in these languages.

### Model Options
- **Whisper**: Standard Whisper model for transcription
- **Faster-Whisper**: Optimized version for faster processing (recommended for long audio files)

## File Structure
```
├── app.py                 # Main application script
├── requirements.txt       # Required Python dependencies
├── README.txt             # Project documentation
```

## Dependencies
The application requires the following libraries:
- `whisper`
- `gradio`
- `faster_whisper`
- `transformers`
- `TTS`
- `torch`
- `streamlit`

These dependencies will be installed automatically using the `requirements.txt` file.

## Contributing
Contributions are welcome! If you find any bugs or have suggestions for improvements, feel free to create an issue or submit a pull request.

## License
This project is licensed under the MIT License. See `LICENSE` for more details.

## Contact
For any inquiries or support, please reach out to the project maintainer.

