nakemake -c  "qsub -V -cwd -l h_vmem={cluster.h_vmem} -l mem_free={cluster.mem_free} -l m_mem_free={cluster.m_mem_free} -pe smp {threads}" --cluster-config cluster-config.yaml --singularity-args "-B /mnt/isilon/:/mnt/isilon/" --use-singularity -s Snakefile_shiva.py -j2 all_gvcf