from pyo import *

# Initialize the audio server
s = Server().boot()

# Sound: Noise Burst with Envelope
def create_noise_burst_with_envelope():
    dur = 1     # Duration in seconds
    
    env = Adsr(attack=0.01, decay=0.1, sustain=0.1, release=0.01)
    noise_burst = PinkNoise(mul=env)
    
    return noise_burst

# Play the noise burst
def main():
    s.start()
    
    noise_sound = create_noise_burst_with_envelope()
    
    noise_sound.out()
    
    s.gui(locals())  # Open the graphical user interface
    
    s.stop()

if __name__ == "__main__":
    main()
