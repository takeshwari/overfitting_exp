from legexp import LengedreExperiment
import numpy as np
import timeit
import time
import sys
import json
from multiprocessing import Process, Queue, Pool

if len(sys.argv)!=2:
	exit("Error: Missing arguments")

file = sys.argv[1]

# def runexps(qf, variance, n, rounds):
# 	eouth2sum = np.float64(0.0)
# 	eouth10sum = np.float64(0.0)
# 	eouth2sum2 = np.float64(0.0)
# 	eouth10sum2 = np.float64(0.0)
# 	eouth2sum3 = np.float64(0.0)
# 	eouth10sum3 = np.float64(0.0)

# 	for i in xrange(rounds):
# 		exp = LengedreExperiment(qf, variance, n)
# 		#exp.printstats()
# 		eouth2sum += exp.eoutg2[0]
# 		eouth10sum += exp.eoutg10[0]
# 		eouth2sum2 += exp.eoutg2[1]
# 		eouth10sum2 += exp.eoutg10[1]
# 		eouth2sum3 += exp.eoutg2[2]
# 		eouth10sum3 += exp.eoutg10[2]
	
# 	print("Eout(H2):  %f"%((eouth2sum/rounds)))
# 	print("Eout2(H2):  %f"%((eouth2sum2/rounds)))
# 	print("Eout3(H2):  %f"%((eouth2sum3/rounds)))
# 	print("Eout(H10): %f"%((eouth10sum/rounds)))
# 	print("Eout2(H10): %f"%((eouth10sum2/rounds)))
# 	print("Eout3(H10): %f"%((eouth10sum3/rounds)))

def runexps(rounds, qf, variance, n):
	start_time = time.time()
	eouth2sum = np.float64(0.0)
	eouth10sum = np.float64(0.0)

	for i in xrange(rounds):
		exp = LengedreExperiment(qf, variance, n)
		if n == 9 and variance == 0.0:
			exp.plot()
			exp.printstats()
		eouth2sum += exp.eoutg2
		eouth10sum += exp.eoutg10

	end_time = time.time()

	return {
			'qf': qf,
			'variance': variance,
			'n': n,
			'rounds': rounds,
			'eouth2': (eouth2sum/rounds),
			'eouth10': (eouth10sum/rounds),
			'start_time': start_time,
			'end_time': end_time
			}

def worker(scenario):
			return runexps(1, *scenario)

def stochastic_noise(num_worker_threads, file):
	qf= 20
	scenarios = []
	for n in xrange(1,10):
		for variance  in np.linspace(0.0, 2.5, num=2):
			scenarios.append((qf, variance, n))



	p = Pool(num_worker_threads)
	with open(file, 'a', 0) as f:
		for obj in p.imap_unordered(worker, scenarios):
			print(obj['eouth10'] - obj['eouth2'])
			f.write(json.dumps(obj)+"\n")

# def stochastic_noise2():
# 	qf= 20
# 	for n in xrange(1,10):
# 		for variance  in np.linspace(0.0, 2.5, num=2):
# 			print runexps(100, qf, variance, n)


# st2 = time.time()
# stochastic_noise2()
# et2 = time.time()
# print("Runtime 1 cores: %f"%(et2-st2))

st4 = time.time()
stochastic_noise(4,file)
et4 = time.time()
print("Runtime 4 cores: %f"%(et4-st4))  
# def worker():
#     while True:
#         item = q.get()
#         do_work(item)
#         q.task_done()

# q = Queue()
# for i in range(num_worker_threads):
#      t = Thread(target=worker)
#      t.daemon = True
#      t.start()

# for item in source():
#     q.put(item)

# q.join()   
# exps = runexps(100,0.1,120,100)
# print(exps)
# print("Elapsed time:%f"%(exps['end_time'] -exps['start_time']))
# def run():
# 	return runexps(100,0.1,120,10)

# exp = LengedreExperiment(100,0.1,120)

# def test1():
# 	exp.mse(exp.g10, exp.leg)

# def test2():
# 	exp.mse2(exp.g10, exp.leg,1000)

# def test3():
# 	exp.mse3(exp.g10, exp.leg)

# #print(timeit.timeit(run,number=1))
# number = 10
# print(timeit.timeit(test1,number=number))
# print(timeit.timeit(test2,number=number))
# print(timeit.timeit(test3,number=number))

