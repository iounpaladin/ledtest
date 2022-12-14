#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import time
from multiprocessing import Process

import scipy.io.wavfile as wavfile
import scipy
from pydub import AudioSegment
from pydub.playback import play
from scipy.fftpack import fft
import numpy as np
from matplotlib import pyplot as plt

from pychroma import Sketch, Controller

from calc_hz import *

Fs, signal = wavfile.read("test.wav")
l_audio = len(signal.shape)
if l_audio == 2:
    signal = signal.sum(axis=1) / 2
N = signal.shape[0]
secs = N / float(Fs)
Ts = 1.0 / Fs  # sampling interval in time

colour = (0, 0, 0)


def banded_analysis(bands, frequencies, fft):
    combined_data = list(zip(frequencies, fft))
    for band in bands:
        for i in range(len(combined_data)):
            data = combined_data[i]
            if data[0] > band:
                amount_low = combined_data[i - 1][1]
                amount_high = combined_data[i][1]

                freq_low = combined_data[i - 1][0]
                freq_high = combined_data[i][0]

                location = (band - freq_low) / (freq_high - freq_low)

                yield amount_high * location + amount_low * (1 - location)
                break


def fft_analysis(start):
    global colour
    end = start + int(analysis_period * Fs)
    data = signal[start:end]
    time_start = start * Ts
    time_end = end * Ts
    size = end - start

    t = np.arange(time_start, time_end - Ts / 2, Ts)  # time vector as scipy arange field / numpy.ndarray
    FFT = abs(fft(data, n=fftsize))
    FFT_side = FFT[range(fftsize // 2)]  # one side FFT range
    freqs = scipy.fftpack.fftfreq(fftsize, t[1] - t[0])
    fft_freqs = np.array(freqs)
    freqs_side = freqs[range(fftsize // 2)]  # one side frequency range
    fft_freqs_side = np.array(freqs_side)

    plt.clf()
    banded_data = list(banded_analysis(hz, freqs_side, FFT_side))
    r, g, b = banded_data[12], banded_data[36], banded_data[84]
    m = max(r, g, b) or 1
    colour = (r / m, g / m, b / m)
    plt.bar(list(range(len(hz))), banded_data)
    plt.show()


def visual():
    plt.ion()

    start = time.time()
    while True:
        curr = time.time()
        delta = curr - start

        idx = int(delta * Fs)

        fft_analysis(idx)
        plt.pause(analysis_period)
        # break  # time.sleep(1)


def pp():
    song = AudioSegment.from_wav("test.wav")
    play(song)


if __name__ == "__main__":
    p1 = Process(target=pp, args=())
    p1.start()
    p2 = Process(target=visual, args=())
    p2.start()
    p1.join()
    p2.join()
