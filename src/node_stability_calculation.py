def make_union(attractors):
    unionized = attractors[0]
    for attractor in attractors[1:]:
        unionized = unionized.union(attractor)
    return unionized


def get_stability_percentage(node, stg, attractor):
    variable_on = stg.mk_subspace({node: True})

    on_in_attractor = attractor.intersect(variable_on).vertices().cardinality()
    off_in_attractor = attractor.minus(variable_on).vertices().cardinality()

    return round((on_in_attractor / (on_in_attractor + off_in_attractor)) * 100.0, 2)


def get_stabilities(classifiers, attractors, stg, calculate_unstable=True):
    all_dict = dict()
    unionized_attractors = make_union(attractors)
    for classifier in classifiers:
        subset = unionized_attractors.intersect_colors(classifiers[classifier])
        enclosing = subset.vertices().enclosing_named_subspace()
        unstable_variables = dict()

        if calculate_unstable:
            all_variables = set(stg.network_variable_names())
            stable_variables = set(enclosing)
            to_calculate = all_variables.difference(stable_variables)

            for variable in to_calculate:
                unstable_variables[variable] = get_stability_percentage(variable, stg, subset)

        stability_dict = dict()
        for node in enclosing:
            if enclosing[node] == True:
                stability_dict[node] = 100
            else:
                stability_dict[node] = 0
        if calculate_unstable:
            stability_dict = stability_dict | unstable_variables

        all_dict[classifier] = stability_dict
    return all_dict


def get_stable_nodes(classifiers, attractors, stg, lower_bound=0, upper_bound=100):
    calculate_unstable = True
    if lower_bound == 100 or upper_bound == 0:
        calculate_unstable = False

    stabilities = get_stabilities(classifiers, attractors, stg, calculate_unstable)

    result_dict = dict()
    for one_class in stabilities:
        print(one_class)
        print("  |", end='')

        sub = []
        for node in stabilities[one_class]:
            if stabilities[one_class][node] > upper_bound:
                continue
            if stabilities[one_class][node] < lower_bound:
                continue

            print(node + ": " + str(stabilities[one_class][node]) + "|", end='')
            sub.append(node)

        print()
        result_dict[one_class] = sub
    return result_dict
