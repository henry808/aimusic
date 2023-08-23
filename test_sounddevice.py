import sounddevice as sd
import numpy as np

sampling_frequency = 44100
duration = 2  # seconds
frequency = 440  # Hz

t = np.linspace(0, duration, int(sampling_frequency * duration), False)
waveform = 0.5 * np.sin(2 * np.pi * frequency * t)

sd.play(waveform, sampling_frequency)
sd.wait()
