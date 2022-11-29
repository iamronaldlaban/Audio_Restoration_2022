# Audio Restoration using Median Filer and Cubic Spline Filter

## High-level Description of the project
This assignment builds on Assignment I. We assume that we have successfully detected the clicks and we are applying different interpolation methods to restore the audio, such as
- median filtering
- cubic splines

---

## Installation and Execution
- matplotlib==3.4.3
- numpy==1.20.3
- playsound==1.2.2
- scikit_learn==1.1.3
- scipy==1.7.1
- tqdm==4.62.3

Provide details on the Python version and libraries (e.g. numpy version) you are using. One easy way to do it is to do that automatically:
```sh                                 
pip3 install pipreqs

pipreqs $project/path/requirements.txt
```
For more details check [here](https://github.com/bndr/pipreqs)


Afer installing all required packages you can run the demo file simply by typing:
```sh
python demo_audio_restoration.py
```
---

## Methodology and Results
**Methodology**

###Median Filter###
  1.  Read the original signal and the degraded signal using `wavfile.read`
  2.  To know the position of the clicks, load the **.mat** file using `loadmat`
  3.  As reading a **.mat** file creates a dictioary, we need to extract the keys and using the correct keys extractt the degraded points.
  4.  From degraded points using `np.where` extract the indexes of the clicks.
  5.  Enter the Window Length for the median filter from the user. *Note: The window size must be ODD, for even window length the program will stop execution
  6.  Call the function(*user-defined*) `median_filter` to obtain the restored signal
      1.  Depending on the click position, pass window length number of parameters around the click, inculding the click.
      2.  Depending on the window lenght, *window length - 1 / 2* number of zeros are padded on both sides of the data.
      3.  A window is passed over the data from the starting point and shifted to the right with a increment of one, until the boundary of thr window covers the last data point.
      4. As the window is passing, the data points in the window are sorted in acensending order and the median value is selected from that data set and stored in a new matrix.
      5.  Shift the window by one point and repeat the above step until the boundary includes the last point.
      6. The new matrix is the same size as the window length. Replace the old data point with the content of the new matrix. The content of the new matrix are filtered output wherein the click (*high amplitude postive/negative*) value is repaced by its neighboring value.
      7. Repeat step i. to vi. for all the click values.
      8. A progress bar was added to check the progress of the median filter evaluation. Also the execution time was measured.
  7.  The output signal at the end of median filter is restored signal free from clicks.
  8.  The restored signal is write as `.wav` file using the command `wavfile.write`.
  9.  The mean squared error between original signal and restored signal was evaluated.
  10.  A unittest function was added to check the proper functioning of the user defined median filter with the in-built median filter `scipy.signal.medfilt'.
  11.  The results are plotted as seen in Figure 1.
     



**Results**

1. For the median filter, different lengths were explored to test the effectiveness of the restoration. In particular, XXXX were tested and XXX was observed to deliver the lowest MSE, as shown in the figure below.

<img src="MedianFilter_MSEvsLength.png" width="350">

The restored waveform <output_medianFilter.wav> with the optimal filter length is given below:



2. Using the cubic splines, we observe ....

The restored waveform <output_cubicSplines.wav> with the optimal filter length is given below:


3. Comparing the two different interpolation methods, we notice that method X achieves a lower MSE. The runtime of XX method is .....

After listening to the two restored files, we notice ...


---
## Credits

This code was developed for purely academic purposes by XXXX (add github profile name) as part of the module ..... 

Resources:
- XXXX
- XXX





