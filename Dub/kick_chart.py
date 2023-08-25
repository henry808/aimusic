import numpy as np
import matplotlib.pyplot as plt

duration_ms = 250
start_frequency = 150.0
end_frequency = 50.0

# Generate the time values
t = np.linspace(0, duration_ms / 1000.0, int(44100 * duration_ms / 1000.0))

# Calculate the linearly spaced frequencies
frequency_sweep = np.linspace(start_frequency, end_frequency, len(t))

# Create the frequency-swept sine wave
phase_acc = np.cumsum(frequency_sweep) / 44100.0
sine_wave = np.sin(2 * np.pi * phase_acc)

# Plot the wave to visualize
plt.plot(t, sine_wave)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Generated Sine Wave')
plt.show()