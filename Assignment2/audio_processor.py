import torch
import torchaudio
from torchaudio import transforms

class AudioProcessor:
    def __init__(self, target_sample_rate=16000):
        self.target_sample_rate = target_sample_rate

    def load_and_preprocess(self, file_path):
        """
        Loads an audio file, resamples it to the target sample rate,
        and ensures it is mono.
        """
        try:
            waveform, sample_rate = torchaudio.load(file_path)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None

        # Resample if necessary
        if sample_rate != self.target_sample_rate:
            resampler = transforms.Resample(orig_freq=sample_rate, new_freq=self.target_sample_rate)
            waveform = resampler(waveform)

        # Convert to mono if stereo
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)

        return waveform
