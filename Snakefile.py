import json, glob

IMAGE = '/mnt/isilon/dbhi_bfx/perry/projects/asif/images/'

rule digest_image:
    output:
        IMAGE + '{image}.json'
    singularity:
       'docker://luebken/skopeo'
    shell:
        'skopeo inspect docker://{wildcards.image} > "{output}"'

rule build_image:
    input:
        i = IMAGE + '{image}.json'
    output:
        IMAGE + '{image}.log'
    run:
        with open(input.i, 'r') as f:
            datastore = json.load(f)
        digest = datastore['Digest'].replace(':', '\\:')
        img_dest = IMAGE + wildcards.image.split(':')[0] + '\\@' + digest
        img_src = 'docker://' + wildcards.image.replace(':', '\\:')
        shell('singularity build {img_dest}.simg {img_src} > {output}')

# data/interim/ConvertPairedFastQsToUnmappedBamWf/16afb941-2d18-4036-a849-e868df7f895d/call-CreateFoFN/execution/NA12878_unmapped_bam.list
# name w/ sample for future
rule run_ubam:
    input:
        i = IMAGE + 'broadinstitute/gatk:4.1.1.0.log'
    output:
        'data/interim/ubam.ls'
    log:
        'log/ubam'
    run:
        shell('sh run_ubam.sh &> {log}')
        # cp bam ls
        bam_ls = glob.glob('data/interim/ConvertPairedFastQsToUnmappedBamWf/*/call-CreateFoFN/execution/*.list')[0]
        shell('cp {bam_ls} {output}')

# image input
# /mnt/isilon/dbhi_bfx/perry/projects/asif/cromwell_test/wdl/singularity-hpc-test/PublicPairedSingleSampleWf_perry.inputs.json
rule run_gvcf:
    input:
        'data/interim/ubam.ls'
    log:
        'logs/gvcf'
    run:
        # mk input
        shell('sh run_gvcf.sh &> {log}')
        # cp output
