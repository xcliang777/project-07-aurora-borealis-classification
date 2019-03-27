#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 11:25:25 2018

-------------------------------------------------------------------------------
Unless stated otherwise, all data in the OATH Dataset is licensed under a
<a href="https://creativecommons.org/licenses/by/4.0/">Creative Commons 4.0 
Attribution License (CC BY 4.0)</a> and the accompanying source code is 
licensed under a <a href="https://opensource.org/licenses/BSD-2-Clause">
BSD-2-Clause License</a>.
In particular, all actual image data included in the tarball are modified from 
the <a href="https://www.nasa.gov/mission_pages/themis/spacecraft/asi.html">
THEMIS all-sky imagers </a>.

We thank H. Frey for giving us permission to include these data.
Copyright for these data remains with NASA.

We acknowledge NASA contract NAS5-02099 and V. Angelopoulos for use of data 
from the THEMIS Mission. Specifically: S. Mende and E. Donovan for use of the
ASI data, the CSA for logistical support in fielding and data retrieval from
the GBO stations, and NSF for support of GIMNAST through grant AGS-1004736.
-------------------------------------------------------------------------------

"""

from sklearn.linear_model import RidgeClassifier
from sklearn.metrics import confusion_matrix

import h5py
import numpy as np
import pandas as pd
import numpy.random as rand

#base_dir = "/mnt/blackdisk/oath/oath/"
base_dir = "../"

# read classifications
df = pd.read_csv(base_dir+"classifications/classifications.csv", skiprows=18)
ndata = len( df["picNum"])

f = h5py.File( base_dir+"features/auroral_feat.h5", "r" )
features = f["Logits"].value
f.close()

alpha = 0.03
avgscore = np.zeros(5)
# the split has been generated by
# rand.seed(1804)
# idxs = np.argsort(rand.rand(5,ndata),axis=1)
# np.savetxt(base_dir+"classifications/train_test_split.csv", idxs, delimiter=",")
idxs = np.loadtxt(base_dir+"classifications/train_test_split.csv", delimiter=",").astype(int)
cnt = 0
for idx in idxs:
  ntrain = int(np.round( 0.7*ndata ))
  idx_train = idx[0:ntrain]
  idx_test = idx[ntrain:]

  # use 'class2' here to train machine on two classes
  # only, aurora and non-aurora (instead of 'class6')
  X_train = features[idx_train,:]
  y_train = df["class6"][idx_train]
  X_test = features[idx_test,:]
  y_test = df["class6"][idx_test]
  
  clf = RidgeClassifier( random_state=10*cnt, normalize=False, alpha=alpha )
  clf.fit( X_train, y_train )
  avgscore[cnt] = clf.score( X_test, y_test )
  cnt += 1
print("==========================")
print("follow are testing results")
print("==========================")
print("average accuracy: ", np.mean(avgscore))
print("standard deviation of accuracy: ", np.std(avgscore))
#print( np.mean(avgscore), np.std(avgscore) )
y_pred = clf.predict( X_test )
mat = confusion_matrix(y_test, y_pred)
print("confusion matrix is:")
print( mat )
