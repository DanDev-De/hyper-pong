#!/usr/bin/env python3
import numpy as np
import wave
import os
from pathlib import Path

def generate_beep(frequency, duration=0.1, decay=5.0, sample_rate=44100):
    """Generate a beep sound with the given frequency and duration."""
    t = np.linspace(0, duration, int(sample_rate * duration))
    beep = np.sin(2 * np.pi * frequency * t) * np.exp(-decay * t)
    # Scale to 16-bit range (-32768 to 32767)
    return (beep * 32767).astype(np.int16)

def generate_ascending_tone(start_freq, end_freq, duration=0.2, decay=5.0, sample_rate=44100):
    """Generate an ascending tone from start_freq to end_freq."""
    t = np.linspace(0, duration, int(sample_rate * duration))
    # Create a frequency array that increases linearly
    freq = np.linspace(start_freq, end_freq, len(t))
    # Calculate the phase by integrating the frequency
    phase = np.cumsum(freq) / sample_rate
    # Generate the tone
    tone = np.sin(2 * np.pi * phase) * np.exp(-decay * t)
    # Scale to 16-bit range
    return (tone * 32767).astype(np.int16)

def save_wav(filename, audio_data, sample_rate=44100):
    """Save audio data as a WAV file."""
    # Convert mono to stereo by duplicating the channel
    stereo_data = np.column_stack((audio_data, audio_data))
    
    # Convert Path object to string if necessary
    filepath = str(filename)
    
    with wave.open(filepath, "w") as wav_file:
        wav_file.setnchannels(2)  # stereo
        wav_file.setsampwidth(2)  # 2 bytes per sample (16 bits)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(stereo_data.tobytes())

def main():
    # Create sounds directory if it doesn't exist
    sounds_dir = Path("sounds")
    try:
        sounds_dir.mkdir(exist_ok=True)
        print(f"Created or confirmed directory: {sounds_dir}")
    except Exception as e:
        print(f"Error creating directory '{sounds_dir}': {e}")
        return
    
    try:
        # Generate paddle hit sound (high-pitched beep)
        paddle_hit = generate_beep(frequency=440)  # A4 note
        save_wav(sounds_dir / "paddle_hit.wav", paddle_hit)  # Path object will be converted to string
        print("Created paddle_hit.wav")
        
        # Generate wall hit sound (low-pitched beep)
        wall_hit = generate_beep(frequency=220)  # A3 note
        save_wav(sounds_dir / "wall_hit.wav", wall_hit)  # Path object will be converted to string
        print("Created wall_hit.wav")
        
        # Generate score sound (ascending tone)
        score = generate_ascending_tone(start_freq=440, end_freq=880)  # A4 to A5
        save_wav(sounds_dir / "score.wav", score)  # Path object will be converted to string
        print("Created score.wav")
        
        print("All sound files generated successfully!")
        
    except Exception as e:
        print(f"Error generating sound files: {e}")

if __name__ == "__main__":
    main()

