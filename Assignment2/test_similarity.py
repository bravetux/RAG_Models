import os
import torch
import torchaudio
from main import add_folder, search_file

def create_dummy_audio(filename, duration=1, sample_rate=16000):
    # Create a simple sine wave
    t = torch.linspace(0, duration, int(duration * sample_rate))
    waveform = torch.sin(2 * torch.pi * 440 * t).unsqueeze(0) # 440Hz sine wave
    torchaudio.save(filename, waveform, sample_rate)

def test_workflow():
    test_dir = "test_audio"
    os.makedirs(test_dir, exist_ok=True)

    # Create dummy files
    file1 = os.path.join(test_dir, "audio1.wav")
    file2 = os.path.join(test_dir, "audio2.wav")
    query_file = os.path.join(test_dir, "query.wav")

    print("Creating dummy audio files...")
    create_dummy_audio(file1)
    create_dummy_audio(file2) # Identical to file1
    create_dummy_audio(query_file) # Identical to file1

    print("\n--- Testing Add Command ---")
    # Use remote model for speed in testing, or local if preferred
    add_folder(test_dir, "local") 

    print("\n--- Testing Search Command ---")
    search_file(query_file, "local")

if __name__ == "__main__":
    test_workflow()
