# SAMRY: Summarization with Abstract Meaning Representation made easY

### About

This is an end-to-end AMR-based summarization model. It was created as part of the software project "Applications for AMR" by Lucia Donatelli at Saarland University.

There are four files which together contain all versions of the summarization models: baseline.py, baseline_eval.py, samry.py and samry_eval.py. 
The implementation in baseline.py and in samry.py are suitable for practical purposes, and the implementation in baseline_eval.py and samry_eval.py are used to evaluate the quality of the summarization models. Please see our paper *link to paper* for information on how each algorithm works.

As input, baseline.py and samry.py take a .txt file containing an English text with each sentence on a separate line. They each summarize the text and output the summary into a file named 'baseline_summary.txt' or 'samry_summary.txt' respectively.
baseline_eval.py and samry_eval.py take a file from the proxy report section of the AMR bank corpus, which includes several news reports and their corresponding gold standard summary. They extract each news report and generate a summary of each, and then they evaluate the quality of the generated summary compared to the gold standard. We use ROUGE-1, ROUGE-2 and ROUGE-L as our evaluation metrics. An evaluation of each summary is printed to the console, as well as the average scores over the whole corpus.

There are several versions of each model. You will be prompted to choose between them when running the respective python script. The baseline model will prompt you to choose between 'first' and 'random' as well as choose an integer summary length. Choosing 'first' will cause the baseline model to use the first n sentences as a summary, and choosing 'random' will cause the baseline model to use n random sentences from the source text as the summary. N is the length of the desired summary in sentences.
The SAMRY model will prompt you to choose between 'absolute' and 'relative'. Choosing 'absolute' will allow you to choose an absolute summary length of n sentences, and you will be prompted to choose a value for n. Choosing 'relative' will cause the generated summaries to have a length relative to the length of their source text. In this case, you will be prompted to choose a value for n, and your summary will be the length of the text divided by n.


## Running the baseline

### Requirements

Before running, you will need to install the following dependencies:

1) amrlib
```
pip install amrlib
```
2) penman library
```
pip install penman
```
3) The pretrained spring parser and generator model. Download and un-tar the following models into the amr-summarizer folder, or into the folder containing the baseline.py file.

| Name              	| Version 	| Date       	| Size  	| Score       	| DL 	|
|-------------------	|---------	|------------	|-------	|-------------	|----	|
| parse_spring      	| 0.1.0   	| 2021-11-25 	| 1.5GB 	| 83.5 SMATCH 	| [Link](https://github.com/bjascob/amrlib-models/releases/download/model_parse_spring-v0_1_0/model_parse_spring-v0_1_0.tar.gz)   	|
| generate_t5wtense 	| 0.1.0   	| 2020-12-30 	| 787MB 	| 54/44 BLEU  	| [Link](https://github.com/bjascob/amrlib-models/releases/download/model_generate_t5wtense-v0_1_0/model_generate_t5wtense-v0_1_0.tar.gz)  	|

You will need a stable internet connection to run these models in the code.


### Usage

#### Running baseline.py

To run baseline.py, simply run the script with the file containing the text you would like to summarize as an argument:
```
python baseline.py textfile.txt
```

You will be prompted to choose between 'random' and 'first'. Choosing 'random' will cause the summarizer to use n random sentences from the input text as the summary. Choosing 'first' will cause the summarizer to use the n first sentences as the summary.
```
random
```
You will then be asked to choose how many sentences the summary should contain. Simply enter any integer:
```
2
```
The summary will then be written to a file called 'baseline_summary.txt', which should appear in the folder containing your baseline.py file.

#### Running baseline_eval.py


## Running SAMRY

### Requirements

Before running, you will need to install the following dependencies:

1) amrlib
```
pip install amrlib
```
2) penman library
```
pip install penman
```
3) The pretrained spring parser and generator model. Download and un-tar the following models into the amr-summarizer folder, or into the folder containing the baseline.py file.

| Name              	| Version 	| Date       	| Size  	| Score       	| DL 	|
|-------------------	|---------	|------------	|-------	|-------------	|----	|
| parse_spring      	| 0.1.0   	| 2021-11-25 	| 1.5GB 	| 83.5 SMATCH 	| [Link](https://github.com/bjascob/amrlib-models/releases/download/model_parse_spring-v0_1_0/model_parse_spring-v0_1_0.tar.gz)   	|
| generate_t5wtense 	| 0.1.0   	| 2020-12-30 	| 787MB 	| 54/44 BLEU  	| [Link](https://github.com/bjascob/amrlib-models/releases/download/model_generate_t5wtense-v0_1_0/model_generate_t5wtense-v0_1_0.tar.gz)  	|

You will need a stable internet connection to run these models in the code.

3) The AMR coreference model [amr_coref](https://github.com/bjascob/amr_coref)

Currently, there is no pip install of amr_coref, so you will have to clone it:
```
git clone https://github.com/bjascob/amr_coref.git
```
Clone the above link directly into the folder containing pipeline.py.

In order to use amr_coref, you will also have to download a pre-trained model and insert it into the right place in your directory.
The pre-trained model can be downloaded [here](https://github.com/bjascob/amr_coref/releases). Go to this link and download the file 'model_coref-v0.1.0.tar.gz'.
Then, navigate into your 'amr_coref' folder and create a directory there called ```data```.
Insert the 'model_coref-v0.1.0.tar.gz' file into ```data``` and un-tar the model.

For this model to run, you will have to make some modifications to its configurations.
To do so, navigate to ```\amr-summarizer\amr_coref\data\model_coref-v0.1.0```. You should see a file called ```config.json```.
Open ```config.json``` with your editor and change "device":"cuda" to "device":"cpu", as well as "num_workers": 4 to "num_workers": 0.

You will need to make some modifications to the code itself as well.
Navigate to amr_coref/amr_coref/coref/coref_featurizer.py. Then, comment out line 242 ('with Pool(processes=processes, maxtasksperchild=maxtpc) as pool:').
Reduce the indent of lines 243-248 (until 'pbar.close()') by 1. Finally, change line 243 to 'for fdata in map(worker, idx_keys):'.


In amr_coref_model:
in line 249, add parameter map_location:
model_dict = torch.load(os.path.join(model_dir, model_fn), map_location='cpu')


### Usage

#### Running pipeline.py

To run pipeline.py, simply enter the following command (note that you may need to use a different command for python, such as py or python3):

```
python pipeline.py textfile.txt
```


#### Running pipeline_eval.py


To run eval.py, first install the ROUGE code and word2number
```
pip install rouge_score
pip install word2number
```

Then run the script with AMR bank proxy report file as an argument. We have included two compatible files, _ and _ , which can be used for this task:
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


### Results

Our baseline model achieves these results:

| Random/first              	| n 	| ROUGE-1       	| ROUGE-2  	| ROUGE-L      	|
|-------------------	|---------	|------------	|-------	|-------------	|
| first   	| 1  	| precision: 0.3596 recall: 0.3563 fscore: 0.3378 	| precision: 0.2007 recall: 0.2078 fscore: 0.1925 	| precision: 0.3052 recall: 0.3057 fscore: 0.2880	|
| first 	|  2  	| precision: 0.5134 recall: 0.2922 fscore: 0.3536 	| precision: 0.3021 recall: 0.1653 fscore: 0.2034 	| precision: 0.4285 recall: 0.2417 fscore: 0.2937  	| 
| random | 1 |  precision: 0.1964 recall: 0.2525 fscore: 0.2037 | precision: 0.0488 recall: 0.0761 fscore: 0.0555 | precision: 0.1532 recall: 0.2022 fscore: 0.1603 |
| random | 2 | precision: 0.3059 recall: 0.1875 fscore: 0.2203 | precision: 0.0967 recall: 0.0585 fscore: 0.0685 | precision: 0.2258 recall: 0.1364 fscore: 0.1607 |
