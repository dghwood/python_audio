# python_audio
Quick python implementation to read audio files 

## Sample Usage 

```
from python_audio import wav
numpy_audio, samples_per_sec = wav.numpy_from_file('python_audio/samples/easy.wav')
```

- `numpy_audio` shape is (num_samples, num_channels) and dtype reflects bits per sample

- `samples_per_sec` gives you the number of samples per second of audio