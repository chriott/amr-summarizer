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

	# Load AMR parser
	p = 'model_parse_spring-v0_1_0'
	stog = amrlib.load_stog_model(model_dir=p)

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

	# If number of AMRs greater than target summary length, select n AMRs at random
	# otherwise, pass on list of AMRs unchanged
	if option == 'random':
		if len(AMRs) > int(summary_length):
			summary_AMRs = random.choices(AMRs, k = int(summary_length))
		else:
			summary_ARMs = AMRs

	# If number of AMRs greater than target summary length, select first n AMRs
	# otherwise, pass on list of AMRs unchanged
	if option == 'first':
		if len(AMRs) > int(summary_length):
			summary_AMRs = AMRs[:int(summary_length)]
		else:
			summary_AMRs = AMRs

	# Convert to multi-sentence AMR
	# TODO
	MSAMR = "\n".join(summary_AMRs)

	# Create output file
	with open("output.txt", "w") as o:
		o.write(MSAMR)


if __name__ == '__main__':
	# TODO add sys.argv structure
	# options for argument 2: 'random', 'first'
	# options for argument 3: any integer
	pseudo_summarizer("input.txt", 'first', '2')
