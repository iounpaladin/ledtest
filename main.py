# IMPORTING PACKAGES

import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.playback import play
import time
from multiprocessing import Process
from scipy.fftpack import fft

# PREPARING THE AUDIO DATA

# Audio file, .wav file
from calc_hz import *
from main2 import fft_analysis

wavFile = "test.wav"

# Retrieve the data from the wav file
data, samplerate = sf.read(wavFile)

n = len(data)  # the length of the arrays contained in data
Fs = samplerate  # the sample rate

# Working with stereo audio, there are two channels in the audio data.
# Let's retrieve each channel seperately:
ch1 = np.array([data[i][0] for i in range(n)])  # channel 1
ch2 = np.array([data[i][1] for i in range(n)])  # channel 2

# x-axis and y-axis to plot the audio data
time_axis = np.linspace(0, n / Fs, n, endpoint=False)
sound_axis = ch1  # we only focus on the first channel here


def playing_audio():
    song = AudioSegment.from_wav(wavFile)
    play(song)


def showing_audiotrack():
    # We use a variable previousTime to store the time when a plot update is made
    # and to then compute the time taken to update the plot of the audio data.
    previousTime = time.time()

    # Turning the interactive mode on
    plt.ion()

    freq = hz

    # Plotting the audio data and updating the plot
    for i in range(n):
        fft_analysis(i)
        plt.pause(analysis_period - (time.time() - previousTime))
        # a forced pause to synchronize the audio being played with the audio track being displayed
        previousTime = time.time()


if __name__ == "__main__":
    p1 = Process(target=playing_audio, args=())
    p1.start()
    p2 = Process(target=showing_audiotrack, args=())
    p2.start()
    p1.join()
    p2.join()
