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

def create_sine_kick_segment(duration_ms):
    """
    Generate a frequency-swept sine wave using numpy
    """
    # Initial and final frequencies for our kick drum sound
    start_frequency = 150.0
    end_frequency = 50.0
    
    # Number of samples for the desired duration
    num_samples = int(44100 * duration_ms / 1000.0)

    # Generate time array
    t = np.linspace(0, duration_ms / 1000.0, num_samples)
    
    # Generate frequency sweep
    frequency_sweep = np.linspace(start_frequency, end_frequency, num_samples)
    
    # Calculate phase accumulator
    phase_acc = np.cumsum(frequency_sweep) / 44100.0
    
    # Generate sine wave from phase accumulator
    sine_wave = np.sin(2 * np.pi * phase_acc)

    # Convert the sine wave from a floating point array to a 16-bit integer array
    sine_wave = (sine_wave * 32767).astype(np.int16)
    
    # Convert the integer array to a pydub AudioSegment
    empty_segment = AudioSegment.silent(duration=0)
    sine_kick = empty_segment._spawn(sine_wave.tobytes()).set_frame_rate(44100).set_channels(1).set_sample_width(2)
    
    return sine_kick


def create_kick_drum(duration_ms):
    """
    Create a simple kick drum sound.
    """
    # Initial and final frequencies for our kick drum sound
    start_frequency = 150.0
    end_frequency = 50.0

    # Create the attack (click) component using white noise
    click_duration = int(duration_ms * 0.07)  # 5% of total duration
    click = WhiteNoise().to_audio_segment(duration=click_duration)
    click = click - 20  # Reduce the volume for the click



 
    sine_kick = create_sine_kick_segment(250)
    sine_kick.export("sine_test.wav", format="wav")


    # # Generate a frequency-swept sine wave using numpy
    # t = np.linspace(0, duration_ms / 1000.0, int(44100 * duration_ms / 1000.0))
    # frequency_sweep = np.linspace(start_frequency, end_frequency, len(t))
    # phase_acc = np.cumsum(frequency_sweep) / 44100.0
    # sine_wave = np.sin(2 * np.pi * phase_acc)

    # sine_wave = (sine_wave * 32767).astype(np.int16)
    # empty_segment = AudioSegment.silent(duration=0)
    # sine_kick = empty_segment._spawn(sine_wave.tobytes()).set_frame_rate(44100).set_channels(1).set_sample_width(2)

    # Combine the click and sine_kick
    combined_kick = sine_kick.overlay(click)

    # Amplify the kick for more pronounced effect
    amplified_kick = combined_kick + 6  # Increase volume by 6dB

    # Ensure that the kick is of the desired length
    amplified_kick = amplified_kick[:duration_ms]

    # Save for testing:
    sine_kick.export("sine_test_simple.wav", format="wav")
    click.export("click_test_simple.wav", format="wav")
    combined_kick.export("combined_kick_test_simple.wav", format="wav")

    return combined_kick

#    return amplified_kick



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


print("Expected kick duration:", sound_duration // 8)
print("Actual kick duration:", len(kick_drum_sound))



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
#full_song = generate_song(song_structure)

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
