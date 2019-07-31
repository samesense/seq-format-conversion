module load singularity
TMPDIR=/home/evansj/me/tmp/ \
      java -Xmx20g -Xms20g -jar -Dconfig.file=hpc.conf \
      /mnt/isilon/dbhi_bfx/apps/bin/cromwell-36.jar run \
      paired-fastq-to-unmapped-bam.wdl \
      -i paired-fastq-to-unmapped-bam.inputs.json \
      -o generic.google-papi.options.json \
      -m metadata_ubam.json
