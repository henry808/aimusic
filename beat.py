import sounddevice as sd
import numpy as np

# Define parameters
sampling_frequency = 44100
duration = 5  # Duration in seconds

# Generate time values
t = np.linspace(0, duration, int(sampling_frequency * duration), False)

# Define basic parameters for the beat
bpm = 120
beat_length = 60 / bpm  # Length of one beat in seconds
num_beats = int(duration / beat_length)

# Define a basic techno-like beat pattern
kick_pattern = [1, 0, 0, 1, 0, 0, 1, 0]
snare_pattern = [0, 0, 1, 0, 0, 1, 0, 0]
hihat_pattern = [1, 1, 1, 1, 1, 1, 1, 1]

# Function to generate a simple sine wave
def generate_sine_wave(frequency, duration):
    return 0.5 * np.sin(2 * np.pi * frequency * t[:int(sampling_frequency * duration)])

# Generate the sound waveform based on the beat patterns
sound_waveform = np.zeros_like(t)
for beat in range(num_beats):
    if kick_pattern[beat % len(kick_pattern)] == 1:
        sound_waveform += generate_sine_wave(60, 0.1)  # Kick at 60 Hz

    if snare_pattern[beat % len(snare_pattern)] == 1:
        sound_waveform += generate_sine_wave(150, 0.05)  # Snare at 150 Hz

    if hihat_pattern[beat % len(hihat_pattern)] == 1:
        sound_waveform += generate_sine_wave(1000, 0.05)  # Hi-hat at 1000 Hz

# Normalize the waveform
sound_waveform /= np.max(np.abs(sound_waveform))

# Play the generated sound
sd.play(sound_waveform, sampling_frequency)
sd.wait()