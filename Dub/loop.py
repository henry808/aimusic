import os
from pydub import AudioSegment
from pydub.generators import Sawtooth, Sine, WhiteNoise
from pydub.playback import play

# Setup sound parameters
# -----------------------

# Determine the full path for the temporary WAV file
temp_wav_path = os.path.join(os.path.expanduser("~"), "Downloads", "temp_sound.wav")

# Duration of each sound in milliseconds (assuming 4 beats)
sound_duration = 2000

# Frequencies of the sawtooth and sine waves (440 Hz is A4 note)
sawtooth_frequency = 440
sine_frequency = 660  # Higher frequency for contrast

# Functions to create different sound types
# -----------------------------------------

def create_kick_drum(duration_ms):
    """
    Create a simple kick drum sound.
    """
    # Initial and final frequencies for our kick drum sound
    start_frequency = 150  # Start from a higher frequency
    end_frequency = 50     # Drop to a lower frequency
    
    # Generate the initial sine wave at the start frequency
    sine_kick = Sine(start_frequency).to_audio_segment(duration=duration_ms)
    
    # Create a frequency sweep (pitch envelope) from the start to end frequency
    # This is a simple method to simulate the characteristic of a kick drum where the pitch drops rapidly.
    for i in range(duration_ms):
        # Calculate frequency drop ratio
        ratio = i / duration_ms
        frequency = start_frequency - ratio * (start_frequency - end_frequency)
        
        # Overlay the sine wave segment with the adjusted frequency
        sine_segment = Sine(frequency).to_audio_segment(duration=1)  # 1ms segment
        sine_kick = sine_kick.overlay(sine_segment, position=i)
    
    # The generated sound might be a bit quiet, so let's increase its volume (amplify it)
    amplified_kick = sine_kick + 6  # Increase volume by 6dB, adjust as needed
    
    return amplified_kick


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

# Creating sound segments
# -----------------------

kick_drum_sound = create_kick_drum(sound_duration // 8)
white_noise_sound = create_white_noise(sound_duration // 8)
sawtooth_wave_sound = create_sawtooth_wave(sawtooth_frequency, sound_duration // 8)
sine_wave_sound = create_sine_wave(sine_frequency, sound_duration // 8)

# Sequencer function
# ------------------

def sequencer(sound_block, loops=1):
    """Generates a sequence based on sound blocks."""
    # Placeholder for the final track
    final_track = AudioSegment.silent(duration=sound_duration)
    
    # Map each sound name to its corresponding sound
    sound_map = {
        "kick": kick_drum_sound,
        "noise": white_noise_sound,
        "saw": sawtooth_wave_sound,
        "sine": sine_wave_sound
    }
    
    for sound_name, pattern in sound_block.items():
        # Placeholder for individual sound tracks
        track = AudioSegment.empty()
        
        for p in pattern:
            # Add sound if 1 or add silence if 0
            segment = sound_map[sound_name] if p == 1 else AudioSegment.silent(duration=sound_duration // 8)
            track += segment
        
        # Overlay this track on top of final track
        final_track = final_track.overlay(track)
    
    # Loop the final track the specified number of times
    return final_track * loops

# Define a sound block pattern
# ----------------------------

sound_block = {
    "kick": [1,0,1,0,1,0,1,0],
    "noise": [0,0,1,0,0,0,1,0],
    "sine": [1,0,0,0,0,0,0,0],
    "saw": [0,1,0,1,0,1,0,1]
}


# sound_block = {
#     "kick": [1,0,1,0,1,0,1,0],
#     "noise": [1,0,0,0,0,0,0,0],
#     "sine": [1,0,0,0,0,0,0,0],
#     "saw": [1,0,0,0,0,0,0,0]
# }

number_of_loops = 4  # Change this to set the desired number of loops

# Generate sequence and play
# --------------------------

combined_sound = sequencer(sound_block, number_of_loops)
play(combined_sound)
