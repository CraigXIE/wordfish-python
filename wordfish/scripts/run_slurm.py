import os
import sys
script_dir = os.path.dirname(os.path.realpath(__file__))
job_dir = "%s/.job" %(script_dir)
out_dir = "%s/.out" %(script_dir)


if len(sys.argv) < 2:
    print 'Please provide job file with list of single commands as input.'

else:
    jobfile = sys.argv[1]

    if not os.path.exists(job_dir):
        os.mkdir(job_dir)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    # Read in the jobfile, and write a job for each line
    filey = open(jobfile,"rb")
    commands = filey.readlines()
    filey.close()

    # Name the job based on input script
    name = os.path.basename(jobfile).split(".")[0]

    for c in range(len(commands)):
        command = commands[c]
        jobfile = open("%s/%s_%s.job" %(job_dir,name,c),'w')
        jobfile.writelines("#!/bin/bash\n")
        jobfile.writelines("#SBATCH --job-name=%s_%s.job\n" %(name,c))
        jobfile.writelines("#SBATCH --output=%s/%s_%s.out\n" %(out_dir,name,c))
        jobfile.writelines("#SBATCH --error=%s/%s_%s.err\n" %(out_dir,name,c)) 
        jobfile.writelines("#SBATCH --time=2-00:00\n") 
        jobfile.writelines("#SBATCH --mem=12000\n")   
        jobfile.writelines(command)  
        jobfile.close()
        os.system('sbatch -p normal -n 1 %s/%s_%s.job' %(job_dir,name,c))
