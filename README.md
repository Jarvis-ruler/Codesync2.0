# CodeSync Pro 2.0 ⚡

An AI-powered lab assignment analyzer powered by Google Gemini 2.5 Flash. Upload lab assignment images and automatically extract questions, generate production-grade code solutions, and get expected outputs.

## Features

- 📸 **Image Upload**: Analyze lab assignment images
- 🤖 **AI Code Generation**: Generate production-grade code solutions using Gemini 2.5 Flash
- 📝 **Automatic Documentation**: Extract questions and expected outputs
- 🌐 **Multi-Language Support**: Generate code in Python, JavaScript, Java, C++, and more
- 📄 **PDF Export**: Download solutions as formatted PDF documents

## Requirements

- Python 3.8+
- Google Gemini API key
- Streamlit

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ecorelay_demo.git
cd ecorelay_demo
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your API key:
   - Create a `.streamlit/secrets.toml` file or `.env` file
   - Add your Google Gemini API key:
   ```
   GOOGLE_API_KEY="your_api_key_here"
   ```

## Usage

Run the Streamlit app:
```bash
streamlit run visiontest.py
```

The app will open at `http://localhost:8501`

1. Enter your Google Gemini API key
2. Upload an image of a lab assignment
3. Select your preferred programming language
4. Click "Extract & Generate Code"
5. Review the extracted question, generated code, and sample output
6. Optionally download the solution as a PDF

## Project Structure

```
ecorelay_demo/
├── visiontest.py          # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
└── Lab_Record.pdf        # Sample lab record
```

## API Keys

This project uses Google's Gemini API. Obtain an API key from [Google AI Studio](https://aistudio.google.com/apikey)

## License

MIT License - Feel free to use this project for your needs.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
