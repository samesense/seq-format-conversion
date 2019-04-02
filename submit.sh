qsub \
    -terse \
    -V \
    -b n \
    -N cromwell_main \
    -wd /mnt/isilon/dbhi_bfx/perry/projects/asif/seq-format-conversion/ \
    -pe smp 2 \
    -l m_mem_free=15g \
    -l h_vmem=15g \
    -l m_mem_free=15g run.sh
