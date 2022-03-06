import cProfile
import os
import re
import time

import amrlib
import random
import sys
import penman
import pstats



def summarize(file, option='-randomselect', summary_length=4):
    start = time.process_time()

    ## Read in the AMRs and put them into a LIST of PENMAN GRAPHS
    AMRs = penman.load(file)  ## List of Graph objects

    print('reading done')
    a = time.process_time() - start
    print('time taken to convert AMRs to graphs:', a, 'seconds')

    ## Option of selecting n random AMRs:

    if option == '-randomselect':
        if len(AMRs) > int(summary_length):
            summary_AMRs = random.choices(AMRs, k=int(summary_length))
        else:
            summary_AMRs = AMRs

        print('randomselect done')
        b = time.process_time() - start
        print('time taken to randomly select', summary_length, 'AMR graphs:', b, 'seconds')

    ## Option of using first n AMRs:

    if option == '-first':
        if len(AMRs) > int(summary_length):
            summary_AMRs = AMRs[:int(summary_length)]
        else:
            summary_AMRs = AMRs

        print('selection done')
        b = time.process_time() - start
        print('time taken to pick the first', summary_length, 'AMR graphs:', b, 'seconds')

    ## Write our summarized set of AMRs into an AMR file:
    penman.dump(summary_AMRs,'summary_amr.txt')

    print('writing done')
    b = time.process_time() - a
    print('time taken to write AMRS to output file:', b, 'seconds')








def main():
    summarize(sys.argv[1],sys.argv[2],sys.argv[3])

    '''
    Arguments:
        #1 - An input file full of AMRs in penman notation
        #2 - Option '-randomselect' or '-first'
        #3 - Any integer: number of AMRs that should be put in our summary
        #4 - Option '-n', '-ncalls' or '-cumtime': Prints profiler information sorted by times called or cumulative time taken. 
             Profiler does not run if left unspecified.
    '''

if __name__ == '__main__':
    if len(sys.argv) == 5:
        if sys.argv[4] == '-ncalls':
            profiler = cProfile.Profile()
            profiler.enable()
            main()
            profiler.disable()
            stats = pstats.Stats(profiler).sort_stats('ncalls')
            stats.print_stats()
        elif sys.argv[4] == '-cumtime':
            profiler = cProfile.Profile()
            profiler.enable()
            main()
            profiler.disable()
            stats = pstats.Stats(profiler).sort_stats('cumtime')
            stats.print_stats()
    else:
        main()



