from pyo import *

# Initialize the audio server
s = Server().boot()

# Sound: Pink Noise
def create_pink_noise():
    noise = PinkNoise()
    return noise

# Play the pink noise
def main():
    s.start()
    
    pink_noise = create_pink_noise()
    pink_noise.out()
    
    s.gui(locals())  # Open the graphical user interface
    
    s.stop()

if __name__ == "__main__":
    main()