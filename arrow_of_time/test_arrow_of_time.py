"""Py.test suite for Arrow-of-Time."""

import pytest

from arrow_of_time import A, B, C, Particle, Universe


def dump_state(u):
	return [(p.type, p.x, p.y, p.vx, p.vy) for p in u.particles]


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
	u.particles.append(Particle(A, 0, 0, 1, 0))
	u.particles.append(Particle(A, 2, 0, -1, 0))
	
	before = dump_state(u)
	
	# Check collision occurs correctly
	u.step()
	assert len(u.particles) == 2
	assert u.particles[0].type == B
	assert u.particles[0].x == 1
	assert u.particles[0].y == 0
	assert u.particles[0].vx == 1
	assert u.particles[0].vy == 0
	
	assert u.particles[1].type == C
	assert u.particles[1].x == 1
	assert u.particles[1].y == 0
	assert u.particles[1].vx == -1
	assert u.particles[1].vy == 0
	
	u.step(-1)
	assert before == dump_state(u)


def test_collide_aaa():
	u = Universe(10, 10)
	u.particles.append(Particle(A, 0, 0, 1, 0))
	u.particles.append(Particle(A, 2, 0, -1, 0))
	u.particles.append(Particle(A, 1, 1, 0, -1))
	
	before = dump_state(u)
	
	# Check collision occurs correctly and that third particle remains an A
	u.step()
	assert len(u.particles) == 3
	assert u.particles[0].type == B
	assert u.particles[0].x == 1
	assert u.particles[0].y == 0
	assert u.particles[0].vx == 1
	assert u.particles[0].vy == 0
	
	assert u.particles[1].type == C
	assert u.particles[1].x == 1
	assert u.particles[1].y == 0
	assert u.particles[1].vx == -1
	assert u.particles[1].vy == 0
	
	assert u.particles[2].type == A
	assert u.particles[2].x == 1
	assert u.particles[2].y == 0
	assert u.particles[2].vx == 0
	assert u.particles[2].vy == -1
	
	u.step(-1)
	assert before == dump_state(u)


def test_collide_aaaa():
	u = Universe(10, 10)
	u.particles.append(Particle(A, 0, 0, 1, 0))
	u.particles.append(Particle(A, 2, 0, -1, 0))
	u.particles.append(Particle(A, 1, 1, 0, -1))
	u.particles.append(Particle(A, 1, 9, 0, 1))
	
	before = dump_state(u)
	
	# Check collision occurs correctly and that third particle remains an A
	u.step()
	assert len(u.particles) == 4
	assert u.particles[0].type == B
	assert u.particles[0].x == 1
	assert u.particles[0].y == 0
	assert u.particles[0].vx == 1
	assert u.particles[0].vy == 0
	
	assert u.particles[1].type == C
	assert u.particles[1].x == 1
	assert u.particles[1].y == 0
	assert u.particles[1].vx == -1
	assert u.particles[1].vy == 0
	
	assert u.particles[2].type == B
	assert u.particles[2].x == 1
	assert u.particles[2].y == 0
	assert u.particles[2].vx == 0
	assert u.particles[2].vy == -1
	
	assert u.particles[3].type == C
	assert u.particles[3].x == 1
	assert u.particles[3].y == 0
	assert u.particles[3].vx == 0
	assert u.particles[3].vy == 1
	
	u.step(-1)
	assert before == dump_state(u)


@pytest.mark.parametrize("p1,p2", [(B, C), (C, B)])
def test_collide_bc(p1, p2):
	u = Universe(10, 10)
	u.particles.append(Particle(p1, 0, 0, 1, 0))
	u.particles.append(Particle(p2, 2, 0, -1, 0))
	
	before = dump_state(u)
	
	# Check collision occurs correctly
	u.step()
	assert len(u.particles) == 2
	assert u.particles[0].type == A
	assert u.particles[0].x == 1
	assert u.particles[0].y == 0
	assert u.particles[0].vx == 1
	assert u.particles[0].vy == 0
	
	assert u.particles[1].type == A
	assert u.particles[1].x == 1
	assert u.particles[1].y == 0
	assert u.particles[1].vx == -1
	assert u.particles[1].vy == 0
	
	print(before)
	print(dump_state(u))
	u.step(-1)
	print(dump_state(u))
	assert before == dump_state(u)
	
