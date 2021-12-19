import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
import random
import itertools


class Problem (object):
    """
    An instance of this class represents a problem to solve.
    """
    def __init__(self, n_jobs, n_machines, seed, upperbound, lowerbound, processing_times):
        """
        Initialise.

        :param n_jobs: The number of jobs
        :param n_machines: The number of machines
        :param seed: The seed of the problem generation
        :param upperbound: The worst solution ever in terms of makespan
        :param lowerbound: The best solution ever in terms of makespan
        :param processing_times: The matrix of processing times (n_jobs x n_machines)
        """
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


def searchfile (jobs, machines, path = "../tests/"):
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


def readfile (filename, path = "../tests/"):
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
            if reading_proc_times and counter < n_machines:
                # Save the processing times for a new machine
                proc_times.append(list(map(int, line.split())))
                counter += 1

            if reading_proc_times and counter == n_machines:
                reading_proc_times = False
                probs.append(Problem(n_jobs, n_machines, seed, upper, lower, processing_times=np.asarray(proc_times).T))
                proc_times = []

    return tuple(probs)



def makespan (sequence, times):
    """
    This method is an unoptimised way to compute the total
    makespan given a certain sequence in which jobs are
    processed.

    :param sequence: The jobs in the sequence in which are
                    processed .
    :param times: The matrix of processing times (i.e., time[i, j] is the
                processing time of job i on machine j).
    :return: The makespan.
    """
    n_jobs, n_machines = times.shape
    M = 0
    # Init the list containing the instant of time in which
    # each job has been concluded by the previous machine.
    # NOTE: Last element of this array should always be zero,
    # because it represents the end time of the first job.
    end_times = [0] * (n_jobs + 1)
    # For each machine plot the schedule of jobs...
    for j in range(n_machines):
        # iterate the jobs made on this machine...
        for k, job in enumerate(sequence):
            endtime = max(end_times[k - 1], end_times[k]) + times[job, j]
            end_times[k] = endtime
            M = max(M, endtime)
    return M


def exhaustive (jobs, times):
    """
    This method is an exhaustive approach to the flow
    shop scheduling problem.

    :param jobs: The set of jobs to sequence.
    :param times: The processing times (i.e., time[i, j] is the
                processing time of job i on machine j).
    :return: The best solution and its makespan.
    """
    best, M = list(jobs), float("inf")
    for sol in itertools.permutations(jobs):
        if (cost := makespan(sol, times)) < M:
            best, M = sol, cost
    return best, M


def plot_schedule (sequence, times, figsize=(8,6), save=None):
    """
    This method takes care of printing a certain jobs schedule.

    :param sequence: The jobs in the order in which they are processed.
    :param times: The matrix of processing times (i.e., time[i, j] is the
                processing time of job i on machine j).
    :param figsize: The size of the plotted figure.
    :param save: The file where the figure is going to be saved. If None
                the figure is simply plotted at screen.
    """
    n_jobs, n_machines = times.shape
    # Initialise the plot characteristics
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlabel('Time')
    ax.set_ylabel('Machines')
    ax.set_yticks([i + 0.5 for i in range(n_machines)])
    ax.set_yticklabels(range(n_machines))
    ax.grid(True)
    # Initialise the color assigned to each job
    colors = random.sample(list(mcolors.CSS4_COLORS.values()), n_jobs)
    # Init the list containing the instant of time in which
    # each job has been concluded by the previous machine
    end_times = [0] * n_jobs
    # For each machine plot the schedule of jobs...
    for j in range(n_machines):
        jobs_bars = []
        # iterate the jobs made on this machine...
        for k, job in enumerate(sequence):
            # Get the processing time
            duration = times[job, j]
            # Get the starting time looking at the ending time
            # on the previous machine, and the time in which this
            # machine finished the previous job.
            end_of_previous_job = 0 if k == 0 else end_times[k - 1]
            start = max(end_of_previous_job, end_times[k])
            # Calculate and save the ending time of this job on
            # this machine
            end_times[k] = start + duration
            # Update the list of jobs bars
            jobs_bars.append((start, duration))
        # Draw the bars relative to this machine
        ax.broken_barh(jobs_bars, (j, 1), facecolors=colors)
        # Add the colors legend
        ax.legend([Patch(facecolor=c, edgecolor=c) for c in colors], sequence, loc='lower right')
        # Draw the ids of jobs on relative bars
        #for jobid, (start, duration) in zip(sequence, jobs_bars):
        #    ax.text(start + duration / 2, j + 0.5, jobid, ha="center", va="center")
    # Save and plot the schedule
    if save is not None:
        plt.savefig(save)
    plt.show()


if __name__ == "__main__":
    """
    Use example.

    """
    probs = readfile("t_j20_m5.txt")
    for p in probs:
        print(p)
