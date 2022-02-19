import os
import re
import amrlib
import random

def pseudo_summarizer(file):
	
	#Load amrlib models for parsing and generation
	p = '/Users/chris/Code/model_parse_spring-v0_1_0'
	g = '/Users/chris/Code/model_generate_t5-v0_1_0'
	stog = amrlib.load_stog_model(model_dir=p)
	gtos = amrlib.load_gtos_model(model_dir=g)

	# Open file and save each sentence to a different line
	with open(file) as f:
		summary = []
		sentences = [sentence.rstrip() for sentence in f.readlines()]

		for i in range(0,len(sentences)):
			if i % 2 == 0:
				summary.append(sentences[i])

		#Parse multi-sentence AMR from "randomly" selected sentences (Text-to-AMR)
		graphs = stog.parse_sents(summary)
		f.close()		
	
	#Generate text from multi-sentence AMR (AMR-to-text)
	parser_output = stog.parse_sents(summary)
	sents, _ = gtos.generate(parser_output, disable_progress=False)

	# Create output file with MSAMR
	with open("output2.txt", "w") as o2:
		o2.write(str(sents))

pseudo_summarizer("input.txt")
