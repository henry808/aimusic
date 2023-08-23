import sounddevice as sd
import numpy as np

# Define parameters
sampling_frequency = 44100.0
duration = 5.0
t = np.linspace(0, duration, int(sampling_frequency * duration), False)

# Define basic parameters for the beat
bpm = 120.0
beat_length = 60.0 / bpm

# On a 16th note grid, each beat is divided by 4
sixteenth_note_length = beat_length / 4.0
num_sixteenth_notes = int(duration / sixteenth_note_length)

# Define beat patterns on a 16th note grid
kick_pattern = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
snare_pattern = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
hihat_pattern = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# hihat_pattern = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]


def create_kick_sound(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # ADSR envelope parameters
    attack_time = 0.01
    decay_time = 0.1
    sustain_level = 0.3
    sustain_time = duration - attack_time - decay_time
    release_time = 0.1

    # Calculate envelope
    attack = np.linspace(0, 1, int(attack_time * sample_rate))
    decay = np.linspace(1, sustain_level, int(decay_time * sample_rate))
    sustain = np.ones(int(sustain_time * sample_rate)) * sustain_level
    release = np.linspace(sustain_level, 0, int(release_time * sample_rate))

    envelope = np.concatenate([attack, decay, sustain, release])

    # Modulate frequency to get the kick sound
    start_freq = frequency * 1.5
    end_freq = frequency
    freqs = np.linspace(start_freq, end_freq, t.size)

    # # Generate waveform and apply envelope
    kick = np.sin(2 * np.pi * freqs * t)
    kick_with_envelope = kick * envelope[:kick.size]

    # Add some noise for the beater sound (optional)
    noise = np.random.normal(0, 0.5, kick_with_envelope.shape)
    noise_envelope = np.exp(-t / 0.05)
    kick_with_noise = kick_with_envelope + noise * noise_envelope

    return kick_with_noise


# Function to generate a simple sine wave
def generate_sine_wave(frequency, duration):
    return 0.5 * \
        np.sin(2 * np.pi * frequency * t[:int(sampling_frequency * duration)])


# Generate the sound waveform based on the beat patterns
sound_waveform = np.zeros_like(t)

for note in range(num_sixteenth_notes):
    start_idx = int(note * sixteenth_note_length * sampling_frequency)
    end_idx = start_idx + int(sampling_frequency * 0.1)

    if kick_pattern[note % len(kick_pattern)] == 1:
        sound_waveform[start_idx:end_idx] += \
            create_kick_sound(100.0, 1.0, sampling_frequency)
        # generate_sine_wave(100.0, 0.1)
    if snare_pattern[note % len(snare_pattern)] == 1:
        sound_waveform[start_idx:end_idx] += generate_sine_wave(200.0, 0.1)
    if hihat_pattern[note % len(hihat_pattern)] == 1:
        sound_waveform[start_idx:end_idx] += generate_sine_wave(400.0, 0.1)

# Normalize the waveform
sound_waveform /= np.max(np.abs(sound_waveform))


# sound_waveform = create_kick_sound(100.0, 1.0, 44100.0)

print("Completed setup.")

# Play the generated sound
sd.play(sound_waveform, sampling_frequency)
sd.wait()
