# AMR Software project

### About

This is an end-to-end summarization model based on AMR.

As input, this summarizer takes a file of English sentences on separate lines. 
There are also options to specify if you prefer sentences to be selected in order
starting from the beginning, rather than randomly, as well as how many sentences 
you wish to use in your summary.

### Requirements

Before running, one needs to install the following dependencies:

- amrlib
```
pip3 install amrlib
```

- The pretrained spring parser and generator model. Extract the following models into the amr-summarizer folder

| Name              	| Version 	| Date       	| Size  	| Score       	| DL 	|
|-------------------	|---------	|------------	|-------	|-------------	|----	|
| parse_spring      	| 0.1.0   	| 2021-11-25 	| 1.5GB 	| 83.5 SMATCH 	| [Link](https://github.com/bjascob/amrlib-models/releases/download/model_parse_spring-v0_1_0/model_parse_spring-v0_1_0.tar.gz)   	|
| generate_t5wtense 	| 0.1.0   	| 2020-12-30 	| 787MB 	| 54/44 BLEU  	| [Link](https://github.com/bjascob/amrlib-models/releases/download/model_generate_t5wtense-v0_1_0/model_generate_t5wtense-v0_1_0.tar.gz)  	|


- [amr_coref](https://github.com/bjascob/amr_coref)

Currently, there is no pip install of amr_coref so you have to clone it
```
git clone 
```
The pre-trained model can be downloaded [here](https://github.com/bjascob/amr_coref/releases)
To use the model create a data ```directory``` and un-tar the model in it.
The pre-trained model can be downloaded [here](https://github.com/bjascob/amr_coref/releases)


### Usage

Example commandline prompt:
```
python pseudo-summarizer.py input.txt first 2
```
Argument 2 is a .txt file containing English sentences.
Argument 3 can be 'first' or 'random_select'. If you choose 'first', the generator will output the first n sentences as a summary, and if you choose 'random_select', the generator will choose n random sentences from the input text file as a summary.
Argument 4 represents the number of sentences your summary should contain.


With this input, the program:
  1) parses them to sentence AMRs using SPRING, 
  2) converts each AMR to a single-line AMR, 
  3) selects a number of AMRs, depending on the selected model, 
  4) from these creates a pseudo-multi-sentence AMR, 
  5) and generates a summary from that, using T5wtense (based on the T5 transformer from [Huggingface](https://github.com/huggingface/transformers))

The summary is written to a text file (output.txt).
