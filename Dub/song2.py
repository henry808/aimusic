import os
from pydub import AudioSegment
import numpy as np
from pydub.generators import Sawtooth, Sine, WhiteNoise
from pydub.playback import play

# Setup sound parameters
# -----------------------

# Determine the full path for the temporary WAV file
temp_wav_path = os.path.join(os.path.expanduser("~"), "Downloads", "temp_sound.wav")

# Duration of each sound in milliseconds (assuming 4 beats)
sound_duration = 2000

# Frequencies of the sawtooth and sine waves (440 Hz is A4 note)
sawtooth_frequency = 523.25
sine_frequency = 130.81  # Higher frequency for contrast

# Functions to create different sound types
# -----------------------------------------


# Kick
def create_kick_drum(duration_ms):
    """
    Create a simple kick drum sound.
    """
    # Initial and final frequencies for our kick drum sound
    start_frequency = 150.0 / 2.0  # Start from a higher frequency
    end_frequency = 50.0 / 2.0     # Drop to a lower frequency

    # Create the attack (click) component using white noise
    click_duration = int(duration_ms * 0.05)  # 5% of total duration
    click = WhiteNoise().to_audio_segment(duration=click_duration)
    click = click - 25  # Reduce the volume for the click

    # Generate the initial sine wave at the start frequency
    sine_kick = Sine(start_frequency).to_audio_segment(duration=duration_ms)

    # Create a frequency sweep (pitch envelope) from the start to end frequency
    for i in range(duration_ms):
        # Calculate frequency drop ratio
        ratio = i / duration_ms
        frequency = start_frequency + ratio * (end_frequency - start_frequency)

        # Overlay the sine wave segment with the adjusted frequency
        sine_segment = Sine(frequency // 4.0).to_audio_segment(duration=0.05)  # 1ms segment
        sine_kick = sine_kick.overlay(sine_segment, position=i)

    # Combine the click and sine_kick
    combined_kick = click.overlay(sine_kick)

    # The generated sound might be a bit quiet, so let's increase its volume (amplify it)
    amplified_kick = combined_kick + 6  # Increase volume by 6dB, adjust as needed

    return amplified_kick


def create_snare_drum(duration_ms):
    """
    Create a synthetic snare drum sound.
    """

    # Snare drum parameters
    # ---------------------

    # The noise component provides the characteristic "snap" of the snare
    noise_duration = int(duration_ms * 0.4)  # Duration of the noise segment (adjust for more/less "snap")

    # The body provides the tonal component of the snare
    body_frequency = 180  # This frequency gives a bit of the "body" of the snare. Adjust as needed.

    # Create components of the snare sound
    # ------------------------------------

    # Generate the noise segment for the snare
    noise_segment = WhiteNoise().to_audio_segment(duration=noise_duration)

    # Generate the tonal "body" of the snare using a sine wave
    body_segment = Sine(body_frequency).to_audio_segment(duration=duration_ms * 0.4)

    # Adjust volumes to make noise more prominent and the body less so (adjust as needed)
    amplified_noise = noise_segment + 5  # Amplify the noise by 5dB
    attenuated_body = body_segment - 10   # Reduce the volume of the body by 5dB

    # Combine the noise and body
    # --------------------------

    # Overlay the amplified noise on top of the attenuated body
    # Start the noise segment at the beginning of the body segment
    snare_combined = attenuated_body.overlay(amplified_noise, position=0)

    # The result might be too quiet or too loud, so adjust volume if needed
    amplified_snare = snare_combined + 2  # Increase volume by 2dB (adjust as needed)

    return amplified_snare

def create_white_noise(duration_ms):
    """Create a white noise audio segment."""
    noise = WhiteNoise().to_audio_segment(duration=duration_ms)
    return noise

def create_sawtooth_wave(frequency, duration_ms):
    """Create a sawtooth wave audio segment."""
    sawtooth_wave = Sawtooth(frequency)
    sawtooth_audio = sawtooth_wave.to_audio_segment(duration=duration_ms)
    return sawtooth_audio

# def create_lead_synthesizer(frequency, duration_ms, vibrato_depth=0.5, vibrato_rate=6):
#     """
#     Create a lead synth audio segment using a sine wave with vibrato.

#     Vibrato is a rapid, slight variation in pitch, producing a richer sound.

#     Parameters:
#     - frequency: The base frequency of the lead
#     - duration_ms: Duration of the note
#     - vibrato_depth: Depth of the vibrato in Hertz. Determines how far the pitch will vary.
#     - vibrato_rate: Rate of vibrato oscillation in Hertz. Determines how fast the pitch will oscillate.

#     Returns:
#     - An AudioSegment object representing the lead synth sound.
#     """

#     samples = []
#     for i in range(int(duration_ms * 44.1)):  # Assuming 44.1kHz sample rate
#         t = i / 44.1  # Time in milliseconds
#         vibrato = vibrato_depth * sin(2 * pi * vibrato_rate * t / 1000)
#         sample_val = sin(2 * pi * (frequency + vibrato) * t / 1000)
#         samples.append(sample_val)

#     # Convert to pydub audio segment
#     lead_audio = pydub.AudioSegment(
#         samples,
#         frame_rate=44100,
#         sample_width=2,
#         channels=1
#     )

#     # Normalize volume
#     lead_audio = lead_audio.normalize()

#     return lead_audio


def create_lead(frequency, duration_ms):
    """Create a lead sound."""
    sine_wave = Sine(frequency)
    # Amplifying the sine wave to get a stronger, more pronounced sound for the lead
    sine_audio = sine_wave.to_audio_segment(duration=duration_ms).apply_gain(3)
    return sine_audio


def create_lead_wave_table(base_frequency=261.63, duration_ms=1000):
    """Create a lead wave table for 12 chromatic notes starting from the given base frequency."""

    # Frequencies for 12-TET (Twelve-tone equal temperament) chromatic scale
    # Using the formula: f_n = f_0 * (2^(1/12))^n
    # where f_0 is the base frequency and n is the number of half steps.

    frequencies = [base_frequency * (2**(1/12))**i for i in range(12)]

    note_names = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']

    lead_wave_table = {}
    for i, note in enumerate(note_names):
        lead_wave_table[i+1] = create_lead(frequencies[i], duration_ms)

    return lead_wave_table


# Creating sound segments
# -----------------------
kick_drum_sound = create_kick_drum(sound_duration // 8)
snare_drum_sound = create_snare_drum(sound_duration // 8)
white_noise_sound = create_white_noise(sound_duration // 8)
sawtooth_wave_sound = create_sawtooth_wave(sawtooth_frequency, sound_duration // 8)
lead_sound_dict = create_lead_wave_table(sine_frequency           , sound_duration // 8)

#  Sequencer function
#  ------------------

def sequencer(sound_block, loops=1):
    """Generates a sequence based on sound blocks."""
    # Placeholder for the final track
    final_track = AudioSegment.silent(duration=sound_duration)

    # Map each sound name to its corresponding sound
    sound_map = {
        "kick": ("drum", kick_drum_sound),
        "snare": ("drum", snare_drum_sound),
        "noise": ("drum", white_noise_sound),
        "saw": ("drum", sawtooth_wave_sound),
        "lead": ("note", lead_sound_dict)
    } 

    # Placeholder for individual sound tracks
    track = AudioSegment.empty()

    for sound_name, pattern in sound_block.items():
        for p in pattern:
            # Define a silent segment
            segment = AudioSegment.silent(duration=sound_duration // 8)
            
            # if drum
            if sound_map[sound_name][0] == "drum":
                # Overlay sound if 1
                if p == 1:
                    segment = segment.overlay(sound_map[sound_name][1])
            elif sound_map[sound_name][0] == "note":
                # Overlay sound if it's not 0
                if p != 0:
                    segment = segment.overlay(sound_map[sound_name][1][p])

            # Add the segment to the track
            track += segment

    # Loop the track the specified number of times
    return track * loops


# def sequencer(sound_block, loops=1):
#     """Generates a sequence based on sound blocks."""
#     # Placeholder for the final track
#     final_track = AudioSegment.silent(duration=sound_duration)

#     # Map each sound name to its corresponding sound
#     sound_map = {
#         "kick": ("drum", kick_drum_sound),
#         "snare": ("drum", snare_drum_sound),
#         "noise": ("drum", white_noise_sound),
#         "saw": ("drum", sawtooth_wave_sound),
#         "lead": ("note", lead_sound_dict)
#     } 

#     for sound_name, pattern in sound_block.items():
#         # Placeholder for individual sound tracks
#         track = AudioSegment.empty()

#         for p in pattern:
#             # if drum
#             if sound_map[sound_name][0] == "drum":
#                 # Add sound if 1 or add silence if 0
#                 segment = sound_map[sound_name][1] if p == 1 else AudioSegment.silent(duration=sound_duration // 8)
#             elif sound_map[sound_name][0] == "note":
#                 # Add sound if 1 or add silence if 0
#                 segment = sound_map[sound_name][1][p] if p == 1 else AudioSegment.silent(duration=sound_duration // 8)                
#             track += segment

#         # Overlay this track on top of final track
#         final_track = final_track.overlay(track)

#     # Loop the final track the specified number of times
#     return final_track * loops


#  Intro: Simple Kick drum and sine wave to introduce the song
intro_block = {
    "kick": [1,0,1,0,1,0,1,0],
    "snare": [0,0,0,0,0,0,0,0],
    "noise": [0,0,0,0,0,0,0,0],
    "lead": [1,0,1,0,1,0,1,0],
    "saw": [0,0,0,0,0,0,0,0]
} 

#  Verse: Introduce more complexity with the sawtooth and white noise
verse_block = {
    "kick": [1,0,1,0,1,0,1,0],
    "snare": [0,0,1,0,0,0,1,0],
    "noise": [0,1,0,1,0,1,0,1],
    "lead": [1,0,1,0,1,0,1,0],
    "saw": [0,1,0,1,0,1,0,1]
}

#  Chorus: The highlight of the song, so let's use all the sounds here
chorus_block = {
    "kick": [1,0,1,0,1,0,1,0],
    "snare": [0,0,1,0,0,0,1,0],
    "noise": [1,0,0,0,1,0,0,0],
    "lead": [1,0,0,0,0,0,0,0],
    "saw": [0,1,0,1,0,1,0,1]
}

# Bridge: Typically different from both the verse and chorus
bridge_block = {
    "kick": [0,0,1,0,0,0,1,0],
    "snare": [1,0,0,0,1,0,0,0],
    "noise": [1,0,1,0,1,0,1,0],
    "lead": [0,0,0,0,1,0,1,0],
    "saw": [1,0,1,0,0,0,0,0]
}

# Outro: A simplified version to end the song, maybe just the kick and sine wave again
outro_block = {
    "kick": [1,0,1,0,1,0,1,0],
    "snare": [0,0,1,0,0,0,1,0],
    "noise": [0,0,0,0,0,0,0,0],
    "lead": [1,0,1,0,1,0,1,0],
    "saw": [0,0,0,0,0,0,0,0]
}

# Combining the song sections
# ---------------------------

song_structure = [
    (intro_block, 1),   # Play the intro once
    (verse_block, 2),   # Play the verse twice
    (chorus_block, 2),  # Play the chorus twice
    (verse_block, 2),   # Verse again
    (bridge_block, 1),  # Bridge once
    (chorus_block, 2),  # Chorus again
    (outro_block, 1)    # Outro once to finish the song
]


def generate_song(song_structure, track_to_play=None):
    """
    Generates a song based on the provided song structure.

    Parameters:
    - song_structure: List of (block, repetitions) pairs defining the song.
    - track_to_play: If provided, only this track will be included in the final song.

    Returns:
    - AudioSegment containing the constructed song.
    """
    song = AudioSegment.empty()

    for block, repetitions in song_structure:
        # If track_to_play is given, the block is filtered to only keep that track's patterns.
        # Otherwise, the whole block is used.
        focused_block = {track_to_play: block[track_to_play]} if track_to_play else block
        section = sequencer(focused_block, repetitions)
        song += section

    return song


# Generate the song
# -----------------

song = AudioSegment.empty()

# full_song = generate_song(song_structure)
full_song = generate_song(song_structure, track_to_play="kick")

# You can save and play each version as needed:
wav_path = os.path.join(os.path.expanduser("~"), "Downloads", "my_song.wav")
mp3_path = os.path.join(os.path.expanduser("~"), "Downloads", "my_song.mp3")

# For the full song
full_song.export(wav_path, format="wav")
full_song.export(mp3_path, format="mp3", bitrate="192k")


play(full_song)


# Play the song
# -------------

# Convert song's sample rate to 44100 Hz
song = song.set_frame_rate(44100)

# Then play the song
play(song)
