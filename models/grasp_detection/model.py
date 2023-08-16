import os
from numpy.core.defchararray import array
import numpy as np
import matplotlib.pyplot as plt
import time

# import keyboard
import copy

# import serial
import joblib
from scipy import signal
from scipy.signal import butter

from teensy import arduino1
from sensors.imu import ImuAndEmg


class GraspDetection:
    def __init__(self, emglist_ch1, emglist_ch2) -> None:
        self.y_pred = None
        self.emglist_ch1 = emglist_ch1
        self.emglist_ch2 = emglist_ch2

    def butter_highpass(self, cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype="high", analog=False)
        return b, a

    def butter_highpass_filter(self, data, cutoff, fs, order=5):
        b, a = self.butter_highpass(cutoff, fs, order=order)
        y = signal.filtfilt(b, a, data)
        return y

    def mav(self, data_sec):
        MAV = np.mean(data_sec)
        return MAV

    def rms(self, data_sec):
        sq = np.square(data_sec)
        msq = np.mean(sq)
        RMS = np.sqrt(msq)
        return RMS

    def var(self, data_sec):
        sq = np.square(data_sec)
        ssq = np.sum(sq)
        VAR = ssq / (len(sq) - 1)
        return VAR

    def wl(self, data_sec):
        D = []
        for k in range(len(data_sec) - 1):
            d = abs(data_sec[k + 1] - data_sec[k])
            D.append(d)
        WL = np.sum(D)
        return WL

    def f1(self, x):
        if x >= 0.01:
            fx = 1
        else:
            fx = 0
        return fx

    def ssc(self, data_sec):
        F = []
        for k in range(len(data_sec) - 2):
            ff = self.f1(
                abs(data_sec[k + 1] - data_sec[k])
                * abs(data_sec[k + 2] - data_sec[k + 1])
            )
            F.append(ff)
        SSC = np.sum(F)
        return SSC

    def f2(self, x):
        if x >= 0.05:
            fx = 1
        else:
            fx = 0
        return fx

    def wamp(self, data_sec):
        F2 = []
        for k in range(len(data_sec) - 1):
            ff2 = self.f2(abs(data_sec[k] - data_sec[k + 1]))
            F2.append(ff2)
        WAMP = np.sum(F2)
        return WAMP

    def featureset(self, data, cutoff, fs):
        data_fil = abs(self.butter_highpass_filter(data, cutoff, fs))
        feat_set = [
            self.mav(data_fil),
            self.rms(data_fil),
            self.var(data_fil),
            self.wl(data_fil),
            self.ssc(data_fil),
            self.wamp(data_fil),
        ]
        return feat_set

    def EMG_classification(self, num_data, loaded_model, cutoff, fs):
        if len(self.emglist_ch1) == num_data and len(self.emglist_ch2) == num_data:
            data_now_ch1 = copy.deepcopy(self.emglist_ch1)
            data_now_ch2 = copy.deepcopy(self.emglist_ch2)
            ch_1_data_filtered = abs(
                self.butter_highpass_filter(data_now_ch1, cutoff, fs)
            )
            ch_2_data_filtered = abs(
                self.butter_highpass_filter(data_now_ch2, cutoff, fs)
            )
            feature_now = [
                self.mav(ch_1_data_filtered),
                self.rms(ch_1_data_filtered),
                self.var(ch_1_data_filtered),
                self.wl(ch_1_data_filtered),
                self.ssc(ch_1_data_filtered),
                self.wamp(ch_1_data_filtered),
                self.mav(ch_2_data_filtered),
                self.rms(ch_2_data_filtered),
                self.var(ch_2_data_filtered),
                self.wl(ch_2_data_filtered),
                self.ssc(ch_2_data_filtered),
                self.wamp(ch_2_data_filtered),
            ]
            self.y_pred = loaded_model.predict([feature_now])
            # print("y_pred", self.y_pred)

        else:
            pass

    def run(self):
        use_unicode = True
        charset = "utf-8"
        os.chdir("/Users/yunsangho/Desktop/3dobject/models/grasp_detection/")
        file_name1 = "220309_svm_0.25_lhr_with_500Hz.pkl"
        loaded_model = joblib.load(file_name1)
        cutoff = 50
        fs = 500

        while True:
            self.EMG_classification(
                ImuAndEmg().emglist_max_length,
                loaded_model,
                cutoff,
                fs,
            )
            # t_inference = threading.Thread(
            #     target=self.EMG_classification,
            #     args=(
            #         self.emglist_ch1,
            #         self.emglist_ch2,
            #         ImuAndEmg().emglist_max_length,
            #         loaded_model,
            #         cutoff,
            #         fs,
            #     ),
            # )
            # time.sleep(0.1)
