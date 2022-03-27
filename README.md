# AMR Summarization Model

### About

This is an end-to-end AMR-based summarization model. It was created as part of the software project "Applications for AMR" by Lucia Donatelli at Saarland University.

There are two files which each contain all versions of the summarization models: summarizer.py and eval.py. 
The implementation in summarizer.py is suitable for practical purposes, and the implementation in eval.py is used to evaluate the quality of the summarization models.
As input, summarizer.py takes a .txt file containing an English text with each sentence on a separate line. It summarizes this text and outputs the summary into a file with the name 'summary.txt'. 
eval.py takes a file from the proxy report section of the AMR bank corpus, which includes several news reports and their corresponding gold standard summary. It extracts and generates a summary of each news report, and then evaluates the quality of the generated summary compared to the gold standard. We use ROUGE-1, ROUGE-2 and ROUGE-L as our evaluation metrics. An evaluation of each summary is printed to the console, as well as the average scores over the whole corpus.

There are several versions of the model. You will be prompted to choose between them when running the python script. The baseline model works by choosing n sentences from the original text and using these as the summary. In this version, you can have the model use either the first n sentences or choose n random sentences to use for the summary. You will also be prompted to choose the length of the summary in number of sentences.


### Requirements

Before running, you will need to install the following dependencies:

1) amrlib
```
pip3 install amrlib
```
2) penman library
```
pip install penman
```
3) The pretrained spring parser and generator model. Download and un-tar the following models into the amr-summarizer folder, or into the folder containing the summarizer.py file.

| Name              	| Version 	| Date       	| Size  	| Score       	| DL 	|
|-------------------	|---------	|------------	|-------	|-------------	|----	|
| parse_spring      	| 0.1.0   	| 2021-11-25 	| 1.5GB 	| 83.5 SMATCH 	| [Link](https://github.com/bjascob/amrlib-models/releases/download/model_parse_spring-v0_1_0/model_parse_spring-v0_1_0.tar.gz)   	|
| generate_t5wtense 	| 0.1.0   	| 2020-12-30 	| 787MB 	| 54/44 BLEU  	| [Link](https://github.com/bjascob/amrlib-models/releases/download/model_generate_t5wtense-v0_1_0/model_generate_t5wtense-v0_1_0.tar.gz)  	|


3) The AMR coreference model [amr_coref](https://github.com/bjascob/amr_coref)

Currently, there is no pip install of amr_coref, so you will have to clone it:
```
git clone https://github.com/bjascob/amr_coref.git
```
The pre-trained model can be downloaded [here](https://github.com/bjascob/amr_coref/releases). To use the model create a ```data``` directory and un-tar the model in it.

! This dependency is not necessary if you are only using the 'baseline' version of the model.


### Usage

#### Running summarizer.py

To run summarizer.py, simply run the script with the file containing the text you would like to summarize as an argument:
```
python summarizer.py textfile.txt
```
You will be prompted to choose which version of the summarization model to use. Simply enter 'baseline' into the command prompt:
```
baseline
```
You will be prompted to choose between 'random' and 'first'. Choosing 'random' will cause the summarizer to use n random sentences from the input text as the summary. Choosing 'first' will cause the summarizer to use the n first sentences as the summary.
```
random
```
You will then be asked to choose how many sentences the summary should contain. Simply enter any integer:
```
2
```
The summary will then be written to a file called 'summary.txt', which should appear in the folder containing your summarizer.py file.


#### Running eval.py


To run eval.py, run the script with AMR bank proxy report file as an argument. We have included two compatible files, _ and _ , which can be used for this task:
```
python eval.py amr-release-3.0-amrs-proxy.txt
```
You will be prompted to choose which version of the summarization model to use. Simply enter 'baseline' into the command prompt:
```
baseline
```
You will be prompted to choose between 'random' and 'first'. Choosing 'random' will cause the summarizer to use n random sentences from the input text as the summary. Choosing 'first' will cause the summarizer to use the n first sentences as the summary.
```
random
```
You will then be asked to choose how many sentences the summary should contain. Simply enter any integer:
```
2
```
For each news article in your proxy report file, the summary generated by our summarizer model will be printed, along with the gold-standard summary. ROUGE-1, ROUGE-2 and ROUGE-L scores will be printed for each generated summary/gold-standard summary pair as well as average scores for the whole corpus.


