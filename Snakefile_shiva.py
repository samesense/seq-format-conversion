include: "const.py"

def mk_shiva_samples():
    """Return sample to fq pair"""
    d = '/mnt/isilon/helbig_lab/projects/arcus-epi-sym/data/raw/'
    df = pd.read_csv(d + 'MANIFEST.csv')
    crit = df.apply(lambda row: row['sample_name'][:-1]=='EG0081', axis=1)
    ret = {}
    fqs = ['filename', 'filename2']
    for idx, row in df[crit].iterrows():
        ret[row['sample_name']] = [d + row[x] for x in fqs]
    return ret

SAMPLES = mk_shiva_samples()
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
        o = IMAGE + '{image}.log'
    run:
        with open(input.i, 'r') as f:
            datastore = json.load(f)
        digest = datastore['Digest'].replace(':', '\\:')
        img_dest = IMAGE + wildcards.image.split(':')[0] + '@' + digest
        img_src = 'docker\\://' + wildcards.image.replace(':', '\\:')
        #o = output.o.replace(':', '\\:')
        shell('singularity build {img_dest}.simg {img_src} &> "{output}"')

def match_fqs(wc):
    return SAMPLES[wc.sample]

def write_ubam_sh(ubam_script, inputs, options):
    with open(ubam_script, 'w') as fout:
        print('module load singularity', file=fout)
        print("""TMPDIR=/home/evansj/me/tmp/ \\
        java -Xmx20g -Xms20g -jar -Dconfig.file=hpc.conf \\
        /mnt/isilon/dbhi_bfx/apps/bin/cromwell-36.jar run \\
        paired-fastq-to-unmapped-bam.wdl \\
        -i """ + inputs + " -o " + options, file=fout)

# data/interim/ConvertPairedFastQsToUnmappedBamWf/16afb941-2d18-4036-a849-e868df7f895d/call-CreateFoFN/execution/NA12878_unmapped_bam.list
# name w/ sample for future
rule run_ubam:
    input:
        i = IMAGE + 'broadinstitute/gatk:4.1.1.0.log',
        fqs = match_fqs
    output:
        ls = 'data/interim/bam_ls/{sample}.ubam.ls',
        options = DATA + 'interim/tmp_ubam_options/{sample}.ubam.options.json',
        inputs = DATA + 'interim/tmp_ubam_inputs/{sample}.inputs.json',
        script = PWD + 'ubam_{sample}.sh'
    log:
        LOG + 'ubam/{sample}'
    run:
        # mk new inputs
        with open(CONFIG + 'template.options.json') as f:
            dat = json.load(f)
        dat['final_workflow_outputs_dir'] = DATA + 'interim/tmp_ubam_out/' + wildcards.sample
        with open(output.options, 'w') as fout:
            json.dump(dat, fout)

        with open(CONFIG + 'paired-fastq-to-unmapped-bam-template.inputs.json') as f:
            dat = json.load(f)

        dat["ConvertPairedFastQsToUnmappedBamWf.readgroup_name"] = [wildcards.sample]
        dat["ConvertPairedFastQsToUnmappedBamWf.sample_name"] = [wildcards.sample]
        dat["ConvertPairedFastQsToUnmappedBamWf.fastq_1"] = list(input.fqs)[:1]
        dat["ConvertPairedFastQsToUnmappedBamWf.fastq_2"] = list(input.fqs)[1:]
        dat["ConvertPairedFastQsToUnmappedBamWf.ubam_list_name"] = wildcards.sample + '_unmapped_bam'
        dat["ConvertPairedFastQsToUnmappedBamWf.library_name"] = ["Agilent-SureSelect-Clinical-Exome"]
        dat["ConvertPairedFastQsToUnmappedBamWf.platform_unit"] = ["na"]
        # time is not right here
        dat["ConvertPairedFastQsToUnmappedBamWf.run_date"] = ["2016-09-01T02:00:00+0200"]
        dat["ConvertPairedFastQsToUnmappedBamWf.platform_name"] = ["illumina"]
        dat["ConvertPairedFastQsToUnmappedBamWf.sequencing_center"] = ["DGD"]

        with open(output.inputs, 'w') as fout:
            json.dump(dat, fout)

        write_ubam_sh(output.script, output.inputs, output.options)
        shell('sh {output.script} &> {log}')

        # cp bam ls
        bam_ls = glob.glob(DATA + 'interim/tmp_ubam_out/' + wildcards.sample + '/ConvertPairedFastQsToUnmappedBamWf/*/call-CreateFoFN/execution/*.list')
        latest_file = max(bam_ls, key=os.path.getctime)
        shell('cp {latest_file} {output.ls}')

def write_gvcf_sh(script, inputs, options):
    with open(script, 'w') as fout:
        print('module load singularity', file=fout)
        print("""TMPDIR=/home/evansj/me/tmp/ \\
        java -Xmx35g -Xms35g -jar -Dconfig.file=hpc.conf \\
        /mnt/isilon/dbhi_bfx/apps/bin/cromwell-36.jar run \\
        PublicPairedSingleSampleWf_perry.wdl \\
        -i """ + inputs + " -o " + options, file=fout)

# image input
# /mnt/isilon/dbhi_bfx/perry/projects/asif/cromwell_test/wdl/singularity-hpc-test/PublicPairedSingleSampleWf_perry.inputs.json
rule run_gvcf:
    input:
        bams = 'data/interim/bam_ls/{sample}.ubam.ls',
        d1 = IMAGE + 'broadinstitute/genomes-in-the-cloud:2.2.5-1486412288.log',
        d2 = IMAGE + 'python:2.7.16-slim-stretch.log'
    output:
        inputs = DATA + 'interim/tmp_gvcf_input/{sample}.json',
        g = DATA + 'endpoints/variants/{sample}.g.vcf.gz',
        idx = DATA + 'endpoints/variants/{sample}.g.vcf.gz.tbi',
        options = DATA + 'interim/tmp_gvcf_options/{sample}.options.json',
        script = PWD + 'gvcf_{sample}.sh'
    log:
        LOG + 'gvcf/{sample}.log'
    run:
        # mk input
        with open(input.bams) as f:
            bam_files = [line.strip() for line in f]
        sample_name = wildcards.sample
        base_filename = wildcards.sample
        final_gvcf_name = wildcards.sample + '.g.vcf.gz'
        with open('configs/gvcf_template.inputs.json') as f:
            dat = json.load(f)

        dat['PairedEndSingleSampleWorkflow.sample_name'] = sample_name
        dat['PairedEndSingleSampleWorkflow.base_file_name'] = base_filename
        dat['PairedEndSingleSampleWorkflow.final_gvcf_name'] = final_gvcf_name
        dat['PairedEndSingleSampleWorkflow.flowcell_unmapped_bams'] = bam_files
        with open(output.inputs, 'w') as fout:
            json.dump(dat, fout)

        with open(CONFIG + 'template.options.json') as f:
            dat = json.load(f)
        dat['final_workflow_outputs_dir'] = DATA + 'interim/tmp_gvcf_out/' + wildcards.sample
        with open(output.options, 'w') as fout:
            json.dump(dat, fout)

        write_gvcf_sh(output.script, output.inputs, output.options)

        shell('sh {output.script} &> {log}')

        # cp output
        gvcf_ls = glob.glob(DATA + 'interim/tmp_gvcf_out/' + wildcards.sample + '/PairedEndSingleSampleWorkflow/*/call-MergeVCFs/execution/*.gz')[0]
        shell('cp {gvcf_ls} {output.g}')

        gvcf_ls = glob.glob(DATA + 'interim/tmp_gvcf_out/' + wildcards.sample + '/PairedEndSingleSampleWorkflow/*/call-MergeVCFs/execution/*.gz.tbi')[0]
        shell('cp {gvcf_ls} {output.idx}')


rule all_gvcf:
    input:
        expand(DATA + 'endpoints/variants/{sample}.g.vcf.gz', sample=SAMPLES)
