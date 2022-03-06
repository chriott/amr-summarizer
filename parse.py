import cProfile, pstats
import os
import re
import time

import amrlib
import random
import sys

def parse(file):

    '''
    Reads in a text file,
    parses it into multi-line AMRs,
    and writes those AMRs into output file 'parsed_amrs.txt'.
    '''

    start = time.process_time()
    # Open file and save each sentence to a different line
    with open(file) as f:
        sentences = [sentence.rstrip() for sentence in f.readlines()]
        print('reading done')
        a = time.process_time() - start
        print('time taken to read in inputfile:', a, 'seconds')

    # Load amrlib models for parsing
    p = './model_parse_spring-v0_1_0'
    stog = amrlib.load_stog_model(model_dir=p)
    print('loading parser done')
    b = time.process_time() - a
    print('time taken to load parser:', b, 'seconds')

    # Convert each sentence to a list of multi-line AMRs
    parser_output = stog.parse_sents(sentences)
    print('parsing done')
    c = time.process_time() - b
    print('time taken to parse sentences:', c, 'seconds')

    # Output the multi-line AMRs into parsed_amrs.txt
    with open('parsed_amrs.txt','w') as w:
        for amr in parser_output:
            w.write(amr + '\n' )
    print('writing done')
    d = time.process_time() - c
    print('time taken to write sentences into output file:', d, 'seconds')


def main():
    if len(sys.argv) != 3 and len(sys.argv) != 2:
        print('Usage: python parse.py <input file> <optional \'-n\',\'-ncalls\',\'-cumtime\'>')
        sys.exit(1)
    else:
        textfile = sys.argv[1]
        parse(textfile)

        # argument 1: text file
        # argument 2: code runs a profiler as a default, add argument '-n' to run without the profiler


if __name__ == '__main__':
    if len(sys.argv) == 3:
        if sys.argv[2] == '-n':
            main()
        elif sys.argv[2] == '-ncalls':
            profiler = cProfile.Profile()
            profiler.enable()
            main()
            profiler.disable()
            stats = pstats.Stats(profiler).sort_stats('ncalls')
            stats.print_stats()
        elif sys.argv[2] == '-cumtime':
            profiler = cProfile.Profile()
            profiler.enable()
            main()
            profiler.disable()
            stats = pstats.Stats(profiler).sort_stats('cumtime')
            stats.print_stats()
    else:
        main()



