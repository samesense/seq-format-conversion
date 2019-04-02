import json

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

rule run:
    input:
        i = IMAGE + 'broadinstitute/gatk:4.1.1.0.log'
    shell:
        'sh run.sh'
