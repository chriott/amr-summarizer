import os
import re
import amrlib
import random
import sys

def pseudo_summarizer(file, option='random_select', summary_length=4):
	"""
	Takes a file of sentences as input,
	parses them to sentence AMRs using SPRING,
	converts each AMR to a single-line AMR,
	selects a number of AMRs, depending on the selected model,
	from these creates a pseudo-multi-sentence AMR,
	and generates a summary from that, using SPRING
	"""

	# Open file and save each sentence to a different line
	with open(file) as f:
		sentences = [sentence.rstrip() for sentence in f.readlines()]
		print('reading done')

	#Load amrlib models for parsing and generation
	p = 'model_parse_spring-v0_1_0'
	g = 'model_generate_t5-v0_1_0'
	stog = amrlib.load_stog_model(model_dir=p)
	gtos = amrlib.load_gtos_model(model_dir=g)
	print('loading models done')

	# Convert each sentence to a list of multi-line AMRs
	parser_output = stog.parse_sents(sentences)
	print('parsing done')

	# Remove original sentence and tabs and new lines,
	# converting multi-line AMRs into single-line AMRs
	AMRs = []
	for AMR in parser_output:
		AMR = re.sub(r"""# ::snt .*?\n""", r"""""", AMR)
		AMR = re.sub(r""" {6}""", r"""""", AMR)
		AMR = re.sub(r"""\n""", r""" """, AMR)
		AMRs.append(AMR)
	print('single line conversion done')

	# PSEUDO SUMMARIZATION
	# If number of AMRs greater than target summary length, select n AMRs at random
	# otherwise, pass on list of AMRs unchanged
	if option == 'random_select':
		if len(AMRs) > int(summary_length):
			summary_AMRs = random.choices(AMRs, k = int(summary_length))
		else:
			summary_AMRs = AMRs

	# Selection of first n sentences
	# If number of AMRs greater than target summary length, select first n AMRs
	# otherwise, pass on list of AMRs unchanged
	if option == 'first':
		if len(AMRs) > int(summary_length):
			summary_AMRs = AMRs[:int(summary_length)]
		else:
			summary_AMRs = AMRs

	# TODO remove print line
	print('single-line summary AMRs\t', summary_AMRs)


	# Convert sentence AMRs to one multi-sentence AMR
	MSAMR = '(z999 / multi-sentence '
	for amr in summary_AMRs:
		# add :sntx tag to each sentence AMR (:snt1, :snt2, ... , :sntn)
		# TODO: rename concept variables to remove duplicates
		# (they start from z0 in each sentence)
		MSAMR += ':snt' + str(summary_AMRs.index(amr)+1) + ' ' + amr
	MSAMR += ')'
	MSAMR_list = [MSAMR]
	print('MS-AMR conversion done')

	#Generate text from multi-sentence AMR (AMR-to-text)
	sents, _ = gtos.generate(MSAMR_list, disable_progress=False)
	print('generation done')

	# Create output file with generated sentences
	# TODO: apply spacy to separate sentences
	with open("output3.txt", "w") as o2:
		o2.writelines(sents)
		print('writing done')


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print('Usage: python pseudo-summarizer_2.0.py <input file> <option \'random_select\' or \'first\'> <summary length>')
		sys.exit(1)
	# argument 1: text file with 1 sentence per line
	# argument 2: options 'random_select' and 'first'
	# argument 3: any integer
	pseudo_summarizer(sys.argv[1], sys.argv[2], sys.argv[3])
