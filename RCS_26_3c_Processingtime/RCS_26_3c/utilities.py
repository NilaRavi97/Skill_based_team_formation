def get_skill_experts_dict(l_graph) -> dict:
    """
    return skill expert community dictionary for input l_graph
    :param l_graph: pass the graph as input
    :return dict:
    """
    skill_experts = dict()
    for node in l_graph.nodes():
        if len(l_graph.nodes[node]) > 0:
            for skill in l_graph.nodes[node]["skills"].split(","):
                if skill in skill_experts:
                    skill_experts[skill].append(node)
                elif skill not in skill_experts:
                    skill_experts[skill] = list([node])
                else:
                    pass
    return skill_experts


def get_author_name_from_label(graph, fteam) -> list:
    """
        return author name from the given label
        :param graph: pass the graph as input
        :param fteam: list of labels
        :return list with author names
    """
    author_list = list()
    for node in graph.nodes():
        if len(graph.nodes[node]) > 0:
            if node in fteam:
                author_list.append(graph.nodes[node]["name"])
    return author_list

def within_k_nbrs(l_gra, start, k):
    nbrs = {start}
    for _ in range(k):
        nbrs = set((nbr for n in nbrs for nbr in l_gra[n]))
    return nbrs
