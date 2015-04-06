#!/usr/bin/env python

"""A simulation of time..."""

from collections import defaultdict

import random


# Particle types
A = "A"
B = "B"


class Particle(object):
	"""A single particle."""
	def __init__(self, type=A, x=0.0, y=0.0, vx=0.0, vy=0.0, aux=None):
		self.type = type
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		self.aux = aux


class Universe(object):
	"""A model of the universe where there are two fundamental particle types.
	
	Particles of type A aniahlate upon collision producing three particles of type
	B. The first two Bs have same velocities of the two A particles while the
	third's velocity is composed of the aux values of the two A particles.
	
	If three B particles collide, two type A particles are produced, taking the
	same velocities as the first two Bs and aux values from the velocity
	components of the third B vector.
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
				b3 = Particle(B, a1.x, a1.y, a1.aux, a2.aux, None)
				a1.aux = None
				a2.aux = None
				
				if step > 0:
					# After last
					self.particles.insert(self.particles.index(a2) + 1, b3)
				else:
					# Before first (note order is reversed so a2 is first)
					self.particles.insert(self.particles.index(a2), b3)
	
	
	def _collide_bbb(self, grid, step):
		"""Check for and apply collision effects of three B particles colliding."""
		for (x, y), ps in grid.items():
			b_particles = [p for p in ps if p.type == B]
			
			if step > 0:
				b_iter = iter(b_particles)
			else:
				b_iter = iter(reversed(b_particles))
			
			for b3, b2, b1 in zip(b_iter, b_iter, b_iter):
				ps.remove(b1)
				ps.remove(b2)
				ps.remove(b3)
				
				b1.type = A
				b2.type = A
				
				b1.aux = b3.vx
				b2.aux = b3.vy
				
				self.particles.remove(b3)
	
	def __str__(self):
		return ", ".join("{}({}, {})".format(p.type, p.x, p.y) for p in u.particles)


def make_random_universe(width, height, n_particles, types):
	"""Create a random universe with an equal distribution of the supplied set of
	particle types.
	"""
	u = Universe(width, height)
	for n in range(n_particles):
		type = random.choice(types)
		u.particles.append(Particle(type=type,
		                            x=random.randint(0, width-1),
		                            y=random.randint(0, height-1),
		                            vx=random.randint(0, width-1),
		                            vy=random.randint(0, height-1),
		                            aux=random.randint(0, min(width, height)-1)
		                                if type == A else None))
	return u


if __name__=="__main__":
	# XXX
	def dump_state(u):
		return [(p.type, p.x, p.y, p.vx, p.vy, p.aux) for p in u.particles]
	
	random.seed(0)
	
	w, h = 2, 1
	n_particles = 4
	n_steps = 100
	
	dumps_fwd = []
	dumps_bwd = []
	
	u = make_random_universe(w, h, n_particles, [A])
	
	# Run time forward
	print("{} non-A particles at t=0".format(
		sum(1 for p in u.particles if p.type != A)))
	for _ in range(n_steps):
		dumps_fwd.append(dump_state(u))
		u.step()
	dumps_fwd.append(dump_state(u))
	print("{} non-A particles at t={}".format(
		sum(1 for p in u.particles if p.type != A), n_steps-1))
	
	# Run time backward again
	for _ in range(n_steps):
		dumps_bwd.append(dump_state(u))
		u.step(-1)
	dumps_bwd.append(dump_state(u))
	print("{} non-A particles at t=0".format(
		sum(1 for p in u.particles if p.type != A)))
	
	
	for n, (fwd, bwd) in enumerate(zip(reversed(dumps_fwd), dumps_bwd)):
		print("{}\n  fwd={}\n  bwd={}".format(n_steps - n - 1, fwd, bwd))
		if fwd != bwd:
			print("Different!")
			break
