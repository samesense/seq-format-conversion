module load singularity
TMPDIR=/home/evansj/me/tmp/ \
        java -Xmx20g -Xms20g -jar -Dconfig.file=hpc.conf \
        /mnt/isilon/dbhi_bfx/apps/bin/cromwell-36.jar run \
        paired-fastq-to-unmapped-bam.wdl \
        -i /mnt/isilon/dbhi_bfx/perry/projects/asif/seq-format-conversion/data/interim/tmp_ubam_inputs/EG0081F.inputs.json -o /mnt/isilon/dbhi_bfx/perry/projects/asif/seq-format-conversion/data/interim/tmp_ubam_options/EG0081F.ubam.options.json
