

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d

color_cycle = [s['color'] for s in list(matplotlib.rcParams['axes.prop_cycle'])]

# this script lets you plot points, and produces a spline fit for you.

class LineBuilder:
    def __init__(self, ax, points, line, input_disable_key='1', activated=True):
        self.ax = ax
        self.line = line
        self.points = points
        self.xs = list(points.get_xdata())
        self.ys = list(points.get_ydata())
        self._ind = None
        self.epsilon = 12
        self.input_disable_key = input_disable_key
        self.keyboard_activated = activated
#         self.cid = points.figure.canvas.mpl_connect('button_press_event', self)

        points.figure.canvas.mpl_connect('button_press_event', self.button_press_callback)
        points.figure.canvas.mpl_connect('button_release_event', self.button_release_callback)
        points.figure.canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)
        points.figure.canvas.mpl_connect('key_press_event', self.key_press_callback)

    def get_ind_under_point(self, event):
        'get the index of the vertex under point if within epsilon tolerance'

        # avoid deleting when nothing is there
        if len(self.xs) == 0:
            return None


        # display coords
        xy = np.transpose( np.array([self.xs,self.ys]) )
        xyt = self.points.get_transform().transform(xy)

        xt, yt = xyt[:, 0], xyt[:, 1]
        d = np.sqrt((xt - event.x)**2 + (yt - event.y)**2)
        indseq = np.nonzero(np.equal(d, np.amin(d)))[0]
        ind = indseq[0]

        if d[ind] >= self.epsilon:
            ind = None

        return ind

    def update_points(self):
        self.points.set_data(self.xs, self.ys)

        if len(self.xs) > 3:
            f = interp1d(self.xs, self.ys, kind='cubic')
            xnew = np.linspace(np.min(self.xs), np.max(self.xs), \
                               num=101, endpoint=True)
            self.line.set_data(xnew, f(xnew))
        else:
            self.line.set_data([], [])


    def key_press_callback(self, event):
        'whenever a key is pressed'
        if event.key == self.input_disable_key:
            self.keyboard_activated = not self.keyboard_activated
            if self.keyboard_activated:
                self.points.set_alpha(1.0)
            else:
                self.points.set_alpha(0.1)

        if not self.keyboard_activated:
            return
        if not event.inaxes:
            return
        if event.key == ' ':

            print('self.xs = ', [xx-1 for xx in linebuilder.xs])
            print('self.ys = ', linebuilder.ys)
            pass
        elif event.key == 'd':
            ind = self.get_ind_under_point(event)
            if ind != None:
                del(self.xs[ind])
                del(self.ys[ind])
                self.update_points()
        elif event.key == 'i':

            if event.inaxes!=self.points.axes: return
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
            self.update_points()


        self.points.figure.canvas.draw()

    def button_press_callback(self, event):
        'whenever a mouse button is pressed'

        if event.inaxes is None:
            return
        if event.button != 1:
            return
        self._ind = self.get_ind_under_point(event)

    def button_release_callback(self, event):
        'whenever a mouse button is released'

        if event.button != 1:
            return
        self._ind = None

    def motion_notify_callback(self, event):
        'on mouse movement'

        if self._ind is None:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        x, y = event.xdata, event.ydata

        self.xs[self._ind],self.ys[self._ind] = x, y
        self.update_points()


fig = plt.figure()
ax = fig.add_subplot(111)

# this is the place where you put some custom plotting routines




x = np.linspace(-np.pi, np.pi)
y = np.sin(x)

plt.plot(x,y)


ax.set_title('click to build a spline')
points, = ax.plot([], [], 'o', c=color_cycle[1], markersize=6)  # empty points
line, = ax.plot([], [], '-' , c=color_cycle[1] ) # empty line
linebuilder = LineBuilder(ax, points, line, '1', True)

plt.legend()
plt.show()

# print('done!')
