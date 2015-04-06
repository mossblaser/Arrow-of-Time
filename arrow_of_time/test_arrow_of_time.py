"""Py.test suite for Arrow-of-Time."""

import pytest

from arrow_of_time import A, B, Particle, Universe


def dump_state(u):
	return [(p.type, p.x, p.y, p.vx, p.vy, p.aux) for p in u.particles]


def test_velocity():
	u = Universe(10, 10)
	u.particles.append(Particle(A, 0, 0, 1, 2))
	
	u.step()
	assert len(u.particles) == 1
	assert u.particles[0].x == 1
	assert u.particles[0].y == 2
	
	u.step(1)
	assert len(u.particles) == 1
	assert u.particles[0].x == 2
	assert u.particles[0].y == 4
	
	u.step(-1)
	assert len(u.particles) == 1
	assert u.particles[0].x == 1
	assert u.particles[0].y == 2


def test_wrap():
	u = Universe(3, 4)
	u.particles.append(Particle(A, 0, 0, 1, 3))
	
	u.step()
	assert len(u.particles) == 1
	assert u.particles[0].x == 1
	assert u.particles[0].y == 3
	
	u.step()
	assert len(u.particles) == 1
	assert u.particles[0].x == 2
	assert u.particles[0].y == 2
	
	u.step()
	assert len(u.particles) == 1
	assert u.particles[0].x == 0
	assert u.particles[0].y == 1


def test_collide_aa():
	u = Universe(10, 10)
	u.particles.append(Particle(A, 0, 0, 1, 0, 2))
	u.particles.append(Particle(A, 2, 0, -1, 0, 3))
	
	before = dump_state(u)
	
	# Check collision occurs correctly
	u.step()
	assert len(u.particles) == 3
	assert u.particles[0].type == B
	assert u.particles[0].x == 1
	assert u.particles[0].y == 0
	assert u.particles[0].vx == 1
	assert u.particles[0].vy == 0
	assert u.particles[0].aux == None
	
	assert u.particles[1].type == B
	assert u.particles[1].x == 1
	assert u.particles[1].y == 0
	assert u.particles[1].vx == -1
	assert u.particles[1].vy == 0
	assert u.particles[1].aux == None
	
	assert u.particles[2].type == B
	assert u.particles[2].x == 1
	assert u.particles[2].y == 0
	assert u.particles[2].vx == 2
	assert u.particles[2].vy == 3
	assert u.particles[2].aux == None
	
	u.step(-1)
	assert before == dump_state(u)


def test_collide_aaa():
	u = Universe(10, 10)
	u.particles.append(Particle(A, 0, 0, 1, 0, 2))
	u.particles.append(Particle(A, 2, 0, -1, 0, 3))
	u.particles.append(Particle(A, 1, 1, 0, -1, 4))
	
	before = dump_state(u)
	
	# Check collision occurs correctly and that third particle remains an A
	u.step()
	assert len(u.particles) == 4
	assert u.particles[0].type == B
	assert u.particles[0].x == 1
	assert u.particles[0].y == 0
	assert u.particles[0].vx == 1
	assert u.particles[0].vy == 0
	assert u.particles[0].aux == None
	
	assert u.particles[1].type == B
	assert u.particles[1].x == 1
	assert u.particles[1].y == 0
	assert u.particles[1].vx == -1
	assert u.particles[1].vy == 0
	assert u.particles[1].aux == None
	
	assert u.particles[2].type == B
	assert u.particles[2].x == 1
	assert u.particles[2].y == 0
	assert u.particles[2].vx == 2
	assert u.particles[2].vy == 3
	assert u.particles[2].aux == None
	
	assert u.particles[3].type == A
	assert u.particles[3].x == 1
	assert u.particles[3].y == 0
	assert u.particles[3].vx == 0
	assert u.particles[3].vy == -1
	assert u.particles[3].aux == 4
	
	u.step(-1)
	assert before == dump_state(u)


def test_collide_aaaa():
	u = Universe(10, 10)
	u.particles.append(Particle(A, 0, 0, 1, 0, 2))
	u.particles.append(Particle(A, 2, 0, -1, 0, 3))
	u.particles.append(Particle(A, 1, 1, 0, -1, 4))
	u.particles.append(Particle(A, 1, 9, 0, 1, 5))
	
	before = dump_state(u)
	
	# Check collision occurs correctly and that third particle remains an A
	u.step()
	assert len(u.particles) == 6
	assert u.particles[0].type == B
	assert u.particles[0].x == 1
	assert u.particles[0].y == 0
	assert u.particles[0].vx == 1
	assert u.particles[0].vy == 0
	assert u.particles[0].aux == None
	
	assert u.particles[1].type == B
	assert u.particles[1].x == 1
	assert u.particles[1].y == 0
	assert u.particles[1].vx == -1
	assert u.particles[1].vy == 0
	assert u.particles[1].aux == None
	
	assert u.particles[2].type == B
	assert u.particles[2].x == 1
	assert u.particles[2].y == 0
	assert u.particles[2].vx == 2
	assert u.particles[2].vy == 3
	assert u.particles[2].aux == None
	
	assert u.particles[3].type == B
	assert u.particles[3].x == 1
	assert u.particles[3].y == 0
	assert u.particles[3].vx == 0
	assert u.particles[3].vy == -1
	assert u.particles[3].aux == None
	
	assert u.particles[4].type == B
	assert u.particles[4].x == 1
	assert u.particles[4].y == 0
	assert u.particles[4].vx == 0
	assert u.particles[4].vy == 1
	assert u.particles[4].aux == None
	
	assert u.particles[5].type == B
	assert u.particles[5].x == 1
	assert u.particles[5].y == 0
	assert u.particles[5].vx == 4
	assert u.particles[5].vy == 5
	assert u.particles[5].aux == None
	
	
	u.step(-1)
	assert before == dump_state(u)


def test_collide_bc():
	u = Universe(10, 10)
	u.particles.append(Particle(B, 0, 0, 1, 0))
	u.particles.append(Particle(B, 2, 0, -1, 0))
	u.particles.append(Particle(B, 3, 1, -2, -1))
	
	before = dump_state(u)
	
	# Check collision occurs correctly
	u.step()
	assert len(u.particles) == 2
	assert u.particles[0].type == A
	assert u.particles[0].x == 1
	assert u.particles[0].y == 0
	assert u.particles[0].vx == 1
	assert u.particles[0].vy == 0
	assert u.particles[0].aux == -2
	
	assert u.particles[1].type == A
	assert u.particles[1].x == 1
	assert u.particles[1].y == 0
	assert u.particles[1].vx == -1
	assert u.particles[1].vy == 0
	assert u.particles[1].aux == -1
	
	u.step(-1)
	assert before == dump_state(u)


def test_xxx():
	u = Universe(2, 1)
	u.particles.append(Particle(A, 0, 0, 1, 0, 0))
	u.particles.append(Particle(A, 0, 0, 0, 0, 0))
	u.particles.append(Particle(B, 1, 0, 0, 0, None))
	u.particles.append(Particle(B, 1, 0, 0, 0, None))
	u.particles.append(Particle(B, 1, 0, 0, 0, None))
	
	before = dump_state(u)
	
	print(dump_state(u))
	u.step()
	print(dump_state(u))
	u.step(-1)
	print(dump_state(u))
	
	assert before == dump_state(u)
