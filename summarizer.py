import re

def summarizer(AMRs, coreferences, n):
	"""
	Outputs a summary given an article in MSAMR format and its
	resolved coreferences.
	"""

	# Create dictionary to store each AMR and its score
	AMR_scores = {}

	# Iterate through each concept in the coreferences dictionary
	for concept, variables in coreferences.items():

		# Save each AMR that references that concept to a list,
		# and iterate through that list
		AMRs = [AMR for AMR, variable in variables]
		for AMR in AMRs:

			# Every time that AMR mentions that concept, add the number of reentrancies that
			# concept has to the AMR score (this weights the score by frequency, and therefore
			# importance, of the concept)
			AMR_scores[AMR] = AMR_scores.get(AMR, 0) + len(variables)

	# Convert dictionary of AMR scores into list sorted from highest to lowest scores,
	# then remove scores from list
	AMR_scores = [(AMR, score) for AMR, score in AMR_scores.items()]
	AMR_scores.sort(reverse=True, key=lambda x: x[1])
	AMRs_sorted = [AMR for AMR, score in AMR_scores]

	# Pick the foremost AMRs in the list for the summary, as these
	# will have the highest scores. Size of the summary is scaled
	# based on n, such that every n sentences in the text will result
	# in 1 additional sentence in the summary
	summary_AMRs = AMRs_sorted[:len(AMRs_sorted)//n]

	# Return selected AMRs as the summary
	return summary_AMRs

# Test input
AMRs = ["AMR_1", "AMR_2", "AMR_3", "AMR_4", "AMR_5"]
coreferences = {"concept_1": [(1, "a"), (2, "g"), (2, "b2"), (4, "c"), (5, "p")], "concept_2": [(2, "l1"), (5, "j")]}
n = 2

summary_AMRs = summarizer(AMRs, coreferences, n)

print(summary_AMRs)
