import numpy as np
import matplotlib.pyplot as plt
import distance as dt
from matplotlib.collections import LineCollection

class Tree:
    """This will be the tree builder"""

    def __init__(self, q_init = None, K = None, qdot = None, buffer = None,
                 goal = None, want_print = False):
        if type(q_init) == int:
            # Randomize
            pass
        if not q_init:
            # Randomize this, eventually
            q_init = [50, 50]
        if not K:
            K == 100
        if not qdot:
            qdot = 1
        if not buffer or buffer == 0:
            print("Buffer must be > 0. Setting to 0.1")
            buffer = 0.1

        # Each element in G will first include itself and then the point it came from
        self.G = [(q_init,None)]
        self.K = K
        self.num_dims = len(q_init)
        self.qdot = qdot
        self.buffer = buffer
        self.goal = goal
        self.path = None
        self.want_print = want_print

    def get_nearest(self, point):
        best_point = None

        # Check the distance of every point
        for i in range(len(self.G)):
            if type(self.G[i][0]) == bool or type(point) == bool:
                pass
            dist = dt.eu_dist(self.G[i][0], point)
            # Update best_point if a point is found closer than current one
            # Automatically accept the first point though
            if not best_point or dist < best_point[1]:
                best_point = [self.G[i][0], dist]
        return best_point

    def new_config(self, domain, qrand, qnear, dist):
        """Adds a new configuration to the tree going from qnear toward qrand"""

        # 1. Get direction
        # 2. Normalize
        # 3. Calculate how far to step in each dimension
        # 4. Step

        direction = [randx - nearx for randx, nearx in zip(qrand, qnear)]
        unit_vector = [dim/dist for dim in direction]
        steps = [dim * self.qdot for dim in unit_vector]
        qnew = [dim + step for dim, step in zip(qnear,steps)]

        # Check if qnew is a valid point in the domain
        if domain.in_domain(qnew) == False:
            qnew = False
        # Also check for obstacle collision
        elif len(domain.obstacles) > 0 and qnew != False:
            for obs in domain.obstacles:
                if obs.check_collision(qnew, qnear, self.buffer) == False:
                    qnew = False
                    break
            if qnew != False:
                self.G.append((qnew, qnear))
        else:
            self.G.append((qnew, qnear))

        if self.want_print:
            print("")
            print(f"rand{qrand}\nnear{qnear}\ndist {dist}")
            print("")
            print(f"dir{direction}\nuv{unit_vector}\nsteps{steps}\nqnew{qnew}")

        return qnew

    def run_rrt(self, domain):
        if not self.goal:
            while len(self.G) < self.K:
                self.random_step(domain)

        else:
            while self.G[-1][0] != self.goal:
                #self.show_tree(domain)
                # Check if there's a straight shot from the last point to the goal
                found_shot = True
                if len(domain.obstacles) > 0:
                    for obs in domain.obstacles:
                        if obs.check_collision(self.goal, self.G[-1][0], self.buffer) == False:
                            found_shot = False
                            break
                if found_shot:
                    self.G.append((self.goal, self.G[-1][0]))
                else:
                    # Random Step if no shot found
                    self.random_step(domain)
                    if len(self.G) > self.K:
                        print("Steps maxed out.")
                        break
        self.trace_path()

    def random_step(self, domain):
        # Get random point from the domain
        qrand = domain.rand_point()
        # Get nearest point in the tree
        (qnear, dist) = self.get_nearest(qrand)
        # Get new point
        qnew = self.new_config(domain, qrand, qnear, dist)
        # qnew will be false if this loop fails (obstacle, out of domain)



    def show_tree(self, domain):
        """Display the tree, but only if it's 2D"""
        if self.num_dims != 2 and self.num_dims !=3:
            print("Cannot yet display anything but 2D")
        elif self.num_dims == 2:
            ##### Begin_Citation [2] #####
            fig, ax = plt.subplots()
            ax.set(xlim=(domain.dims[0]), ylim = domain.dims[1])
            segs = []
            circles = []
            if domain.obstacles != []:
                for obs in domain.obstacles:
                    if obs.shape == "circle":
                        circles.append(plt.Circle(obs.center,obs.dims[0], color = "y"))
                if circles != []:
                    for circle in circles:
                        ax.add_patch(circle)
            for ((x1,y1), point2) in self.G:
                if point2 == None:
                    ax.scatter(x1, y1, color = "green")
                ##### Begin_Citation [3] #####
                elif point2 != None:
                    (x2, y2) = point2
                    segs.append([(x1, y1), (x2, y2)])
                    ax.scatter(x1, y1, color = "black")
            if self.goal != None:
                ax.scatter(self.goal[0],self.goal[1], color = "red")
            tree_lines = LineCollection(segs, colors = "red")
            ax.add_collection(tree_lines)
            # Plot the path if known
            if self.path != None:
                path_segs = []
                for i in range(len(self.path) - 1):
                    path_segs.append([(self.path[i]),(self.path[i+1])])
                path_lines = LineCollection(path_segs, color = "blue")
                ax.add_collection(path_lines)
            ##### End_Citation [3] #####
            ax.set_aspect("equal")
            plt.show()
            ##### End_Citation [2] #####

        elif self.num_dims == 3:
            ##### Begin_Citation [2] #####
            fig = plt.figure()
            ax = fig.add_subplot(projection="3d")
            ax.set(xlim=(domain.dims[0]), ylim = domain.dims[1], zlim = domain.dims[2])
            ax.set_aspect("equal")
            #ax.set_zlim(domain.dims[2])
            segs = []

            for i in range(len(self.G) - 1):
                ((x1,y1,z1), point2) = self.G[i+1]
                if i == 0:
                    ax.scatter(x1, y1, z1, color = "green")
                ##### Begin_Citation [3] #####
                else:
                    (x2, y2, z2) = point2
                    segs.append([(x1, y1, z1), (x2, y2, z2)])
                    ax.scatter(x1, y1, z1, color = "black")
            # Plot the path dots in if known
            if self.path != None:
                for (x, y, z) in self.path:
                    ax.scatter(x, y, z, color = "b")

            # Show start
            (x, y, z) = self.G[0][0]
            ax.scatter(x, y, z, color = "green")

            # Show goal
            if self.goal != None:
                (x, y, z) = self.G[-1][0]
                ax.scatter(x, y, z, color = "red")

            circles = []
            if domain.obstacles != []:
                for obs in domain.obstacles:
                    if obs.shape == "circle":
                        #circles.append(plt.Circle(obs.center,obs.dims[0], color = "b"))
                        ##### Begin_Citation [6] #####
                        u = np.linspace(0, 2 * np.pi, 100)
                        v = np.linspace(0, np.pi, 100)
                        x = obs.dims[0] * np.outer(np.cos(u), np.sin(v)) + obs.center[0]
                        y = obs.dims[0] * np.outer(np.sin(u), np.sin(v)) + obs.center[1]
                        z = obs.dims[0] * np.outer(np.ones(np.size(u)), np.cos(v)) + obs.center[2]
                        ##### End_Citation [6] #####
                        ax.plot_surface(x, y, z, color="y")

            # Show the path
            for seg in segs:
                (x1, y1, z1) = seg[0]
                (x2, y2, z2) = seg[1]
                ax.plot([x1, x2], [y1, y2], [z1, z2], color = "r")

            ##### End_Citation [3] #####

            plt.show()


    def trace_path(self):
        """When the tree hits the goal, run this to actually find the path
           It sets self.path to the path, but also returns the path. If no path,
           return None"""
        last_vector = self.G[-1]
        if last_vector[0] != self.goal:
            print("Tree did not hit goal")
            return None

        path = [list(last_vector[0])]
        at_start = False
        while not at_start:
            for vec in self.G:
                if vec[0] != None and vec[0] == last_vector[1]:
                    last_vector = vec
                    break
            path.append(last_vector[0])
            if path[-1] == self.G[0][0]:
                at_start = True
        self.path = path
        return path

    def optimize_path(self, domain):
        """The default implementation here finds a path, but does not optimize that path.
            optimize_path will attempt to remove unnecessary steps in the path to shorten it."""
        # Withe a tree with n steps, the step n is already a straight shot to the target,
            # We need to check the rest of the step end points starting with step n-1
        new_tree = self.path.copy()
        new_tree.reverse()
        last_tree = []

        reset = True
        while last_tree != new_tree:
            last_tree = new_tree.copy()
            start_of_tree = new_tree.copy()
            end_of_tree = [start_of_tree.pop()]
            end_of_tree.insert(0, start_of_tree.pop())
            reset = False
            while not reset:
                # check if the any two steps can connect with eachother, starting with
                # check 1 -> n-1, then 2->n-1, ..., then 1->n-2, 2->n-2, ...
                found_shot = True
                for i in range(len(start_of_tree)):
                    step = start_of_tree[i]
                    if len(domain.obstacles) > 0:
                        for obs in domain.obstacles:
                            if obs.check_collision(step, end_of_tree[0], self.buffer) == False:
                                found_shot = False
                                break
                    if found_shot == True:
                        new_tree = start_of_tree[0:i+1].copy()
                        new_tree.extend(end_of_tree)
                        reset = True
                        break
                # if we get through all steps without finding a shortcut, transfer one step from the start list to the end list
                if not reset and len(start_of_tree) > 0:
                    end_of_tree.insert(0, start_of_tree.pop())
        new_tree.reverse()
        self.path = new_tree

