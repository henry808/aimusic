from pyo import Server, Adsr, Sine, PinkNoise
import time

# Initialize the audio server
s = Server().boot()

# Sound 1: Sine Wave with Envelope
def create_sine_with_envelope():
    # Set frequency and duration
    freq = 440  # Frequency in Hz
    dur = 2     # Duration in seconds
    
    # Create an envelope with attack, decay, sustain, and release times
    env = Adsr(attack=0.1, decay=0.2, sustain=0.5, release=0.1)
    
    # Create a sine wave oscillator and apply the envelope
    sine_wave = Sine(freq=freq, mul=env)
    
    # Return the sound object and its duration
    return sine_wave, dur

# Sound 2: Plucked String-like Sound
def create_plucked_string():
    # Set frequency and duration
    freq2 = 220  # Frequency in Hz
    dur2 = 3     # Duration in seconds
    
    # Create a simple FM synthesis for a plucked string-like sound
    mod = Sine(freq=freq2 * 6, mul=0.1)
    carrier = Sine(freq=freq2 + mod, mul=0.3)
    
    # Return the sound object and its duration
    return carrier, dur2

# Sound 3: Noise Burst with Envelope
def create_noise_burst_with_envelope():
    # Set duration
    dur3 = 1     # Duration in seconds
    
   # Create an envelope with attack, decay, sustain, and release times
    env3 = Adsr(attack=0.5, decay=0.1, sustain=0.1, release=0.5)
    
    # Create a noise burst and apply the envelope
    noise_burst = PinkNoise(mul=env3)

    # Return the sound object and its duration
    return noise_burst, dur3

# Play each sound
def main():
    # Create sound objects and get their durations
    sine_sound, sine_dur = create_sine_with_envelope()
    plucked_sound, plucked_dur = create_plucked_string()
    noise_sound, noise_dur = create_noise_burst_with_envelope()
    
    # Start the audio server
    s.start()
    
    # Play each sound
    sine_sound.out()
    # plucked_sound.out()
    noise_sound.out()
    
    # Wait for the longest sound to finish playing
    longest_dur = max(sine_dur, plucked_dur, noise_dur)
    time.sleep(longest_dur)
    
    # Stop the audio server
    s.stop()

if __name__ == "__main__":
    main()
