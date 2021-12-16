import numpy as np
import math
import random


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
        """
        # Take useful variables to the stack
        t = self.problem.processing_times
        n = self.problem.n_jobs
        m = self.problem.n_machines
        # Initialise the solution
        sequence = [0] * n
        # Sort jobs for decreasing processing time on machines.
        jobs = sorted(list(range(0, self.problem.n_jobs)), key=lambda i: t[i, :].sum(), reverse=True)
        # Find the best schedule with the first two jobs.
        M1, M2 = 0, 0
        for j in range(m):
            ...




    '''
    def NEH(self):
        """
        1) First, we create a list with our jobs. We sort it depending of the time that each job spend until it finishes.
        2) We reorganize this list using BR.
        3) We use NEH to complete our solution
        4) We return our makespan
        """
        #1
        lista = [(i, i.total_time, j) for j,i in enumerate(self.jobs)]
        lista.sort(reverse=True, key= lambda x: x[1])

        #2
        lista = self.reorganize_list(lista)

        #3
        self.solution.append(lista.pop(0)[0])
        for _ in range(len(lista)):
            self.insert(lista)

        #4
        return [i.time for i in self.machines][-1]

    def insert(self, lista):
        data = self.seleccionar(lista)[0]
        best = []
        for i in range(len(self.solution) + 1):
            #aux_solution = copy.deepcopy(self.solution)
            aux_solution = self.copy_solution()
            #aux_machines = copy.deepcopy(self.machines)
            aux_machines = [machine(i) for i in range(len(self.machines))]
            aux_solution = aux_solution[:i] + [data] + aux_solution[i:]

            for j in aux_solution:
                for k in aux_machines:
                    if k.id == 0:
                        k.time += j.time_machines[k.id]
                    elif aux_machines[k.id - 1].time <= k.time:
                        k.time += j.time_machines[k.id]
                    else:
                        k.time = aux_machines[k.id - 1].time + j.time_machines[k.id]

            best.append((aux_machines[-1].time, aux_machines, aux_solution))

        best.sort(key=operator.itemgetter(0))   # best.sort(key=lambda x: x[0])
        self.solution = best[0][2]
        self.machines = best[0][1]

    def multistart_NEH(self):
        start_time = time.time()
        best = -1
        best_planning = ()
        while self.max_time > time.time() - start_time:
            makespan = self.NEH()
            if best == -1 or best > makespan:
                #best_planning = (copy.deepcopy(self.solution), copy.deepcopy(self.machines), makespan)
                best_planning = (self.copy_solution(), copy.deepcopy(self.machines), makespan)
                best = makespan
            self.solution = []
            self.machines = [machine(i) for i in range(len(self.machines))]

        self.solution = best_planning[0]
        makespan_bb = self.bb_makespan()
        self.show(best_planning)
        print("Makespan for our black box is: ", makespan_bb)


    def bb_makespan(self, save = False):
        #aux_solution = copy.deepcopy(self.solution)
        aux_solution = self.copy_solution()
        if save:
            data_base = open("data_base.txt","a")
            if os.stat("data_base.txt").st_size == 0:
                data_base.write("h" + " Machine_processed_jobs" + " time_of_job_in_machine" + " time_black_box" + " job_class"  + " machine_time" + " job_id" + " machine_id" + "\n")
        aux_machines = [machine(i) for i in range(len(self.machines))]
        n = len(self.jobs)
        for j in aux_solution:
            for k in aux_machines:
                if k.processed_jobs == 10:
                    print()
                time_black_box = j.black_box(self.h, k, n)


                if k.id == 0:
                    k.time += time_black_box
                elif aux_machines[k.id - 1].time <= k.time:
                    k.time += time_black_box
                else:
                    k.time = aux_machines[k.id - 1].time + time_black_box

                if save:
                    data_base.write(str(self.h) + " " + str(k.processed_jobs/len(self.jobs)) + " " + str(j.time_machines[k.id])  + " "  + str(time_black_box) + " " + str(j.job_class)  + " " + str(k.time) + " " + str(j.id) + " " + str(k.id) + "\n")
                k.processed_jobs += 1
        if save:
            data_base.close()

        return aux_machines[-1].time

    def build_dataset(self, n_solutions):
        """
        We build "n_solutions" solutions and we introduce the data that we obtained in our data_base.txt.
        We will use it for doing our learnheuristic.
        :param n_solutions: Number of solutions that we want in our data base
        """
        self.beta = 0.01
        #copy_machines = copy.deepcopy(self.machines)
        copy_machines = [machine(i) for i in range(len(self.machines))]
        for _ in range(n_solutions):
            self.NEH()
            self.bb_makespan(save=True)
            self.solution = []
            self.machines = copy_machines
    '''
