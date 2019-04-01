module load singularity
TMPDIR=/home/evansj/me/tmp/ \
      java -Xmx15g -Xms15g -jar -Dconfig.file=hpc.conf \
      /mnt/isilon/dbhi_bfx/apps/bin/cromwell-36.jar run \
      paired-fastq-to-unmapped-bam.wdl \
      -i paired-fastq-to-unmapped-bam.inputs.json \
      -m metadata.json &> test.er
