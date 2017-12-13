# -*- coding: utf-8 -*-
"""
@author: Administrator
"""
from keras.models import load_model
netfile = "/sun/sites/etennis.top/yyonline/yyonline/media/tmp/net_0.h5"
model = load_model(netfile)
import numpy as np
y = model.predict(np.zeros((2,50,9)))
print(y)