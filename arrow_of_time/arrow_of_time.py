#!/usr/bin/env python

"""A simulation of time..."""

from collections import defaultdict

import random


# Particle types
A = "A"
B = "B"


class Particle(object):
	"""A single particle."""
	def __init__(self, type=A, x=0.0, y=0.0, vx=0.0, vy=0.0):
		self.type = type
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy


class Universe(object):
	"""A model of the universe where there are two fundamental particle types.
	
	Particles of type A aniahlate upon collision producing three particles of type
	B. The first two type B particles will have the same velocities as the type A
	particles and the third will have the X-velocity of the first A and the
	Y-velocity of the second A.
	
	If three type B particles collide, two type A particles are produced where the
	first two type B particles effectively become type A particles and the third
	is deleted.
	"""
	
	def __init__(self, width, height):
		# A list of Particles
		self.particles = []
		self.width = width
		self.height = height
	
	
	def step(self, step=1):
		"""Step the simulation by the specified number of time steps (may be
		negative to run time backwards)."""
		for _, _step in sorted([(0 * step, self._step_positions),
		                        (1 * step, self._step_collisions)]):
			_step(step)
	
	
	def _step_positions(self, step):
		# Move all particles according to their velocities
		for p in self.particles:
			p.x += step * p.vx
			p.y += step * p.vy
			
			p.x %= self.width
			p.y %= self.height
	
	def _step_collisions(self, step):
		# Collect particles which are on the same grid square. A dictionary from
		# grid-squares to lists of particles in those squares.
		grid = defaultdict(list)
		for p in self.particles:
			grid[(p.x, p.y)].append(p)
		
		# Determine action to take as a result of collisions
		for _, collider in sorted([(0 * step, self._collide_aa),
		                           (1 * step, self._collide_bbb)]):
			collider(grid, step)
	
	
	def _collide_aa(self, grid, step):
		"""Check for and apply collision effects of two A particles colliding."""
		for (x, y), ps in grid.items():
			a_particles = [p for p in ps if p.type == A]
			
			if step > 0:
				a_iter = iter(a_particles)
			else:
				a_iter = iter(reversed(a_particles))
			for a1, a2 in zip(a_iter, a_iter):
				ps.remove(a1)
				ps.remove(a2)
				
				a1.type = B
				a2.type = B
				b3 = Particle(type=B, x=a1.x, y=a2.y, vx=a1.vx, vy=a2.vy)
				self.particles.insert(self.particles.index(a2) + 1, b3)
	
	
	def _collide_bbb(self, grid, step):
		"""Check for and apply collision effects of three B particles colliding."""
		for (x, y), ps in grid.items():
			b_particles = [p for p in ps if p.type == B]
			
			if step > 0:
				b_iter = iter(reversed(b_particles))
			else:
				b_iter = iter(b_particles)
			
			for b1, b2, b3 in zip(b_iter, b_iter, b_iter):
				ps.remove(b1)
				ps.remove(b2)
				ps.remove(b3)
				
				b1.type = A
				b2.type = A
				# The third particle is just removed
				self.particles.remove(b3)
	
	def __str__(self):
		return ", ".join("{}({}, {})".format(p.type, p.x, p.y) for p in u.particles)


def make_random_universe(width, height, n_particles, types):
	"""Create a random universe with an equal distribution of the supplied set of
	particle types.
	"""
	u = Universe(width, height)
	for n in range(n_particles):
		u.particles.append(Particle(type=random.choice(types),
		                            x=random.randint(0, width-1),
		                            y=random.randint(0, height-1),
		                            vx=random.randint(0, width-1),
		                            vy=random.randint(0, height-1)))
	return u




if __name__=="__main__":
	w, h = 100, 100
	#n_particles = 100
	#u = make_random_universe(w, h, n_particles, [A])
	
	u = Universe(w, h)
	u.particles.append(Particle(A, 0, 0, 1, 0))
	u.particles.append(Particle(A, 6, 0, -1, 0))
	u.particles.append(Particle(A, 3, 3, 0, -1))
	
	n_steps = 10
	print(sum(1 for p in u.particles if p.type == B))
	for _ in range(n_steps):
		u.step()
		print(str(u))
	print(sum(1 for p in u.particles if p.type == B))
	for _ in range(n_steps):
		u.step(-1)
		print(str(u))
	print(sum(1 for p in u.particles if p.type == B))
