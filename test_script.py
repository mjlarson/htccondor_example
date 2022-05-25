#!/usr/bin/env python3
#------------------------------------------------------------------------------#
# Test script for use in the condor examples. Doesn't do anything terribly     #
#  interesting, so don't expect much from it. Basically will just scramble     #
#  experimental data and return an array containing the maximum number of      #
#  events per pixel for each trial. Writes a file solely so students can see   #
#  the file IO with a condor job submission.                                   #
#------------------------------------------------------------------------------#
import os, sys, glob, copy, argparse
import numpy as np
import numpy.lib.recfunctions as rf

import healpy as hp

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset_dir", type=str,
                    default = "/data/i3store/users/mjlarson/ps_tracks/version-004-p01/",
                    help = "Path to the NuSources npy files")
parser.add_argument("-n", "--ntrials", type=int,
                    default = 1,
                    help = "The number of trials to run")
parser.add_argument("--nside", type=int,
                    default = 128,
                    help = "The healpix nside to use. Defaults to 256")
parser.add_argument("-o", "--outfile", required=True,
                    help = "Name of the output file (ending in .npy")
args = parser.parse_args()


# #######################################
# Function to read in and merge all of the
# npy files from IC86 data
# #######################################
def load_exp():
    file_path = os.path.join(args.dataset_dir, "IC86*exp.npy")
    print("Loading files from {}".format(file_path))
    files = glob.glob(file_path)
    print("... Found {} IC86 files to load.".format(len(files)))

    # Start reading the files
    merged = []
    for f in sorted(files):
        events = np.load(f)
        merged.append(events)

    # Combine them
    return np.concatenate(merged)

# #######################################
# Scramble the events in right ascension
# Note that we'll copy the array here so
# that we don't change the original.
# #######################################
def scramble(events):
    events_copy = np.copy(events)
    new_ra = np.random.uniform(0, 2*np.pi, len(events_copy))
    events_copy['ra'] = new_ra
    return events_copy

# #######################################
# Bin in a healpix map
# #######################################
def bin_to_healpix(events):
    # find the bin for each event. Note that
    # healpy is screwy here and doesn't directly
    # accept RA/dec coordinates. Instead, we have
    # to pass them in in degrees and use a separate
    # option...
    ra, dec = events['ra'], events['dec']
    bin_indices = hp.ang2pix(args.nside,
                             np.degrees(ra),
                             np.degrees(dec),
                             lonlat=True)

    # Fill the array using the found indices, assuming
    # each event counts as once (ie, that we don't have
    # any event weights to think about).
    npixels = hp.nside2npix(args.nside)
    empty_map = np.zeros(npixels, dtype=np.float32)

    # Simplify this and just find out which indices have
    # events and how many for each bin
    unique_indices, unique_counts = np.unique(bin_indices, return_counts=True)
    empty_map[unique_indices] = unique_counts

    # And finally return
    return empty_map


# #######################################
# Run it
# #######################################
data = load_exp()

npixels_filled = np.zeros(args.ntrials, dtype=int)

for trial_num in range(args.ntrials):
    print("Trial {}".format(trial_num), end='... ')
    events = scramble(data)
    healpix_map = bin_to_healpix(events)
    print("Found a maximum of {} events in one bin".format(healpix_map.max()))
    npixels_filled[trial_num] = healpix_map.max()


# And write it out
np.save(args.outfile, npixels_filled)
