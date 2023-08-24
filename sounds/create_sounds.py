from pyo import *

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
    
    # Return the sound object
    return sine_wave

# Sound 2: Plucked String-like Sound
def create_plucked_string():
    # Set frequency and duration
    freq2 = 220  # Frequency in Hz
    dur2 = 3     # Duration in seconds
    
    # Create a plucked string-like sound using Karplus-Strong algorithm
    plucked = KarplusStrong(freq=freq2, dur=dur2)
    
    # Return the sound object
    return plucked

# Sound 3: Noise Burst with Envelope
def create_noise_burst_with_envelope():
    # Set duration
    dur3 = 1     # Duration in seconds
    
    # Create an envelope with attack, decay, sustain, and release times
    env3 = Adsr(attack=0.01, decay=0.1, sustain=0.1, release=0.01)
    
    # Create a noise burst and apply the envelope
    noise_burst = Noise(mul=env3)
    
    # Return the sound object
    return noise_burst

# Play each sound
def main():
    # Create sound objects
    sine_sound = create_sine_with_envelope()
    plucked_sound = create_plucked_string()
    noise_sound = create_noise_burst_with_envelope()
    
    # Start the audio server
    s.start()
    
    # Play each sound
    sine_sound.out()
    plucked_sound.out()
    noise_sound.out()
    
    # Wait for the longest sound to finish playing
    longest_dur = max(sine_sound.getDur(), plucked_sound.getDur(), noise_sound.getDur())
    s.sleep(longest_dur)
    
    # Stop the audio server
    s.stop()

if __name__ == "__main__":
    main()
