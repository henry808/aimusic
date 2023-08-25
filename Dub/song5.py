import os
from pydub import AudioSegment
import math
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
sawtooth_frequency = 130.81 / 2.0
sine_frequency = 130.81  # Higher frequency for contrast

# Functions to create different sound types
# -----------------------------------------

def create_kick_drum(duration_ms):
    """
    Create a simple kick drum sound.
    """
    # Initial and final frequencies for our kick drum sound
    start_frequency = 150.0
    end_frequency = 50.0

    # Create the attack (click) component using white noise
    click_duration = int(duration_ms * 0.05)  # 5% of total duration
    click = WhiteNoise().to_audio_segment(duration=click_duration)
    click = click - 30  # Reduce the volume for the click

    # Generate a frequency-swept sine wave using numpy
    t = np.linspace(0, duration_ms / 1000.0, int(44100 * duration_ms / 1000.0))
    frequency_sweep = np.linspace(start_frequency, end_frequency, len(t) // 2)  # Sweep faster
    frequency_sweep = np.concatenate((frequency_sweep, np.ones(len(t) // 2) * end_frequency))  # Hold at end frequency
    phase_acc = np.cumsum(frequency_sweep) / 44100.0
    sine_wave = np.sin(2 * np.pi * phase_acc)

    sine_wave = (sine_wave * 32767).astype(np.int16)
    empty_segment = AudioSegment.silent(duration=0)
    sine_kick = empty_segment._spawn(sine_wave.tobytes()).set_frame_rate(44100).set_channels(1).set_sample_width(2)

    # Truncate the sine_kick to the desired duration minus the click's duration
    sine_kick = sine_kick[:duration_ms - 25]

    # Combine the click and sine_kick
    combined_kick = sine_kick.overlay(click)

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


def simple_delay(audio, delay_time, decay_factor):
    """
    Simulates a delay effect.

    Parameters:
    - audio: The original AudioSegment object.
    - delay_time: Time in milliseconds for the delay.
    - decay_factor: Multiplier for the volume of the delayed sound. 
                    0.5 means the delayed sound is half as loud as the original.

    Returns:
    - AudioSegment with delay added.
    """

    delayed = audio._spawn(audio.raw_data, overrides={
       "frame_rate": audio.frame_rate
    }).set_frame_rate(audio.frame_rate * 2)

    delayed = delayed - 20  # reduce volume of delayed segment
    combined = audio.overlay(delayed, position=delay_time)

    return combined.apply_gain(10 * math.log10(decay_factor))



def enhance_bass_synth(audio):
    # Add intensity
    audio = audio.apply_gain(15)

    # Boost lower frequencies for a more intense bass sound
    audio = audio.low_pass_filter(120)  # retain frequencies below 120 Hz
    
    # Simulate basic distortion by applying excessive gain and then normalize
    audio = audio.apply_gain(20).normalize()

    # Add some cyberpunk flavor with a bit of echo
    echo = simple_delay(audio, 100, 0.5)
    audio = audio.overlay(echo)

    # Normalize again to avoid clipping
    audio = audio.normalize()

    return audio


def create_bass(frequency, duration_ms):
    """Create a sawtooth wave audio segment."""
    sawtooth_wave = Sawtooth(frequency)
    sawtooth_audio = sawtooth_wave.to_audio_segment(duration=duration_ms)
    return enhance_bass_synth(sawtooth_audio)


def create_bass_table(sawtooth_frequency, duration_ms):
    lead_wave_table = {
    1:  create_bass(sawtooth_frequency / 2.0, duration_ms),
    13:  create_bass(sawtooth_frequency, duration_ms)

    }
    return lead_wave_table 


def create_lead_synthesizer(frequency, duration_ms, vibrato_depth=0.5, vibrato_rate=6):
    """
    Create a lead synth audio segment using a sine wave with vibrato.

    Vibrato is a rapid, slight variation in pitch, producing a richer sound.

    Parameters:
    - frequency: The base frequency of the lead
    - duration_ms: Duration of the note
    - vibrato_depth: Depth of the vibrato in Hertz. Determines how far the pitch will vary.
    - vibrato_rate: Rate of vibrato oscillation in Hertz. Determines how fast the pitch will oscillate.

    Returns:
    - An AudioSegment object representing the lead synth sound.
    """

    sample_rate = 44100
    num_samples = int(duration_ms * sample_rate / 1000)  # total samples for the given duration
    t = np.linspace(0, duration_ms / 1000, num_samples)   # Time array in seconds
    
    vibrato = vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)
    samples = np.sin(2 * np.pi * (frequency + vibrato) * t) * 32767  # 32767 for 16-bit PCM

    # Convert to pydub audio segment
    samples = samples.astype(np.int16)  # convert to int16 for 2-byte samples
    lead_audio = AudioSegment(samples.tobytes(), frame_rate=sample_rate, sample_width=2, channels=1)

    # delay
    echo = simple_delay(lead_audio, 50, 0.7)
    lead_audioaudio = lead_audio.overlay(echo)

    # Normalize volume
    lead_audio = lead_audio.normalize()

    return lead_audio


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
        lead_wave_table[i+1] = create_lead_synthesizer(frequencies[i], duration_ms)

    return lead_wave_table


# Creating sound segments
# -----------------------
kick_drum_sound = create_kick_drum(sound_duration // 8)
snare_drum_sound = create_snare_drum(sound_duration // 8)
white_noise_sound = create_white_noise(sound_duration // 8)
sawtooth_wave_sound = create_bass_table(sawtooth_frequency, sound_duration // 8)
lead_sound_dict = create_lead_wave_table(sine_frequency, sound_duration // 8)


print("Expected kick duration:", sound_duration // 8)
print("Actual kick duration:", len(kick_drum_sound))


#  Sequencer function
#  ------------------

def sequencer(sound_block, sound_duration, levels, loops=1):
    """Generates a sequence based on sound blocks."""

    # Map each sound name to its corresponding sound
    sound_map = {
        "kick": ("drum", kick_drum_sound),
        "snare": ("drum", snare_drum_sound),
        "noise": ("drum", white_noise_sound),
        "saw": ("note", sawtooth_wave_sound),
        "lead": ("note", lead_sound_dict)
    }

    # Placeholder for the final track
    final_track = AudioSegment.silent(duration=sound_duration)

    for sound_name, pattern in sound_block.items():
        # Placeholder for individual sound tracks
        track = AudioSegment.empty()

        for step in pattern:
            # Define a silent segment
            segment = AudioSegment.silent(duration=sound_duration // 8)

            # if drum
            if sound_map[sound_name][0] == "drum":
                # Overlay sound if 1
                if step == 1:
                    segment = segment.overlay(sound_map[sound_name][1] - levels[sound_name])
            elif sound_map[sound_name][0] == "note":
                # Overlay sound if it's not 0
                if step != 0:
                    segment = segment.overlay(sound_map[sound_name][1][step] - levels[sound_name])

            # Add the segment to the track
            track += segment

        # Overlay this track on top of final track
        final_track = final_track.overlay(track)

    # Loop the track the specified number of times
    return final_track * loops * 2


#  Intro: Simple Kick drum and sine wave to introduce the song
intro_block = {
    "kick": [1, 0, 1, 0, 1, 0, 1, 0],
    "snare": [0, 0, 0, 0, 0, 0, 0, 0],
    "noise": [0, 0, 0, 0, 0, 0, 0, 0],
    "lead": [1, 0, 5, 0, 3, 0, 6, 0],
    "saw": [1, 13, 0, 0, 0, 0, 0, 0]
}

#  Verse: Introduce more complexity with the sawtooth and white noise
verse_block = {
    "kick": [1, 0, 1, 0, 1, 0, 1, 0],
    "snare": [0, 0, 1, 0, 0, 0, 1, 0],
    "noise": [0, 1, 0, 1, 0, 1, 0, 1],
    "lead": [1, 5, 3, 6, 8, 10, 8, 6],  # Corrected melody
    "saw": [1, 13, 1, 13, 1, 13, 1, 13]
}

# Chorus: The highlight of the song, use an uplifting melody
chorus_block = {
    "kick": [1, 0, 1, 0, 1, 0, 1, 0],
    "snare": [0, 0, 1, 0, 0, 0, 1, 0],
    "noise": [1, 0, 0, 0, 1, 0, 0, 0],
    "lead": [8, 5, 6, 8, 10, 8, 6, 5],  # New chorus melody
    "saw": [1, 13, 1, 13, 1, 13, 1, 13]
}

# Bridge: Different pace, more contemplative
bridge_block = {
    "kick": [0, 0, 1, 0, 0, 0, 1, 0],
    "snare": [1, 0, 0, 0, 1, 0, 0, 0],
    "noise": [1, 0, 1, 0, 1, 0, 1, 0],
    "lead": [5, 6, 8, 10, 8, 6, 5, 3],  # New bridge melody
    "saw": [1, 13, 1, 0, 0, 0, 0, 0]
}

solo_block = {
    "kick": [1, 1, 1, 1, 0, 0, 1, 0],
    "snare": [0, 0, 0, 0, 0, 0, 0, 0],
    "noise": [0, 0, 0, 0, 0, 0, 0, 0],
    "lead": [0, 0, 0, 0, 0, 0, 0, 0],
    "saw": [1, 13, 0, 0, 1, 13, 0, 0]
}

# Outro: A simplified version to end the song, maybe just the kick and sine wave again
outro_block = {
    "kick": [1, 0, 1, 0, 1, 0, 1, 0],
    "snare": [0, 0, 1, 0, 0, 0, 1, 0],
    "noise": [0, 0, 0, 0, 0, 0, 0, 0],
    "lead": [0, 0, 0, 0, 0, 0, 0, 0],
    "saw": [1, 13, 0, 0, 0, 0, 0, 0]
}


# Levels
levels = {
    "kick": 0,
    "snare": 0,
    "noise": 40,
    "lead": 20,
    "saw": 23
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
    (solo_block, 1),    # Bridge once
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
        section = sequencer(focused_block, sound_duration, levels, repetitions)
        song += section

    return song


# Generate the song
# -----------------

song = AudioSegment.empty()

# full_song = generate_song(song_structure, track_to_play="kick")
full_song = generate_song(song_structure)

# You can save and play each version as needed:
wav_path = os.path.join(os.path.expanduser("~"), "Downloads", "my_song.wav")
mp3_path = os.path.join(os.path.expanduser("~"), "Downloads", "my_song.mp3")


full_song = full_song.set_channels(2)
full_song = full_song.set_frame_rate(44100)
full_song.export(mp3_path, format="mp3", bitrate="192k")

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
