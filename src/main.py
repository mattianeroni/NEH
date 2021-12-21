import time
import utils
import solver



if __name__ == '__main__':
    problems = utils.readfile("t_j20_m5.txt")
    problem = problems[3]
    #sequence, makespan = utils.exhaustive(list(range(problem.n_jobs)), problem.processing_times)

    #times = problem.processing_times
    #print("0: ", times[0,:])
    #print("4: ", times[4,:])
    #print("6: ", times[6,:])

    algorithm = solver.Solver(problem)
    start = time.time()
    sequence, makespan = algorithm.NEH()
    print("Time: ", time.time() - start)
    print("Check: ", utils.makespan(sequence, problem.processing_times))
    #utils.plot_schedule(sequence, problem.processing_times)


    #print(problem)

    #machines = []
    #for i in range(17):
    #    machines.append(machine(i))

    #jobs = []
    #for i in range(15):
    #    jobs.append(job(i, machines, 0))

    #solution = sol(jobs, machines, beta=0.2, max_time=1, h = 0.25)
    #solution.multistart_NEH()
    #solution.build_dataset(10)
