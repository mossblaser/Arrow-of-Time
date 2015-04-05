#!/usr/bin/env python

"""A simulation of time..."""

from collections import defaultdict

import random


# Particle types
A = "A"
B = "B"
C = "C"


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
	
	Particles of type A aniahlate upon collision producing two particles of type B
	and C which have the same velocities of the two A particles.
	
	If a B and C particle collide, two type A particles are produced, taking the
	same velocities again.
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
		                           (1 * step, self._collide_bc)]):
			collider(grid, step)
	
	
	def _collide_aa(self, grid, step):
		"""Check for and apply collision effects of two A particles colliding."""
		for (x, y), ps in grid.items():
			a_particles = [p for p in ps if p.type == A]
			
			a_iter = iter(a_particles)
			for a1, a2 in zip(a_iter, a_iter):
				ps.remove(a1)
				ps.remove(a2)
				
				a1.type = B
				a2.type = C
	
	
	def _collide_bc(self, grid, step):
		"""Check for and apply collision effects of three B particles colliding."""
		for (x, y), ps in grid.items():
			b_particles = [p for p in ps if p.type == B]
			c_particles = [p for p in ps if p.type == C]
			
			b_iter = iter(reversed(b_particles))
			c_iter = iter(reversed(c_particles))
			
			for b, c in zip(b_iter, c_iter):
				ps.remove(b)
				ps.remove(c)
				
				b.type = A
				c.type = A
	
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
	n_particles = 100
	n_steps = 1000
	
	u = make_random_universe(w, h, n_particles, [A])
	
	# Run time forward
	print("{} non-A particles at t=0".format(
		sum(1 for p in u.particles if p.type != A)))
	for _ in range(n_steps):
		u.step()
	print("{} non-A particles at t={}".format(
		sum(1 for p in u.particles if p.type != A), n_steps-1))
	
	# Run time backward again
	for _ in range(n_steps):
		u.step(-1)
	print("{} non-A particles at t=0".format(
		sum(1 for p in u.particles if p.type != A)))
