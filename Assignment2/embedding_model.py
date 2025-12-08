from abc import ABC, abstractmethod
import torch
from transformers import Wav2Vec2Model, Wav2Vec2Processor
import numpy as np

class EmbeddingModel(ABC):
    @abstractmethod
    def get_embedding(self, waveform):
        pass

class LocalWav2Vec2Model(EmbeddingModel):
    def __init__(self, model_name="facebook/wav2vec2-base-960h"):
        print(f"Loading local model: {model_name}...")
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        self.model = Wav2Vec2Model.from_pretrained(model_name)
        self.model.eval()

    def get_embedding(self, waveform):
        # Waveform is expected to be (1, T) tensor
        # Processor expects numpy array
        input_values = self.processor(waveform.squeeze().numpy(), return_tensors="pt", sampling_rate=16000).input_values
        
        with torch.no_grad():
            outputs = self.model(input_values)
        
        # Use mean pooling of the last hidden state as the embedding
        # hidden_states: (batch_size, sequence_length, hidden_size)
        hidden_states = outputs.last_hidden_state
        embedding = torch.mean(hidden_states, dim=1)
        
        return embedding.squeeze().numpy().tolist()

class RemoteMockModel(EmbeddingModel):
    def __init__(self):
        print("Initialized Remote Mock Model")

    def get_embedding(self, waveform):
        # Return a random vector of size 768 (standard for base transformers)
        # to simulate an API response
        print("Simulating remote API call...")
        return np.random.rand(768).tolist()
