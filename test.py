import numpy as np
import scipy
from playsound import playsound
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.io import loadmat
from sklearn.metrics import mean_squared_error
from time import sleep
from tqdm import tqdm


samplerate, data = wavfile.read('degraded.wav')
length = data.shape[0] / samplerate
print(f"length = {length}s")

# playsound('degrade.wav')

time = np.linspace(0., length, data.shape[0])
plt.figure(figsize=(15, 5))
plt.plot(time, data, label="Degraded Signal")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()

# Load .mat file
degraded_files = loadmat('degraded_points.mat')

# Extract the keys of the dictionary
print(degraded_files.keys())
x = degraded_files["degraded_point"]

# Extract the click location
clicks = np.where(x == 1)
points = clicks[0]
P = len(points)
#print(P)
#print(points)


# Window Size
win_len = int(input('Enter the window size : '))

if win_len % 2 == 1:
    print('The window size is ODD')
else:
    print('The window size is EVEN')
    print('CHANGE WINDOW SIZE TO ODD NUMBER')



def median_filter(data, points, P, win_len):
    data_new = data
    for i in range(P):
        A = int((win_len - 1) / 2)
        inputVar = data_new[points[i] - A : points[i] + A + 1]
        #print(inputVar)
        N = len(inputVar)
        padded_input = np.pad(inputVar, (A, A), 'constant', constant_values=(0, 0))
        #print(padded_input)
        input_len = len(padded_input)
        c = np.zeros(N)
        for j in range(N):
            a = padded_input[j:win_len+j]
            b = np.sort(a)
            c[j] = b[int((win_len - 1) / 2)]
        #print(c)
        data_new[points[i] - A : points[i] + A + 1] = c
    return data_new

for i in tqdm(range(100)):
    clean_data = median_filter(data, points, P, win_len)
    sleep(0.3)
wavfile.write("restored.wav", samplerate, clean_data)


length = clean_data.shape[0] / samplerate
print(f"length = {length}s")
time = np.linspace(0., length, clean_data.shape[0])
plt.figure(figsize=(15, 5))
plt.plot(time, clean_data, label="Restored Signal")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()   



samplerate2, orginal_data = wavfile.read('clean_input.wav')
length = orginal_data.shape[0] / samplerate2
print(f"length = {length}s")

# MSE = mean_squared_error(orginal_data, clean_data)
# print(MSE)

    