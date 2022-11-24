import numpy as np


def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list


# Synesthesia settings
starting_freq = 40
num_bands = 96
bands_per_octave = 24
analysis_period = 0.01
fftsize = 4096

hz = [starting_freq]

for i in range(num_bands // bands_per_octave):
    hz.append(hz[-1] * 2)

octaves = list(hz)
hz = (flatten_list([
    list(np.arange(i, 2 * i, i / bands_per_octave))
    for i in hz[:-1]
]))
