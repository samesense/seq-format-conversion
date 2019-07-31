module load singularity
TMPDIR=/home/evansj/me/tmp/ \
        java -Xmx35g -Xms35g -jar -Dconfig.file=hpc.conf \
        /mnt/isilon/dbhi_bfx/apps/bin/cromwell-36.jar run \
        PublicPairedSingleSampleWf_perry.wdl \
        -i /mnt/isilon/dbhi_bfx/perry/projects/asif/seq-format-conversion/data/interim/tmp_gvcf_input/EG0081F.json -o /mnt/isilon/dbhi_bfx/perry/projects/asif/seq-format-conversion/data/interim/tmp_gvcf_options/EG0081F.options.json
