import numpy as np
from scipy.interpolate import interpn
import pandas as pd
import matplotlib.pyplot as plt


def sg_lut(ifile, thetas, aott, rh, amod=2, diff=True, skipr=20):

    ws = pd.read_csv(ifile, skiprows=skipr)
    ws = ws[ws.amod == amod]
    dim = [len(pd.unique(ws.sza)), len(pd.unique(ws.aot)), len(pd.unique(ws.rh)), len(pd.unique(ws.ws))]
    slopelut = np.zeros(dim)

    if diff:
        for szi, sza in enumerate(pd.unique(ws.sza)):
            for aoti, aot in enumerate(pd.unique(ws.aot)):
                for rhi, rh in enumerate(pd.unique(ws.rh)):
                    cd = ws.D[(ws.sza == sza) & (ws.aot == aot) & (ws.rh == rh)]
                    slopelut[szi, aoti, rhi, :] = cd
    print(slopelut)
    slopeut = interpn((pd.unique(ws.sza), pd.unique(ws.aot), pd.unique(ws.rh)),
                      slopelut, np.array([thetas, aott, rh]).T)
    return pd.DataFrame({"D":np.squeeze(slopeut), "w":pd.unique(ws.ws)})

if __name__ == '__main__':
    DW=sg_lut('LUT/SPE_OSOAA_GoyensRuddick2022v1.00.csv', 30, 0.2, 70)
    print(DW)
    plt.figure()
    plt.plot(DW.w, DW.D)
    plt.show()
