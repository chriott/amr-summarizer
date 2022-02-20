import os
import re
import amrlib
import random

def pseudo_summarizer(file, option='random', summary_length=4):
	"""
	Takes a file of sentences as input, converts each sentence to a single-line AMR,
	randomly selects four AMRs, and from these creates a pseudo-multi-sentence AMR.
	"""

	# Open file and save each sentence to a different line
	with open(file) as f:
		sentences = [sentence.rstrip() for sentence in f.readlines()]

	#Load amrlib models for parsing and generation
	p = 'model_parse_spring-v0_1_0'
	g = 'model_generate_t5-v0_1_0'
	stog = amrlib.load_stog_model(model_dir=p)
	gtos = amrlib.load_gtos_model(model_dir=g)

	# Convert each sentence to a list of multi-line AMRs
	parser_output = stog.parse_sents(sentences)

	# Remove original sentence and tabs and new lines,
	# converting multi-line AMRs into single-line AMRs
	AMRs = []
	for AMR in parser_output:
		AMR = re.sub(r"""# ::snt .*?\n""", r"""""", AMR)
		AMR = re.sub(r""" {6}""", r"""""", AMR)
		AMR = re.sub(r"""\n""", r""" """, AMR)
		AMRs.append(AMR)

	# Random selection
	# If number of AMRs greater than target summary length, select n AMRs at random
	# otherwise, pass on list of AMRs unchanged
	if option == 'random':
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
	print('one-line summary AMRs\t', summary_AMRs)


	# Convert to multi-sentence AMR

	# Break one-line to multi-line AMRs
	ml_summary_AMRs = []
	for amr in summary_AMRs:
		ml_summary_AMRs.append(amr.replace(':', '\n\t:'))

	# TODO remove print line
	print('multi-line summary AMRs\t', summary_AMRs)

	MSAMR = '(z999 / multi-sentence'
	for amr in ml_summary_AMRs:
		# add :sntx tag to each sentence AMR (:snt1, :snt2, ... , :sntn)
		# add newline and indent before appending
		# TODO: adjust number of indents to concept depth
		# TODO: rename concept variables to remove duplicates
		# (they start from z0 in each sentence)
		MSAMR += '\n\t:snt' + str(ml_summary_AMRs.index(amr)+1) + ' ' + amr
	MSAMR += ')'

	# TODO remove print line
	print(MSAMR)


	#Generate text from multi-sentence AMR (AMR-to-text)
	sents, _ = gtos.generate(MSAMR, disable_progress=False)

	# Create output file with MSAMR
	with open("output.txt", "w") as o2:
		o2.write(str(sents))


if __name__ == '__main__':
	# TODO: add sys.argv structure
	# options for argument 2: 'random', 'first'
	# options for argument 3: any integer
	pseudo_summarizer("input.txt", 'first', '2')
