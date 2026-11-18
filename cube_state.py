"""Logical 3x3 cube. Every sticker = [cubie_position, normal, color].
Moves rotate stickers in 3D, so the 3D view and the solver always agree."""
import random
try:
    import kociemba            # optional: optimal-ish solver (needs a C compiler on Windows)
except ImportError:
    kociemba = None

FACES = {'U': (0, 1, 0), 'R': (1, 0, 0), 'F': (0, 0, 1),
         'D': (0, -1, 0), 'L': (-1, 0, 0), 'B': (0, 0, -1)}
ORDER = 'URFDLB'  # kociemba facelet order


def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def rot(v, axis, k):
    """Rotate v by 90 degrees about axis. k=+1 right-hand, k=-1 clockwise (seen from axis tip)."""
    d, c = dot(axis, v), cross(axis, v)
    return tuple(axis[i] * d + k * c[i] for i in range(3))


def _cell(face, r, c):
    a, b = c - 1, r - 1
    return {'U': (a, 1, b), 'R': (1, -b, -a), 'F': (a, -b, 1),
            'D': (a, -1, -b), 'L': (-1, -b, a), 'B': (-a, -b, -1)}[face]


class Cube:
    def __init__(self):
        self.reset()

    def reset(self):
        self.history = []
        self.stickers = []
        for f in ORDER:
            for r in range(3):
                for c in range(3):
                    self.stickers.append([_cell(f, r, c), FACES[f], f])

    def move(self, m):
        self.history.append(m)
        face, axis = m[0], FACES[m[0]]
        k = 1 if "'" in m else -1
        for _ in range(2 if '2' in m else 1):
            for s in self.stickers:
                if dot(s[0], axis) == 1:
                    s[0], s[1] = rot(s[0], axis, k), rot(s[1], axis, k)

    def apply(self, moves):
        for m in (moves.split() if isinstance(moves, str) else moves):
            self.move(m)

    def facelets(self):
        d = {(s[0], s[1]): s[2] for s in self.stickers}
        return ''.join(d[(_cell(f, r, c), FACES[f])]
                       for f in ORDER for r in range(3) for c in range(3))

    def is_solved(self):
        return self.facelets() == ''.join(f * 9 for f in ORDER)

    def solve(self):
        if kociemba:
            return kociemba.solve(self.facelets()).split()
        return self._undo_history()

    def _undo_history(self):
        """Fallback solver: reverse every move made since the solved state."""
        inv = {'': "'", "'": '', '2': '2'}
        out = []
        for m in reversed(self.history):
            m = m[0] + inv[m[1:]]
            if out and out[-1][0] == m[0]:          # merge R R -> R2, R R' -> nothing
                t = lambda x: {'': 1, '2': 2, "'": 3}[x[1:]]
                n = (t(out.pop()) + t(m)) % 4
                if n: out.append(m[0] + {1: '', 2: '2', 3: "'"}[n])
            else:
                out.append(m)
        return out


def random_scramble(n=20):
    out, last = [], ''
    for _ in range(n):
        f = random.choice([x for x in 'URFDLB' if x != last])
        last = f
        out.append(f + random.choice(['', "'", '2']))
    return out
