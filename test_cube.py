from cube_state import Cube, random_scramble
for _ in range(30):
    c = Cube()
    c.apply(random_scramble())
    assert not c.is_solved()
    c.apply(c.solve())
    assert c.is_solved()
c = Cube(); c.apply("R U R' U'"); c.apply("U R U' R'"); c.apply("R"); c.apply("R'")
print("All tests passed")

import cube_state
cube_state.kociemba = None   # also test the fallback solver
for _ in range(30):
    c = Cube(); c.apply(random_scramble(25)); c.apply(c.solve()); assert c.is_solved()
print("Fallback solver OK")
