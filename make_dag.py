#!/usr/env python3
import os, sys

#########################################
# Going to do this in a braindead way.
# Feel free to spruce your own script
# up to make it more easily usable.
########################################

########################################
# Set up your paths and variables that you want to use
########################################
script = "/data/condor_builds/users/mlarson/condor_examples/test_script.py"
submit_file = "/data/condor_builds/users/mlarson/condor_examples/submit.sub"

dag_name = "myjobs.dag"

dataset_dir = "/data/i3store/users/mjlarson/ps_tracks/version-004-p01/"
outdir = "/data/condor_builds/users/mlarson/condor_examples/output/"
logdir = "/data/condor_builds/users/mlarson/condor_examples/logs/"

# And any other variables you might need
ntrials_per_file = 100
nfiles_per_nside = 10
nside = 256

########################################
# Make a string where we can store our file contents
########################################
dag_contents = ""

########################################
# Start looping over things 
########################################
for filenum in range(nfiles_per_nside):

    # every job needs a unique name.
    job_name = "test_script_{}_{}".format(nside, filenum)

    # And an output file name
    outfile = os.path.join(outdir, job_name+".npy")

    # Write out the arguments that you need to run the script
    arguments = "--dataset_dir {} ".format(dataset_dir)
    arguments += "--ntrials {} ".format(ntrials_per_file)
    arguments += "--nside {} ".format(nside)
    arguments += "--outfile {} ".format(outfile)

    # Now we start writing Condor stuff.
    # We'll start with the basic stuff that's always here
    # no matter what you're trying to run
    dag_contents += f"JOB {job_name} {submit_file}\n"
    dag_contents += f"VARS {job_name} "
    dag_contents += f" job_name=\"{job_name}\" "
    dag_contents += f" log_dir=\"{logdir}\" "
    dag_contents += f" exe=\"{script}\" "
    dag_contents += f" args=\"{arguments}\" "
    dag_contents += "\n"

    # Done. Move to the next trial.

########################################
# Write the dag file out
########################################
open(dag_name, 'w').write(dag_contents)
