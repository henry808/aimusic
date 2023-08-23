import sounddevice as sd
import numpy as np


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


kick_waveform = create_kick_sound(100.0, 1.0, 44100.0)
print("Test:", kick_waveform.max(), kick_waveform.min())
sd.play(kick_waveform, 44100.0)
sd.wait()
