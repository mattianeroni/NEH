import numpy as np
import machine, job, sol


class Problem (object):
    """
    An instance of this class represents a problem to solve.
    """
    def __init__(self, n_jobs, n_machines, seed, upperbound, lowerbound, processing_times):
        self.n_jobs = n_jobs
        self.n_machines = n_machines
        self.seed = seed
        self.upperbound = upperbound
        self.lowerbound = lowerbound
        self.processing_times = processing_times

    def __repr__(self):
        return f"""
        ----------------------------------------------------------
        Jobs : {self.n_jobs},
        Machines : {self.n_machines},
        Seed : {self.seed},
        Upperbound : {self.upperbound},
        Lowerbound : {self.lowerbound},
        ProcessingTimes:
        {self.processing_times}
        ----------------------------------------------------------
        """


def searchfile (jobs, machines, path = "./tests/"):
    """
    Given a number of jobs and a number of machines that define
    the complexity of a problem, this method looks for the file
    with the correct benchmarks.

    If the exactly specified number of jobs and machine is not found,
    an exception is raised.

    """
    try:
        filename = f"t_j{jobs}_m{machines}.txt"
        f = open(path + filename)
        f.close()
        return filename
    except:
        raise Exception("Bechmarks with required caracteristics not found.")


def readfile (filename, path = "./test/"):
    """
    This method reads a file containing some Taillard's benchmarks
    and returns a set of standardized Problem instances (see class above).

    """
    # Init problem variables
    n_jobs, n_machines, seed, upper, lower = 0, 0, 0, 0, 0
    proc_times = []
    reading_general_info, reading_proc_times, counter = False, False, 0

    # Init standard headers reported in bechmark files
    signal_new_problem = "number of jobs, number of machines, initial seed, upper bound and lower bound :".strip()
    signal_proc_times = "processing times :".strip()

    # Init problems list
    probs = list()

    with open(f"{path}{filename}", 'r') as file:
        for line in file:
            cline = line.strip()

            # If next line contains general info of a new problem
            if cline == signal_new_problem:
                reading_general_info = True
                continue

            if reading_general_info:
                n_jobs, n_machines, seed, upper, lower = tuple(map(int, line.split()))
                reading_general_info = False
                continue

            # If starting from the next line, the machines processing times
            # are reported...
            if cline == signal_proc_times:
                reading_proc_times, counter = True, 0
                continue

            # If still reading the machines processing times...
            if reading_proc_times and counter < machines:
                # Save the processing times for a new machine
                proc_times.append(list(map(int, line.split())))
                counter += 1

            if reading_proc_times and counter == machines:
                reading_proc_times = False
                probs.append(Problem(n_jobs, n_machines, seed, upper, lower, processing_times=np.asarray(proc_times)))
                proc_times = []

    return tuple(probs)




if __name__ == "__main__":
    """
    Use example.

    """
    probs = readfile("t_j20_m5.txt")
    for p in probs:
        print(p)
