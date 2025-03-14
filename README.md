# py-music

## Description

`py-music` is a Python project for generating and playing music using machine learning models. The project includes functionalities for converting ABC notation to WAV files, playing notes, and generating music using trained models.

## Requirements

- Python >= 3.12
- comet-ml >= 3.49.4
- dotenv >= 0.9.9
- ipykernel >= 6.29.5
- matplotlib >= 3.10.1
- mitdeeplearning >= 0.7.5 (Remove)
- music21 >= 9.5.0 (Remove)
- pandas >= 2.2.3
- simpleaudio >= 1.0.4
- timidity >= 0.1.2
- torch >= 2.6.0
- torchinfo >= 1.8.0

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/py-music.git
   cd py-music
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Load the saved model and generate ABC format text:

   ```python
   from utils import load_data
   from song_utils import play_notes
   from your_model_module import generate_text

   # Load the model
   model = torch.load('training_checkpoint/final_model')

   # Generate text
   text_gen = generate_text(model, 'X', generation_length=1000)
   ```

2. Convert the generated ABC text to WAV and play it:

   ```python
   from utils import save_song_abc, play_song

   # Save the generated text to ABC format
   save_song_abc(text_gen, filename="generated_song")

   # Play the song
   play_song("generated_song")
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License.
