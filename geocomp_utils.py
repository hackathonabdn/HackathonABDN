import os
import pandas as pd
import numpy as np
from scipy import stats
from scipy.signal import butter, lfilter
from scipy import fftpack
import math

def sum(x):
    return float(np.sum(x))

def mean(x):
    return float(np.mean(x))

def sd(x):
    y = np.std(x)
    if not is_valid_num(y):
        print('sd: %f'%y)
    return float(y)

def iqr(x):
    y = np.subtract(*np.percentile(x,[75,25]))
    if not is_valid_num(y):
        print('iqr: %f'%y)
    return float(y)

    
def percentile(x, p):
    y = np.percentile(x, p)
    if np.isnan(y).any() or np.isinf(y).any():
        print('percentile: %f'%str(np.argwhere(np.isnan(y))))
    return y

def peak2peak_amp(x):
    y = np.max(x) - np.min(x)
    if not is_valid_num(y):
        print('peak2peak: %f'%y)
    return float(y)

def power(x):
    y = np.sum(np.square(x))
    if not is_valid_num(y):
        print('power: %f'%y)
    return float(y)
    
def log_power(x):
    printed = False
    mf = 0.00001
    x = np.add(x,mf)
    log_power = np.sum(np.log(np.square(x)))
    if not printed:
        if 0 in x:
            print(x)
            printed = True
    if not is_valid_num(log_power):
        print('log_power: %f'%log_power)
    return float(log_power)

def lag_one_autocorr(x, m=None):
    num = 0
    if m is None:
        m = np.mean(x)
    i = 0    
    while i < len(x)-1:
        num += (x[i] - m) * (x[i+1] - m)
        i += 1
    denom = np.sum(np.square(np.subtract(x,m)))
    if denom > 0:
   	    return float(num/denom)
    else:
        return 0

def kurtosis(x):
    y = stats.kurtosis(x)
    if not is_valid_num(y):
        print('kurt: %f'%y)
    return float(y)

def skewness(x, m=None):
    if m is None:
        m = np.mean(x)
    num = np.sum(np.power(np.subtract(x,m),3))/len(x)
    denom = np.power(np.sqrt(np.sum(np.square(np.subtract(x,m)))/(len(x)-1)), 3)
    if denom > 0:
    	return float(num/denom)
    else:
        return 0

def corr(a,b):  
    y = np.corrcoef(a,b)[0,1]
    if not is_valid_num(y):
        print('corr: %f'%y)
    return float(y)

def zero_cross(x):
    count = 0
    median = np.median(x)
    last_sign = np.sign(x[0])
    i = 1
    while i < len(x):
        if np.sign(x[i]) != last_sign:
            last_sign = np.sign(x[i])
            count +=1
        i+=1
    if not is_valid_num(count):
        print('zero cross: %f'%count)
    return count
    

def median_cross(x, m=None):
    if m is None:
        m = np.median(x)
    count = 0
    i=0
    while i < len(x)-1:
        count += np.absolute(np.sign(x[i] - m) - np.sign(x[i+1] - m))
        i+=1
    return count/2
        
#New features
def mag(x, y, z):
    x_2 = np.square(x)
    y_2 = np.square(y)
    z_2 = np.square(z)
    mag =  np.sqrt(np.add(x_2, np.add(y_2,z_2)))   
    return mag
    
def rho(x, y, z):
    theta = (180/math.pi) * math.atan(x/(math.sqrt(math.pow(y, 2) + math.pow(z,2))))
    return theta

def phi(x, y, z):
    theta = (180/math.pi) * math.atan(y/(math.sqrt(math.pow(x, 2) + math.pow(z,2))))
    return theta
    
def theta(x, y, z):
    theta = (180/math.pi) * math.atan(z/(math.sqrt(math.pow(y, 2) + math.pow(x,2))))
    return theta
    
def energy(x, y, z):
    ex = np.sqrt(np.sum(np.square(np.subtract(x,mean(x)))))
    ey = np.sqrt(np.sum(np.square(np.subtract(y,mean(y)))))
    ez = np.sqrt(np.sum(np.square(np.subtract(z,mean(z)))))
    
    e = (1/(3 * len(x))) * (ex + ey + ez)
    return e
    
def root_square_mean(x):
    y = np.sqrt(np.mean(np.square(x)))
    if not is_valid_num(y):
        print('rms: %f'%y)
    return y
    
def mean_abs_dev(x):
    m = np.mean(x)
    y = np.mean(np.subtract(x, m))
    if not is_valid_num(y):
        print('mean_abs_dev: %f'%y)
    return float(y)
    
def spec_centroid(x):
    i = range(x)
    return np.sum(np.multiply(x, i))/np.sum(x)
    
def spec_entropy(x):
    N = len(x)
    p = np.divide(np.square(x), N)
    pi = np.divide(p, np.sum(p))
    H = - np.sum(np.multiply(pi, np.log(pi)))
    if math.isnan(H):
        print(p)
        print(pi)
        print(H)
    return H


def rms_vector(tw):
    x = tw['x'].values
    y = tw['y'].values
    z = tw['z'].values
    
    rms = []
    for i in range(len(x)):  
        val = (x[i] * x[i]) + (y[i] * y[i]) +(z[i] * z[i])
        val = np.sqrt(val)/3
        rms.append(val)
    rms = np.array(rms)
    return rms

def is_valid_num(x):
    if not np.isnan(x) and not np.isinf(x):
        return True
    else:
        return False


def get_time_features(data):
    features = []
    data = data+0.001 
    
    features.append(sum(data)) #0
    
    features.append(mean(data)) #4
  
    features.append(sd(data)) #8

    features.append(iqr(data)) #12

    features.extend(percentile(data, [10,25,50,75,90])) #13 - 17

    features.append(peak2peak_amp(data)) #28

    features.append(power(data)) #31

    features.append(log_power(data)) #34

    features.append(lag_one_autocorr(data)) #37

    features.append(kurtosis(data)) #40

    features.append(skewness(data)) #43

    features.append(median_cross(data)) #49
    
    features.append(root_square_mean(data))

    features.append(np.max(data))

    features.append(np.min(data))

    features.append(mean_abs_dev(data))
    
    return features


def extract_time_features(time_windows, class_attr, n_comps=None):   
    data = []
    _class = []
    l = len(time_windows[0])
    for tw in time_windows:
        if tw.shape[0] == l:
            features = []
            features.extend(get_time_features(tw))
            data.append(features)
            if class_attr is not None:
                _class.append(tw[class_attr].iloc[0])
    dataset = np.array(data, dtype=np.float32)
    if class_attr is not None:
    	return dataset, _class
    else:
        return dataset

def split_windows(data, width, overlap_ratio=None, min_width=1):
    time_windows = []
    increment = width
    if overlap_ratio is not None:
        increment = int(width * (1-overlap_ratio))
        
    i = 0
    N = len(data)
    while i < N:  
        start = i
        end = start+width
        if end > N:
            end = N
        elif (N - end) < min_width:
            end = N 
        #print str(start)+" "+str(end)
        tw = data[start:end]
        #classlabels = tw['class'].unique()
        #if len(classlabels) == 1:
        time_windows.append(tw)
    
        increment = end-start
        i = int(i + increment)
    return time_windows