Example script and dag creation code for use in teaching HTC Condor.


Usage:

Create a script you'd like to run. Make it executably by adding the relavent shebang at the top (see the first few lines of test_script.py for an example using icetray code) and running `chmod u+x <filename>`.

Next, make sure you can run your script from the command line. In principle, this will work out to something like
> ./test_script.py --outfile test.npy --nside 128

We'll split this into two pieces: the executable script ("./test_script.py"), which is the same for all jobs, and the arguments ("--outfile test.npy --nside 128"), which can vary for each job.

Next, modify the `make_dag.py` script so that the `arguments` lines include the needed options for your specific script.

Once ready, run
> python3 make_dag.py

which will create a new file called `myjobs.dag`. This contains all of the information needed to run all of your jobs. You can crack this open and look at the first few lines using the `head` command
> head myjobs.dag

>JOB test_script_256_0 /data/condor_builds/users/mlarson/condor_examples/submit.sub
>
>VARS test_script_256_0  job_name="test_script_256_0"  log_dir="/data/condor_builds/users/mlarson/condor_examples/logs/"  cmd="/data/condor_builds/users/mlarson/condor_examples/test_script.py --dataset_dir /data/i3store/users/mjlarson/ps_tracks/version-004-p01/ --ntrials 100 --nside 256 --outfile /data/condor_builds/users/mlarson/condor_examples/output/test_script_256_0.npy " 

We need to test our command to make sure it's functional. The way we do this here is to copy everything inthe paranthesis after `cmd=` and try to run it. In this case, we'll do this:
> /usr/bin/env /data/condor_builds/users/mlarson/condor_examples/test_script.py --dataset_dir /data/i3store/users/mjlarson/ps_tracks/version-004-p01/ --ntrials 100 --nside 256 --outfile /data/condor_builds/users/mlarson/condor_examples/output/test_script_256_0.npy

This should run to completion, but note that it includes my directories and your line may look slightly different.

Once the test runs, we're ready to submit. We can do this by running
> condor_submit_dag myjobs.dag

This will begin the process of actually submitting your jobs to the cluster. If you'd like to check on them, run
> tail -f myjobs.dag.dagman.out | grep -a3 Done

which will start printing out updates from condor by reading the myjobs.dag.dagman.out file. You'll want to look for lines like this:
> 05/25/22 15:51:35 Of 10 nodes total:
>
> 05/25/22 15:51:35  Done     Pre   Queued    Post   Ready   Un-Ready   Failed
> 
> 05/25/22 15:51:35   ===     ===      ===     ===     ===        ===      ===
> 
> 05/25/22 15:51:35     3       0        7       0       0          0        0
> 
> 05/25/22 15:51:35 0 job proc(s) currently held

This tells us how many jobs are done, how many are currently waiting or running ("Queued"), how many are waiting to be submitted ("Ready" and "Un-Ready"), and how many have failed ("Failed"). It'll also tell you if any are held, which normally indicates that they have hit a memory limit or have otherwise exceeded their allowed resources.


