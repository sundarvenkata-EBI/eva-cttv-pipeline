from collections import defaultdict
import logging

from eva_cttv_pipeline.evidence_string_generation import utilities

logger = logging.getLogger(__package__)


def process_gene(consequence_type_dict, variant_id, ensembl_gene_id, so_term):
    consequence_type_dict[variant_id].append(ConsequenceType(ensembl_gene_id, SoTerm(so_term)))


def process_consequence_type_file_tsv(snp_2_gene_filepath):
    consequence_type_dict = defaultdict(list)
    one_rs_multiple_genes = set()

    with utilities.open_file(snp_2_gene_filepath, "rt") as snp_2_gene_file:
        for line in snp_2_gene_file:
            line = line.rstrip()
            line_list = line.split("\t")

            if len(line_list) < 6:
                logger.warning('Skip invalid line in snp_2_gene file: {}'.format(line))
                continue

            variant_id = line_list[0]
            ensembl_gene_id = line_list[2]
            so_term = line_list[4]

            if ensembl_gene_id == 'NA':
                logger.warning('Skip line with missing gene ID: {}'.format(line))
                continue

            process_gene(consequence_type_dict, variant_id, ensembl_gene_id, so_term)

    return consequence_type_dict, one_rs_multiple_genes


def process_consequence_type_file(snp_2_gene_file):
    logger.info('Loading mapping rs -> ENSG/SOterms')
    consequence_type_dict, one_rs_multiple_genes = \
        process_consequence_type_file_tsv(snp_2_gene_file)
    logger.info('{} rs->ENSG/SOterms mappings loaded'.format(len(consequence_type_dict)))
    logger.info('{} rsIds with multiple gene associations'.format(len(one_rs_multiple_genes)))
    return consequence_type_dict


class SoTerm(object):

    """
    Represents a sequence ontology term belonging to a consequence type object.
    Holds information on accession and rank.
    """

    so_accession_name_dict = {'transcript_ablation': 1893,
                              'splice_donor_variant': 1575,
                              'splice_acceptor_variant': 1574,
                              'stop_gained': 1587,
                              'frameshift_variant': 1589,
                              'stop_lost': 1578,
                              'initiator_codon_variant': 1582,
                              'inframe_insertion': 1821,
                              'inframe_deletion': 1822,
                              'missense_variant': 1583,
                              'transcript_amplification': 1889,
                              'splice_region_variant': 1630,
                              'incomplete_terminal_codon_variant': 1626,
                              'synonymous_variant': 1819,
                              'stop_retained_variant': 1567,
                              'coding_sequence_variant': 1580,
                              'miRNA': 276, 'miRNA_target_site': 934,
                              'mature_miRNA_variant': 1620,
                              '5_prime_UTR_variant': 1623,
                              '3_prime_UTR_variant': 1624,
                              'exon_variant': 1791,
                              'non_coding_transcript_exon_variant': 1792,
                              'non_coding_transcript_variant': 1619,
                              'intron_variant': 1627,
                              'NMD_transcript_variant': 1621,
                              'TFBS_ablation': 1895,
                              'TFBS_amplification': 1892,
                              'TF_binding_site_variant': 1782,
                              'regulatory_region_variant': 1566,
                              'regulatory_region_ablation': 1894,
                              'regulatory_region_amplification': 1891,
                              'feature_elongation': 1907,
                              'feature_truncation': 1906,
                              'intergenic_variant': 1628,
                              'lincRNA': 1463,
                              'downstream_gene_variant': 1632,
                              '2KB_downstream_gene_variant': 1632,
                              'upstream_gene_variant': 1631,
                              '2KB_upstream_gene_variant': 1631,
                              'SNV': 1483,
                              'SNP': 694,
                              'RNA_polymerase_promoter': 1203,
                              'CpG_island': 307,
                              'DNAseI_hypersensitive_site': 685,
                              'polypeptide_variation_site': 336,
                              'start_lost': 2012,
                              'protein_altering_variant': 1818,
                              'gene_fusion': 1565,
                              'gene_variant': 1564,
                              'sequence_variant': 1060,
                              'trinucleotide_repeat_microsatellite_feature': 291,
                              'trinucleotide_repeat_expansion': 2165}

    ranked_so_names_list = ['transcript_ablation',
                            'splice_acceptor_variant',
                            'splice_donor_variant',
                            'stop_gained',
                            'frameshift_variant',
                            'stop_lost',
                            'initiator_codon_variant',
                            'transcript_amplification',
                            'inframe_insertion',
                            'inframe_deletion',
                            'missense_variant',
                            'splice_region_variant',
                            'incomplete_terminal_codon_variant',
                            'stop_retained_variant',
                            'synonymous_variant',
                            'coding_sequence_variant',
                            'mature_miRNA_variant',
                            '5_prime_UTR_variant',
                            '3_prime_UTR_variant',
                            'non_coding_transcript_exon_variant',
                            'intron_variant',
                            'NMD_transcript_variant',
                            'non_coding_transcript_variant',
                            'upstream_gene_variant',
                            'downstream_gene_variant',
                            'TFBS_ablation',
                            'TFBS_amplification',
                            'TF_binding_site_variant',
                            'regulatory_region_ablation',
                            'regulatory_region_amplification',
                            'regulatory_region_variant',
                            'feature_elongation',
                            'feature_truncation',
                            'intergenic_variant']

    def __init__(self, so_name):
        self.so_name = so_name
        if so_name in SoTerm.so_accession_name_dict:
            self._so_accession = SoTerm.so_accession_name_dict[so_name]
        else:
            self._so_accession = None

    @property
    def accession(self):
        if self._so_accession is not None:
            accession_number_str = str(self._so_accession)
            return 'SO:' + accession_number_str.rjust(7, '0')
        else:
            return None

    @property
    def rank(self):
        # If So name not in Ensembl's ranked list, return the least severe rank
        if self.so_name not in SoTerm.ranked_so_names_list:
            return len(SoTerm.ranked_so_names_list)
        else:
            return SoTerm.ranked_so_names_list.index(self.so_name)

    def __eq__(self, other):
        return self.accession == other.accession

    def __hash__(self):
        return hash(self._so_accession)


class ConsequenceType:

    """
    Holds information on the type of consequence related to a variation
    with relationship to ensembl gene IDs and SO terms
    """

    def __init__(self, ensembl_gene_id, so_term):
        self.ensembl_gene_id = ensembl_gene_id
        self.so_term = so_term

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)
