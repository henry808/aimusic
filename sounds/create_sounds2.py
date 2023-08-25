from pyo import *

# Initialize the audio server
s = Server().boot()

# Sound 1: Sine Wave with Envelope
def create_sine_with_envelope():
    freq = 440  # Frequency in Hz
    dur = 2     # Duration in seconds
    
    env = Adsr(attack=0.1, decay=0.2, sustain=0.5, release=0.1)
    sine_wave = Sine(freq=freq, mul=env)
    
    return sine_wave

# Sound 2: Plucked String-like Sound
def create_plucked_string():
    freq2 = 220  # Frequency in Hz
    dur2 = 3     # Duration in seconds
    
    mod = Sine(freq=freq2 * 6, mul=0.1)
    carrier = Sine(freq=freq2 + mod, mul=0.3)
    
    return carrier

# Sound 3: Noise Burst with Envelope
def create_noise_burst_with_envelope():
    dur3 = 1     # Duration in seconds
    
    env3 = Adsr(attack=0.01, decay=0.1, sustain=0.1, release=0.01)
    noise_burst = PinkNoise(mul=env3)
    
    return noise_burst

# Play each sound
def main():
    s.start()
    
    sine_sound = create_sine_with_envelope()
    plucked_sound = create_plucked_string()
    noise_sound = create_noise_burst_with_envelope()
    
    sine_sound.out()
    # plucked_sound.out()
    noise_sound.out()
    
    s.gui(locals())  # Open the graphical user interface
    
    s.stop()

if __name__ == "__main__":
    main()
