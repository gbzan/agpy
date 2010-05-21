#!/Library/Frameworks/Python.framework/Versions/Current/bin/python
import pyregion
import pyfits
import pywcs
import ds9
import numpy

def ds9_photometry(xpapoint):
    D = ds9.ds9(xpapoint)
    reg = pyregion.parse(D.get("regions selected -format ds9 -system wcs -sky fk5 -skyformat sexagesimal"))
    pf = D.get_pyfits()
    mask = reg.get_mask(pf[0])
    arr = pf[0].data
    hdr = pf[0].header
    wcs = pywcs.WCS(hdr)
    try:
        bmaj = float(hdr['BMAJ'])
        bmin = float(hdr['BMIN'])
        cd1,cd2 = wcs.wcs.cdelt[:2]
        ppbeam = bmin*bmaj / abs(cd1*cd2)
        print "BMAJ: %g  BMIN: %g  PPBEAM: %g   SUM/PPBEAM: %g" % (bmaj,bmin,ppbeam,arr[mask].sum()/ppbeam)
    except:
        pass
    return arr[mask].sum(),arr[mask].mean(),numpy.median(arr[mask]),arr[mask].std(),mask.sum()

if __name__ == "__main__":

    import sys
    xpaname = sys.argv[1]

    print "Sum: %g  Mean: %g  Median: %g  RMS: %g  NPIX: %i" % ds9_photometry(xpaname)

