import os
from pydub import AudioSegment
from pydub.generators import Sawtooth, Sine, WhiteNoise
from pydub.playback import play

# Determine the full path for the temporary WAV file
temp_wav_path = os.path.join(os.path.expanduser("~"), "Downloads", "temp_sound.wav")

def create_white_noise(duration_ms):
    """Create a white noise audio segment."""
    noise = WhiteNoise().to_audio_segment(duration=duration_ms)
    return noise

def create_sawtooth_wave(frequency, duration_ms):
    """Create a sawtooth wave audio segment."""
    sawtooth_wave = Sawtooth(frequency)
    sawtooth_audio = sawtooth_wave.to_audio_segment(duration=duration_ms)
    return sawtooth_audio

def create_sine_wave(frequency, duration_ms):
    """Create a sine wave audio segment."""
    sine_wave = Sine(frequency)
    sine_audio = sine_wave.to_audio_segment(duration=duration_ms)
    return sine_audio

# Duration of each sound in milliseconds
sound_duration = 2000

# Frequencies of the sawtooth and sine waves (440 Hz is A4 note)
sawtooth_frequency = 440
sine_frequency = 660  # Higher frequency for contrast

# Create white noise, sawtooth wave, and sine wave audio segments
white_noise_sound = create_white_noise(sound_duration)
sawtooth_wave_sound = create_sawtooth_wave(sawtooth_frequency, sound_duration)
sine_wave_sound = create_sine_wave(sine_frequency, sound_duration)

# # Combine the three sounds
# combined_sound = white_noise_sound.overlay(sawtooth_wave_sound).overlay(sine_wave_sound)

# Combine the three sounds into a single audio segment
combined_sound = white_noise_sound + sawtooth_wave_sound + sine_wave_sound

# Play the combined sound
play(combined_sound)