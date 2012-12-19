from image_registration.fft_tools import upsample
import numpy as np
import pytest
import itertools

def gaussian(x):
    return np.exp(-x**2/2.)

@pytest.mark.parametrize(('imsize','upsample_factor'),
    list(itertools.product(range(11,27),range(1,25))))
def test_plot_tests(imsize, upsample_factor,doplot=False):
    """
    Test that, when upsampled, z[::upsample_factor] = g

    Tested for offsets in the *input gaussian function*

    This doesn't imply you know what's going on, just that the behavior is consistent

    ONLY tests for OUTSIZE=INSIZE*UPSAMPLE_FACTOR
    """
    # always centered
    x = np.arange(imsize)
    g = gaussian(x - imsize/2.)
    xz,z = upsample.zoom1d(g,upsample_factor,outsize=g.size*upsample_factor,return_xouts=True)

    if doplot:
        print x,xz
        from pylab import *
        figure(1); clf()
        plot(xz,z)
        plot(x,g)
        plot(xz,gaussian(xz-imsize/2.))
        figure(2); clf()
        plot(z[::upsample_factor])
        plot(g)
        figure(3); clf()
        plot(g-z[::upsample_factor])
    assert ((gaussian(xz - imsize/2.)-z)**2).sum() < 0.001

@pytest.mark.parametrize(('imsize','upsample_factor','offset'),
    list(itertools.product(range(11,27),range(1,25),(-1,0,1))))
def test_gaussian_upsample(imsize, upsample_factor, offset):
    """
    Test that, when upsampled, z[::upsample_factor] = g

    Tested for offsets in the *input gaussian function*

    This doesn't imply you know what's going on, just that the behavior is consistent

    ONLY tests for OUTSIZE=INSIZE*UPSAMPLE_FACTOR
    """
    x = np.arange(imsize)
    g = gaussian(x-imsize/2.-offset)
    xz,z = upsample.zoom1d(g,upsample_factor,outsize=g.size*upsample_factor,return_xouts=True)

    assert ((gaussian(xz - imsize/2. -offset)-z)**2).sum() < 0.001
