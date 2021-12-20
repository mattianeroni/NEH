import numpy as np
import math
import random

import utils

def _bra (lst, beta = 0.3):
    """
    This method carry out a biased randomised selection on a set of items.
    The randomisation is made using a quasi-geometric distribution

                        f(x) = (1 - beta)^x

    where the beta parameter ranges between 0 and 1.

    :param beta: The parameter of the quasi-geometric distribution.
    :param lst: The set of options from which it is possible
                to select.
    """
    L, options = len(lst), list(lst)
    for _ in range(L):
        idx = int(math.log(random.random(), 1 - beta)) % len(options)
        yield options.pop(idx)


class Solver (object):
    """
    An instance of this class represents the algorithm proposed.
    """

    def __init__(self, problem):
        """
        Initialise.

        :param problem: The problem to solve.
        """
        self.problem = problem

    def NEH (self):
        """
        This method implements the Nawaz, Enscore and Ham algorithm
        with the Taillard acceleration described in

        Taillard, E. (1990). Some efficient heuristic methods for the flow shop
        sequencing problem. European Journal of Operational Research, 47(1), 65-74.

        :return: The sequence in which jobs should be processed and the respective
                makespan.
        """
        # Take useful variables to the stack
        times = self.problem.processing_times
        n_jobs = self.problem.n_jobs
        n_machines = self.problem.n_machines
        # Initialise the solution and the respective makespan
        sequence, makespan = [], 0
        # Sort jobs for decreasing processing time on machines.
        jobs = sorted(list(range(0, n_jobs)), key=lambda i: times[i, :].sum(), reverse=True)
        # Find the best schedule with the first two jobs in an exaustive way.
        # M1 = Makespan when first job in list is made first.
        # M2 = Makespan when second job in list is made first.
        # end1 = End of first job on current machine when first job is made first
        # end2 = End of second job on current machine when second job is made first
        first_job, second_job = tuple(jobs[:2])
        M1, end1 = 0, 0
        M2, end2 = 0, 0
        for j in range(n_machines):
            end1 += times[first_job, j]
            M1 = max(end1, M1) + times[second_job, j]
            end2 += times[second_job, j]
            M2 = max(end2, M2) + times[first_job, j]
        # First two jobs are scheduled ensuring the minor makespan possible
        sequence = [second_job, first_job] if M1 > M2 else [first_job, second_job]
        # For each other job...
        for k, job in zip(range(2, n_jobs), jobs[2:]):
            # Init earliest completion time of i-th job on j-th machine
            e = np.zeros((k+1, n_machines+1))
            # Init the tail of the i-th job on the j-th machine
            q = np.zeros((k+1, n_machines+1))
            # Init the earlie1st relative completion time for the k-th job
            # in i-th position on j-th machine.
            f = np.zeros((k+1, n_machines+1))
            # Initialise the partial minimum makespan after inserting
            # the k-th job in the i-th position
            Mmin, position = float("inf"), None
            # For each position in which the job can be inserted...
            for i in range(k):
                # Compute the earliest completion time, the tail, and the
                # relative completion time
                for j in range(n_machines):
                    e[i, j] = max(e[i, j-1], e[i-1, j]) + times[sequence[i], j]
                    q[k-i-1, n_machines-j-1] = max(q[k-i-1, n_machines-j], q[k-i, n_machines-j-1]) + times[sequence[k-i-1], n_machines-j-1]
                    #q[k-i, n_machines-j] = max(q[k-i, n_machines-j+1], q[k-i+1, n_machines-j]) + times[sequence[k-i-1], n_machines-j]
                    f[i, j] = max(f[i, j-1], e[i-1, j]) + times[job, j]

            # Partial makespans inserting job in i-th position
            Mi = np.amax(f + q, axis=1)[:-1]
            # Find the position where to insert k-th job that minimise the makespan
            position = np.where(Mi == Mi.min())[0][0]
            makespan = Mi[position]
            # Insert the k-th job in the position that minimised the partial makespan
            sequence.insert(position, job)

        # Return the sequence and the makespan
        print(jobs)
        print(sequence, makespan)
        return sequence, makespan
