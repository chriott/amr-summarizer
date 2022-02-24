# AMR Software project

This is an end-to-end summarization model based on AMR.

Before running, one needs the latest install the following dependency:

AMRLib, including the Spring parser, which can be found here:
https://amrlib.readthedocs.io/en/latest/install/

As input, this summarizer takes a file of English sentences on separate lines. 
There are also options to specify if you prefer sentences to be selected in order
starting from the beginning, rather than randomly, as well as how many sentences 
you wish to use in your summary.

Example commandline prompt:
```
python pseudo-summarizer.py input.txt first 2
```

With this input, the program:
  1) parses them to sentence AMRs using SPRING, 
  2) converts each AMR to a single-line AMR, 
  3) selects a number of AMRs, depending on the selected model, 
  4) from these creates a pseudo-multi-sentence AMR, 
  5) and generates a summary from that, using T5wtense (based on the T5 transformer from [Huggingface](https://github.com/huggingface/transformers))
