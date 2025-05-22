def get_evaluated_nodes(phenotype, evaluation=True):
    result_list = []
    for node in phenotype:
        if node[0] == "+" and evaluation:
            result_list.append(node[1:])
        elif node[0] == "-" and not evaluation:
            result_list.append(node[1:])
    return result_list
