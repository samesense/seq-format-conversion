module load singularity
TMPDIR=/home/evansj/me/tmp/ \
      java -Xmx35g -Xms35g -jar -Dconfig.file=hpc.conf \
     /mnt/isilon/dbhi_bfx/apps/bin/cromwell-36.jar run \
     PublicPairedSingleSampleWf_perry.wdl \
     -i PublicPairedSingleSampleWf_perry.inputs.json \
     -o generic.google-papi.options.json \
     -m metadata_gvcf.json
