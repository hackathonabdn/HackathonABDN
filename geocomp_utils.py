import os
import pandas as pd
import numpy as np
from scipy import stats
from scipy.signal import butter, lfilter
from scipy import fftpack
import math

def sum(x):
    return np.sum(x)

def mean(x):
    return np.mean(x)

def sd(x):
    y = np.std(x)
    if not is_valid_num(y):
        print('sd: %f'%y)
    return y

def iqr(x):
    y = np.subtract(*np.percentile(x,[75,25]))
    if not is_valid_num(y):
        print('iqr: %f'%y)
    return y

    
def percentile(x, p):
    y = np.percentile(x, p)
    if np.isnan(y).any() or np.isinf(y).any():
        print('perc: '+str(np.argwhere(np.isnan(y))))
    return y

def peak2peak_amp(x):
    y = np.max(x) - np.min(x)
    if not is_valid_num(y):
        print('peak2peak: %f'%y)
    return y

def power(x):
    y = np.sum(np.square(x))
    if not is_valid_num(y):
        print('power: %f'%y)
    return y
    
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
    return log_power

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
   	    return num/denom
    else:
        return 0

def kurtosis(x):
    y = stats.kurtosis(x)
    if not is_valid_num(y):
        print('kurt: %f'%y)
    return y

def skewness(x, m=None):
    if m is None:
        m = np.mean(x)
    num = np.sum(np.power(np.subtract(x,m),3))/len(x)
    denom = np.power(np.sqrt(np.sum(np.square(np.subtract(x,m)))/(len(x)-1)), 3)
    if denom > 0:
    	return num/denom
    else:
        return 0

def corr(a,b):  
    y = np.corrcoef(a,b)[0,1]
    if not is_valid_num(y):
        print('corr: %f'%y)
    return y

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
    return y
    
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

def get_time_features(tw):
    features = []
    x = tw['x'].values+0.001
    y = tw['y'].values+0.001
    z = tw['z'].values+0.001
    m = mag(x,y,z) 
        
    ax = x[int(len(x)/2)]
    ay = y[int(len(y)/2)]
    az = z[int(len(z)/2)]    
    
    #if indx == 0:
     
    features.append(sum(x)) #0
    features.append(sum(y)) #1
    features.append(sum(z)) #2
    features.append(sum(m)) #3 
    #elif indx == 1:
    features.append(mean(x)) #4
    features.append(mean(y)) #5
    features.append(mean(z)) #6
    features.append(mean(m)) #7    
    #elif indx == 2:
    features.append(sd(x)) #8
    features.append(sd(y)) #9 H
    features.append(sd(z)) #10
    features.append(sd(m)) #11
    #elif indx == 3:
    features.append(iqr(x)) #12
    features.append(iqr(y)) #13 H
    features.append(iqr(z)) #14
    features.append(iqr(m)) #15
    #elif indx == 4:
    features.extend(percentile(x, [10,25,50,75,90])) #13 - 17
    features.extend(percentile(y, [10,25,50,75,90])) #18 - 22
    features.extend(percentile(z, [10,25,50,75,90])) #23 - 27
    features.extend(percentile(m, [10,25,50,75,90]))
    #elif indx == 5:
    features.append(peak2peak_amp(x)) #28
    features.append(peak2peak_amp(y)) #29 
    features.append(peak2peak_amp(z)) #30
    features.append(peak2peak_amp(m)) 
    #elif indx == 6:
    features.append(power(x)) #31
    features.append(power(y)) #32 H
    features.append(power(z)) #33
    features.append(power(m))
    #elif indx == 7:
    features.append(log_power(x)) #34
    features.append(log_power(y)) #35 H
    features.append(log_power(z)) #36
    features.append(log_power(m))
    #elif indx == 8:
    features.append(lag_one_autocorr(x)) #37
    features.append(lag_one_autocorr(y)) #38
    features.append(lag_one_autocorr(z)) #39 H
    features.append(lag_one_autocorr(m))
    #elif indx == 9:
    features.append(kurtosis(x)) #40
    features.append(kurtosis(y)) #41
    features.append(kurtosis(z)) #42
    features.append(kurtosis(m))
    #elif indx == 10:
    features.append(skewness(x)) #43
    features.append(skewness(y)) #44
    features.append(skewness(z)) #45
    features.append(skewness(m))
    #elif indx == 11:
    #features.append(corr(x,y)) #46
    #features.append(corr(x,z)) #47
    #features.append(corr(y,z)) #48 H
    #elif indx == 12:
    features.append(zero_cross(x)) #49
    features.append(zero_cross(y)) #50 H
    features.append(zero_cross(z)) #51
    features.append(zero_cross(m))
    #elif indx == 13:
    features.append(energy(x,y, z))
    #elif indx == 14:
    features.append(root_square_mean(x))
    features.append(root_square_mean(y))
    features.append(root_square_mean(z))
    features.append(root_square_mean(m))
    #elif indx == 15:
    features.append(np.max(x))
    features.append(np.max(y))
    features.append(np.max(z))
    features.append(np.max(m))
    #elif indx == 16:
    features.append(np.min(x))
    features.append(np.min(y))
    features.append(np.min(z))        
    features.append(np.min(m))
    #elif indx == 17:
    features.append(mean_abs_dev(x))
    features.append(mean_abs_dev(y))
    features.append(mean_abs_dev(z))
    features.append(mean_abs_dev(m))
    #elif indx == 18:
    #features.append(rho(ax, ay, az))
    #features.append(phi(ax, ay, az))
    #features.append(theta(ax, ay, az))
    
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
    
def split_windows(_df, samp_rate, w, overlap_ratio=None, overlap_time=None, min_width=1):
    time_windows = []
    width = samp_rate * w  
    increment = width
    if overlap_time is not None:
        increment = samp_rate * overlap_time
    elif overlap_ratio is not None:
        increment = int(width * (1-overlap_ratio))
        
    i = 0
    N = len(_df.index)
    while i < N:  
        start = i
        end = start+width
        if end > N:
            end = N
        elif (N - end) < samp_rate * min_width:
            end = N 
        #print str(start)+" "+str(end)
        tw = _df.iloc[start:end]
        classlabels = tw['class'].unique()
        if len(classlabels) == 1:
            time_windows.append(tw)
    
        increment = end-start
        i = int(i + (increment))
    return time_windows