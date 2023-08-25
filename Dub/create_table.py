from pydub.playback import play
from pydub.generators import Sine


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


# Test the function
lead_wave_table = create_lead_wave_table()

# Print to verify
for key, audio in lead_wave_table.items():
    print(f"{key}: Length of {audio.duration_seconds} seconds")
# Assuming you have the lead_wave_table generated as shown above...

for key, audio in lead_wave_table.items():
    print(f"Playing note: {key}")
    play(audio)