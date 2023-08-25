from pydub import AudioSegment

import numpy as np
import matplotlib.pyplot as plt

duration_ms = 250
start_frequency = 150.0
end_frequency = 50.0

# Generate the time values
t = np.linspace(0, duration_ms / 1000.0, int(44100 * duration_ms / 1000.0))

# Calculate the linearly spaced frequencies
frequency_sweep = np.linspace(start_frequency, end_frequency, len(t))

# Create the frequency-swept sine wave
phase_acc = np.cumsum(frequency_sweep) / 44100.0
sine_wave = np.sin(2 * np.pi * phase_acc)


  # Generate a frequency-swept sine wave using numpy
    t = np.linspace(0, duration_ms / 1000.0, int(44100 * duration_ms / 1000.0))
    frequency_sweep = np.linspace(start_frequency, end_frequency, len(t))
    phase_acc = np.cumsum(frequency_sweep) / 44100.0
    sine_wave = np.sin(2 * np.pi * phase_acc)


# Convert the sine wave to an audio segment and save
sine_wave_audio = (sine_wave * 32767).astype(np.int16)
empty_segment = AudioSegment.silent(duration=0)
sine_kick = empty_segment._spawn(sine_wave.tobytes()).set_frame_rate(44100).set_channels(1).set_sample_width(2)
sine_kick.export("sine_test.wav", format="wav")