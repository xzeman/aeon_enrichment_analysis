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


class EnrichmentBehaviourClass:
    def __init__(self, ) -> None:
        self.attractors = list()
        self.attractor_types = list()

    def attractor_types(self):
        return self.attractors_types

    def add_attractor(self, attractor):
        self.attractors.append(attractor)
        self.attractor_types.append(attractor.attractor_type)


class EnrichmentAttractor:
    def __init__(self, attractor_type, enrichment_result, fdr) -> None:
        self.fdr = fdr
        self.attractor_type = attractor_type
        self.goterms = dict()
        self.go_terms_set = set()
        self.mapped_ids = enrichment_result.mapped_ids
        self.unmapped_ids = enrichment_result.unmapped_ids

        for process in enrichment_result.result:
            go_term = EnrichmentGOterm(process)
            if go_term.fdr > self.fdr: continue
            self.goterms[go_term.go_id] = go_term
            self.go_terms_set.add(go_term.go_id)

    def get_goterms_by_set(self, wanted):
        return [self.goterms[go_id] for go_id in wanted if go_id in self.goterms]

    def get_all_goterms(self):
        return self.goterms

    def get_plus_goterms(self):
        return [goterm for goterm in self.goterms if goterm.plus_minus == "+"]

    def get_minus_goterms(self):
        return [goterm for goterm in self.goterms if goterm.plus_minus == "-"]


class EnrichmentGOterm:
    def __init__(self, process) -> None:
        self.go_id = process.get("term", {}).get("id", "")
        self.process_name = process["term"]["label"]

        self.fold_enrichment = process["fold_enrichment"]
        self.fdr = process["fdr"]
        self.expected = process["expected"]
        self.number_in_reference = process["number_in_reference"]
        self.p_value = process["pValue"]
        self.plus_minus = process["plus_minus"]

    def __repr__(self):
        return f"{self.plus_minus}{self.process_name}"

    def __str__(self):
        return f"{self.plus_minus}{self.process_name}"

