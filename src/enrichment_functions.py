import requests


class EnrichmentResult:
    def __init__(self, enrichmentData):
        self.data = enrichmentData

        self.input = self.data["results"]["input_list"]
        self.organism = self.input["organism"]
        self.mapped_ids = self.input["mapped_ids"]
        self.mapped_count = self.input["mapped_count"]
        self.unmapped_ids = self.input["unmapped_ids"]
        self.unmapped_count = self.input["unmapped_count"]
        self.result = self.data["results"]["result"]  # Sorted by FDR


def prepare_list_for_enrichment(nodes):
    as_string = str(nodes)[1:-1]
    as_string = as_string.replace("\'", "")
    return as_string


def prepare_enrichment_result(enrichment):
    if isinstance(enrichment, dict) and 'search' in enrichment and isinstance(enrichment['search'], dict) and 'error' in enrichment['search']:
        return None

    enrichment_result = EnrichmentResult(enrichment)
    return enrichment_result


def get_enrichment(genes_string, organism_id, goterm_type, test_type="FISHER", correction="FDR"):
    input_genes = genes_string
    organism = organism_id
    test_type = test_type   # FISHER, BINOMIAL
    correction = correction # FDR, BONFERRONI, NONE
    # refInputList  <- potential extension
    # refOrganism

    match goterm_type:
        case "MF": data_type = "GO:0003674"
        case "BP": data_type = "GO:0008150"
        case "CC": data_type = "GO:0005575"
        case _:
            print('Wrong goterm_type. Use "MF","BP","CC" instead. Ending get_enrichment function.')
            return

    req_link = f"https://pantherdb.org/services/oai/pantherdb/enrich/overrep?geneInputList={input_genes}&organism={organism}&annotDataSet={data_type}&enrichmentTestType={test_type}&correction={correction}"
    headers = {"Content-Type": "application/json"}
    response = requests.get(req_link, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data

    print("Failed to get data. Ending get_enrichment function.")
    return
