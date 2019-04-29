import numpy as np
import os
from skimage import io
from IPython.display import clear_output
# https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Online_algorithm
# found a python implementatin of Welford's algorithm on wikipedia.

# for a new value newValue, compute the new count, new mean, the new M2.
# mean accumulates the mean of the entire dataset
# M2 aggregates the squared distance from the mean
# count aggregates the number of samples seen so far
def update(existingAggregate, newValue):
    (count, mean, M2) = existingAggregate
    count += 1 
    delta = newValue - mean
    mean += delta / count
    delta2 = newValue - mean
    M2 += delta * delta2

    return (count, mean, M2)

# retrieve the mean, variance and sample variance from an aggregate
def finalize(existingAggregate):
    (count, mean, M2) = existingAggregate
    (mean, variance, sampleVariance) = (mean, M2/count, M2/(count - 1)) 
    if count < 2:
        return float('nan')
    else:
        return (mean, variance, sampleVariance)

def compute_training_set_statistics(patch_path):

	patch_list = [a for a in os.listdir(patch_path) if a.endswith('.tif')]
	existingAggregate = (0,0,0)

	for p in patch_list:  #TODO remove slice
		clear_output(wait=True)
		print(p)

		patch = io.imread('{}/{}'.format(patch_path, p))
		existingAggregate = update(existingAggregate, np.mean(patch))

	mean, variance, sampleVariance = finalize(existingAggregate)

	return mean, sampleVariance

def count_classes(gt_path):

	patches = [a for a in os.listdir(gt_path) if a.endswith('.tif')]

	classes = np.zeros(3)  # seems to be expecting 5 dimensions instead of 3..

	for p in patches:  #TODO remove slice
		clear_output(wait=True)
		print(p)

		patch = io.imread('{}/{}'.format(gt_path, p))

		patch = np.rollaxis(patch, np.argmin(patch.shape), 3)       # <-- is kept at the same place now..

		# print(np.sum(patch, axis=0))
		# print(np.sum(np.sum(patch, axis=0), axis=0))

		classes += np.sum(np.sum(patch, axis=0), axis=0)


	return classes