"""
    call signature::

      figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')


    Create a new figure and return a :class:`matplotlib.figure.Figure`
    instance.  If *num* = *None*, the figure number will be incremented and
    a new figure will be created.  The returned figure objects have a
    *number* attribute holding this number.

    If *num* is an integer, and ``figure(num)`` already exists, make it
    active and return the handle to it.  If ``figure(num)`` does not exist
    it will be created.  Numbering starts at 1, matlab style::

      figure(1)

    If you are creating many figures, make sure you explicitly call "close"
    on the figures you are not using, because this will enable pylab
    to properly clean up the memory.

    Optional keyword arguments:

      =========   =======================================================
      Keyword     Description
      =========   =======================================================
      figsize     width x height in inches; defaults to rc figure.figsize
      dpi         resolution; defaults to rc figure.dpi
      facecolor   the background color; defaults to rc figure.facecolor
      edgecolor   the border color; defaults to rc figure.edgecolor
      =========   =======================================================

    rcParams defines the default values, which can be modified in the
    matplotlibrc file

    *FigureClass* is a :class:`~matplotlib.figure.Figure` or derived
    class that will be passed on to :meth:`new_figure_manager` in the
    backends which allows you to hook custom Figure classes into the
    pylab interface.  Additional kwargs will be passed on to your
    figure init function.
"""
    
    
    
    
    
    
    
    
    
    
import time
import pylab
# interactive mode on
pylab.ion()
timefig = pylab.figure(1)
timesub = pylab.subplot(111)
dt = 0.1
t = pylab.arange(0.0, 2.0, dt)
h = 1.2*pylab.sin(t)
lines = pylab.plot(t,h)
for i in range(8):
     t = t + dt
     h = 1.2*pylab.sin(t)
     lines[0].set_data(t,h)
     timesub.set_xlim((t[0],t[-1]))
     pylab.draw()
     time.sleep(1.0)
     
     
     
     
     
     
