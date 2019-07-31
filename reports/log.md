 snakemake -c  "qsub -V -cwd -l h_vmem={cluster.h_vmem} -l mem_free={cluster.mem_free} -l m_mem_free={cluster.m_mem_free} -pe smp {threads}" --cluster-config cluster-config.yaml --singularity-args "-B /mnt/isilon/:/mnt/isilon/" --use-singularity -s Snakefile_shiva.py -n all_gvcf

 The platform (PL) attribute (illumina-hiseq-2500) 
