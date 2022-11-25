import numpy as np
import scipy
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.io import loadmat
from sklearn.metrics import mean_squared_error
from datetime import datetime
from time import sleep
from tqdm import tqdm

#Import the ORGINAL wave file
samplerate_org, data_org = wavfile.read('original.wav')
length_org = data_org.shape[0] / samplerate_org
time_org = np.linspace(0., length_org, data_org.shape[0])
plt.subplot(3, 1, 1)
plt.plot(time_org,data_org)
plt.subplots_adjust(hspace=0.5)
plt.title("Original Signal")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude") 


#Import the DEGRADED wave file
samplerate_deg, data_deg = wavfile.read('degraded.wav')
length_deg = data_deg.shape[0] / samplerate_deg
time_deg = np.linspace(0., length_deg, data_deg.shape[0])
plt.subplot(3, 1, 2)
plt.plot(time_deg,data_deg)
plt.subplots_adjust(hspace=0.5)
plt.title("Degraded Signal")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude") 

# Load .mat file
degraded_files = loadmat('degraded_points.mat')

# Extract the keys of the dictionary
print(degraded_files.keys())

# Extract the array from the dictionary using the key
x = degraded_files["degraded_point"]

# Extract the click location
clicks = np.where(x == 1)

#Extract array from tuple
click_index = clicks[0]

#Number of clicks
num_clicks = len(click_index)

# Window Size
win_len = int(input('Enter the window size : '))
#win_len = x = range(1, 50, 2)

#Check wheather the filter window size is ODD or EVEN
if win_len % 2 == 1:
    print('The window size is ODD')
else:
    print('The window size is EVEN')
    print('CHANGE WINDOW SIZE TO ODD NUMBER')



def median_filter(data_deg, click_index, num_clicks, win_len):
    '''
    
    '''
    data_new = data_deg
    for i in range(num_clicks):
        #Number of padded zeros required
        pad_num = int((win_len - 1) / 2)

        #Extract data around clicks
        inputVar = data_new[click_index[i] - pad_num : click_index[i] + pad_num + 1]
        N = len(inputVar)

        #Add padded zeros
        padded_input = np.pad(inputVar, (pad_num, pad_num), 'constant', constant_values=(0, 0))
        
        new_mat = np.zeros(N)
        for j in range(N):
            a = padded_input[j:win_len+j]
            b = np.sort(a)
            new_mat[j] = b[int((win_len - 1) / 2)]
        data_new[click_index[i] - pad_num : click_index[i] + pad_num + 1] = new_mat
    return data_new

start_time = datetime.now()
for i in tqdm(range(100)):
    restored_data = median_filter(data_deg, click_index, num_clicks, win_len)
    sleep(0.3)
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
wavfile.write("restored.wav", samplerate_org, restored_data)
length = restored_data.shape[0] / samplerate_org
time_restored = np.linspace(0., length, restored_data.shape[0])
plt.subplot(3, 1, 3)
plt.plot(time_restored,restored_data)
plt.subplots_adjust(hspace=0.5)
plt.title("Restored Signal using Median Filter ")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()  

MSE = mean_squared_error(data_org, restored_data)
print(MSE)





