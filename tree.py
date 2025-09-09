

class Tree:
    """This will be the tree builder"""

    def __init__(self, q_init = None, K = None):
        if not q_init:
            # Randomize
            pass
        if not K:
            K == 100

        self.G = [q_init]
        self.K = K

        