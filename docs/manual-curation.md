# Manual trait curation

The goal is for traits with occurence ≥ 10 to have 100% coverage after the manual curation. For the rest of the traits, curate as many as possible.

Before executing the subsequent commands, make sure to set up environment (described in the “Set up environment” section of the main protocol.)

## Extract information about previous mappings
At this step, mappings produced by the pipeline on the previous iteration (including automated and manual) are downloaded to be used to aid the manual curation process.

```bash
# Download the latest eva_clinvar release from FTP
wget -qO- ftp://ftp.ebi.ac.uk/pub/databases/eva/ClinVar/latest/eva_clinvar.txt \
  | cut -f4-5 | sort -u > ${BATCH_ROOT}/trait_mapping/previous_mappings.tsv
```

## Create the final table for manual curation
```bash
python bin/trait_mapping/create_table_for_manual_curation.py \
  --traits-for-curation ${BATCH_ROOT}/trait_mapping/traits_requiring_curation.tsv \
  --previous-mappings ${BATCH_ROOT}/trait_mapping/previous_mappings.tsv \
  --output ${BATCH_ROOT}/trait_mapping/table_for_manual_curation.tsv
```

## Sort and export to Google Sheets
Note that the number of columns in the output table is limited to 50, because only a few traits have that many mappings, and in virtually all cases these extra mappings are not meaningful. However, having a very large table degrades the performance of Google Sheets substantially.

```bash
cut -f-50 ${BATCH_ROOT}/trait_mapping/table_for_manual_curation.tsv \
  | sort -t$'\t' -k2,2rn > ${BATCH_ROOT}/trait_mapping/google_sheets_table.tsv
```

Create a Google Sheets table by duplicating a [template](https://docs.google.com/spreadsheets/d/1PyDzRs3bO1klvvSv9XuHmx-x7nqZ0UAGeS6aV2SQ2Yg/edit?usp=sharing). Paste the contents of `google_sheets_table.tsv` file into it, starting with column H “ClinVar label”. Example of a table fully populated with data can be found [here](https://docs.google.com/spreadsheets/d/1HQ08UQTpS-0sE9MyzdUPO7EihMxDb2e8N14s1BknjVo/edit?usp=sharing)

## Manual curation criteria
Good mappings must be eyeballed to ensure they are actually good. Alternative mappings for medium or low quality mappings can be searched for using OLS. If a mapping can't be found in EFO, look for a mapping to a HP, ORDO, or MONDO trait name. Most HP/ORDO/MONDO terms will also be in EFO but some are not. These can be imported to EFO using the Webulous submission service.

### Criteria to manually evaluate mapping quality
* Exact string for string matches are _good_
* Slight modifications are _good_ e.g. IRAK4 DEFICIENCY → Immunodeficiency due to interleukin-1 receptor-associated kinase-4 deficiency
* Subtype to parent are _good_ e.g ACHROMATOPSIA 3 → Achromatopsia
* Parent to subtype are _bad_ e.g. HEMOCHROMATOSIS → Hemochromatosis type 3
* Familial / congenital represented on only one half are _bad_ e.g. Familial renal glycosuria → Renal glycosuria
* Susceptibility on only one half is _bad_ e.g Alcohol dependence, susceptibility to → alcohol dependence
* Early / late onset on only one half is _bad_ e.g. Alzheimer disease, early-onset → Alzheimer's disease

### Unmapped trait names
Trait names that haven't been automatically mapped against any ontology term can also be searched for using OLS. If a mapping can't be found in EFO, look for a mapping to a HP, ORDO, or MONDO trait name. If these are not already in EFO they should be imported to EFO using the Webulous submission service.

## Curation workflow
Curation should be done by subsequently applying filters to appropriate columns, then making decisions for the traits in the filtered selection.

* 1\. **There is a previously assigned mapping for this trait.** All of these are the decisions that we made in the past, so we trust them (to an extent). Copy and paste previously used mappings into “Mapping to use”. Then review them according to the following steps.
  * 1.1. **The previously assigned mapping is in EFO**
    * 1.1.1. **The previously assigned mapping is in EFO and is exact.** Mark as finished immediately. (It's extremely unlikely that a better mapping could be found).
    * 1.1.2. **The previously assigned mapping is in EFO and IS NOT exact.** Review the mappings to see if a better (more accurate/specific) mapping is available. Then mark as finished.
  * 1.2. **The previously assigned mapping is not contained in EFO.** We need to either find a mapping which is already in EFO, or import these terms into EFO.
    * 1.2.1. **The previously used mapping IS NOT contained in EFO and is exact.** These are good candidates to mark as finished and them import in EFO afterwards. However, quickly check whether there are non-exact matches which are already in EFO are are as good as exact mappings.
      * E. g. if the exact mapping is “erythrocytosis 6, familial” and not in EFO, but there is an inexact mapping “familial erythrocytosis 6” which *is* in EFO, we should use the inexact mapping.
      * If a trait does not have any EFO mappings, it's probably safe to mark it as finished (with subsequent import to EFO).
    * 1.2.2. **The previously assigned mapping IS NOT contained in EFO and IS NOT exact.** Similarly to 1.2.1, attempt to find an acceptable EFO mapping; if not found, use any acceptable mapping (with subsequent import to EFO).
* 2\. **There is no previously assigned mappings for the trait, but exact mappings are available.** Because letter-to-letter matches are extremely likely to be correct, we can use them after eyeballing for correctness.
  * 2.1. **The exact mapping in the EFO.** Mark as finished immediately.
  * 2.2. **The exact mapping IS NOT in the EFO.** Similarly to 1.2.1, attempt to find an acceptable EFO mapping; if not found, use any acceptable mapping (with subsequent import to EFO).
* 3\. **There are no previously used or exact mappings for the trait.** Curate manually as usual.

### Time-saving options
The new manual workflow can be shortened if necessary, while the quality of the results will be _at least as good as for the old workflow_ (because we're reusing the results of previous curations):
* All subsections 1.\* involve review of mappings previously selected by ourselves. Because we trust them (to an extent), this review can be applied not to all mappings, but only to some (selected on a basis of frequency, or just randomly sampled/eyeballed).
* If necessary, section 1 can be skipped completely, i. e. copy-paste previous mappings into “Mapping to use” column, but skip the review.
* Sections 2.2 and 3 can only be applied to some variants (e. g. based on frequency), depending on the time available.

## Entering the curation results

### Adding new mappings
To select a new mapping which does not appear in the list of automatically generated mappings, use the following format: `URL|LABEL|||EFO_STATUS`. Example: `http://www.ebi.ac.uk/efo/EFO_0006329|response to citalopram|||EFO_CURRENT`. The last value can be either `EFO_CURRENT` (trait is present in the latest EFO version available in OLS), or `NOT_CONTAINED` if the term is not contained in the EFO.

### Marking the status of curated terms
The “Status” column has the following acceptable values:
* **DONE** — an acceptable trait contained in EFO has been found for the trait
* **IMPORT** — an acceptable trait has been found from the MONDO/ORDO/HP ontologies which is not contained in EFO and must be imported
* **NEW** — new term must be created in EFO
* **SKIP** — trait is going to be skipped in this iteration, due to being too non-specific, or just having a low frequency
* **UNSURE** — temporary status; traits to be discussed with reviewers/the team

“Comment” field can contain arbitrary additional information.

### Note on spaces and line breaks
Sometimes, especially when copy-pasting information from external sources, a mapping label or URL can contain an additional space symbol (at the beginning or end) or an accidental line break. This causes problems in the downstream processing and must be manually removed. To minimise the occurences of this, Google Sheets template includes a validation formula for the first two columns (“URI of selected mapping” and “Label of selected mapping”). If it detects an extra space symbol or a line break, the cell will be highlighted in red.

## Exporting curation results
Once the manual curation is complete, export the results to a file named `finished_mappings_curation.tsv` and save it to `${BATCH_ROOT}/trait_mapping` directory. This file must consist of three columns from the curation spreadsheet: “ClinVar label”; “URI of selected mapping”; “Label of selected mapping”, in that order. Make sure to only export the mappings which the curator marked as done.

Sometimes “Mapping to use” column may contain newline characters inserted by accident; if present, remove them using a global regexp search in Google Sheets.
 
After that, two files with mappings must be concatenated to a single file to be used as input for the evidence string generation:
* `automated_trait_mappings.tsv`
  + Mappings generated automatically by the trait mapping pipeline and already considered “finished”
* `finished_mappings_curation.tsv`
  + Eyeballed good quality mappings
  + Manually curated medium and low quality mappings
  + New mappings for previously unmapped traits

The resulting file must be named `trait_names_to_ontology_mappings.tsv` and saved to `${BATCH_ROOT}/trait_mapping` directory as well.
