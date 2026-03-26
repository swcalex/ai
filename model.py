import torch
import torch.nn as nn
import torch.nn.init as init

class AudioAutoencoder(nn.Module):
    def __init__(self):
        super(AudioAutoencoder, self).__init__()
        # Algorithm Spec v0.6.0
        self.input_size = 800
        self.hidden_size = 100
        self.output_size = 800
        
        # Encoder: Input -> Hidden (Compression)
        # Activation: Tanh (Preserve Audio Phase -1~1)
        self.encoder = nn.Sequential(
            nn.Linear(self.input_size, self.hidden_size),
            nn.Tanh()
        )
        
        # Decoder: Hidden -> Output (Reconstruction)
        self.decoder = nn.Sequential(
            nn.Linear(self.hidden_size, self.output_size),
            nn.Tanh() 
        )
        
        self._init_weights()

    def _init_weights(self):
        """
        Xavier Uniform Initialization for Tanh activation
        """
        for m in self.modules():
            if isinstance(m, nn.Linear):
                init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    init.zeros_(m.bias)

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded