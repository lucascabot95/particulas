#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class ParticleBox:
	def __init__(self,
				 init_state = [[1, 0, 0, -1],
							   [-0.5, 0.5, 0.5, 0.5],
							   [-0.5, -0.5, -0.5, 0.5]],
				 bounds = [0, 100, 0, 100],
				 size = 0.04):
		self.init_state = np.asarray(init_state, dtype=float)
		self.size = size
		self.state = self.init_state.copy()
		self.time_elapsed = 0
		self.bounds = bounds
		self.time_stop=1
		self.init_coll = np.zeros((self.init_state.size/4,1),dtype=int)
		for x in range(0 , self.init_coll.size):
			self.init_coll[x]=x

	def monitor_col(self,j,k,xy):
		if  abs(self.state[j,xy]-self.state[k,xy])<2*self.size and self.border(j,k) :
			return True
		return False

	def out_monitor(self,j,k,xy):
		if abs(self.state[j,xy]-self.state[k,xy])>2.25*self.size and self.border(j,k):
			return True
		return False

	def border(self,j,k):
		notK_border=False
		notJ_border=False
		border_limit=1.1
		if self.bounds[0] +border_limit*self.size <= self.state[j,0] <= self.bounds[1] - border_limit*self.size and self.bounds[2] +border_limit*self.size<= self.state[j,1] <= self.bounds[3] - border_limit*self.size :
			notJ_border=True
		if -self.bounds[0] +border_limit*self.size <= self.state[k,0] <= self.bounds[1] - border_limit*self.size and self.bounds[2] +border_limit*self.size<= self.state[k,1] <= self.bounds[3] - border_limit*self.size :
			notK_border=True
		if notJ_border and notK_border:
			return True
		return False

	def changeVel(self,j,k):
		gh=self.state[j,2]
		self.state[j,2]=self.state[k,2]
		self.state[k,2]=gh
		gh=self.state[j,3]
		self.state[j,3]=self.state[k,3]
		self.state[k,3]=gh
		self.init_coll[k]=j
		self.init_coll[j]=k



	def step(self, dt):

		"""step once by dt seconds"""
		if self.time_stop==1  :
			self.time_elapsed += dt
			self.state[:, 0] +=	 dt * self.state[:, 2] 
			self.state[:, 1] +=	 dt * self.state[:, 3] 
		# check for crossing boundary
		crossed_x1 = (self.state[:, 0] < self.bounds[0] + self.size)
		crossed_x2 = (self.state[:, 0] > self.bounds[1] - self.size)
		crossed_y1 = (self.state[:, 1] < self.bounds[2] + self.size)
		crossed_y2 = (self.state[:, 1] > self.bounds[3] - self.size)

		for j in range(0, init_state[:,0].size):
			for k in range(j, init_state[:,0].size):
				if j!=k:

					re_col=True

					if self.init_coll[k]==j and self.init_coll[j]==k  :
						re_col=False
						if self.out_monitor(j,k,0) or self.out_monitor(j,k,1):
							self.init_coll[k]=k
							self.init_coll[j]=j
					if self.monitor_col(j,k,0) and self.monitor_col(j,k,1) and re_col:
						self.changeVel(j,k)

		self.state[crossed_x1 | crossed_x2, 2] *= -1
		self.state[crossed_y1 | crossed_y2, 3] *= -1
		

		

#------------------------------------------------------------
# set up initial state
init_state = np.random.random((50,4))
#random x,y desde 2 a 98
init_state[:, :2]*=96
init_state[:, :2]+=2
#random vel (vx,vy) desde -75 a 75 
init_state[:, 2:]*=(init_state[:, 2:]-0.5)*2
init_state[:, 2:]*=75

#print init_state
box = ParticleBox(init_state, size=1)
dt = 1. / 50 # 30fps

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
particles, = ax.plot([], [], 'bo', ms=5)

# initialization function: plot the background of each frame
def init():
	global box
	particles.set_data([], [])
	return particles,

# animation function.  This is called sequentially
def animate(i):
	global box, dt, ax, fig
	box.step(dt)

	particles.set_data(box.state[:, 0], box.state[:, 1])
	particles.set_markersize(5)
	return particles,
	

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

plt.show()
