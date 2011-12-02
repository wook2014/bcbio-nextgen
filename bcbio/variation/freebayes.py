"""Bayesian variant calling with FreeBayes.

http://bioinformatics.bc.edu/marthlab/FreeBayes
"""
import os
import subprocess

from bcbio.utils import file_exists
from bcbio.distributed.transaction import file_transaction
from bcbio.pipeline import log

def run_freebayes(align_bam, ref_file, config, dbsnp=None, region=None,
                  out_file=None):
    """Detect small polymorphisms with FreeBayes.
    """
    log.info("Genotyping with FreeBayes: {0}".format(os.path.basename(align_bam)))
    if out_file is None:
        out_file = "%s-variants.vcf" % os.path.splitext(align_bam)[0]
    if not file_exists(out_file):
        with file_transaction(out_file) as tx_out_file:
            cl = [config["program"].get("freebayes", "freebayes"),
                  "-b", align_bam, "-v", tx_out_file, "-f", ref_file]
            if region:
                cl.extend(["-r", region])
            subprocess.check_call(cl)
    return out_file
