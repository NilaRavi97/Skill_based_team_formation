def diameter(team , l_graph) -> float:
    """
            return diameter of graph formed by team
            diam(X) := max{sp_{X}(u,v) | u,v ∈ X}.
            :param self:
            :param l_graph:
            :return:
        """
    import networkx as nx
    t_graph = graph_of_team(team, l_graph)
    # print(list(t_graph.edges))
    if nx.number_of_nodes(t_graph) < 2:
        return 0
    else:
        sp = dict()
        for nd in t_graph.nodes:
            # sp[nd] stores the distance between node nd and all other nodes
            # node - 12276
            # Distance to other nodes - {'12276': 0, '1432': 1, '13881': 1, '12607': 2, '12449': 2, '4973': 2, '3748': 2, '9831': 3, '7875': 3,
            # '4341': 3, '13623': 3, '3359': 3, '7744': 3, '7486': 4, '8129': 4}
            sp[nd] = nx.single_source_dijkstra_path_length(t_graph, nd, weight="cc")
        # The eccentricity of a node v is the maximum distance from v to all other nodes in G.
        e = nx.eccentricity(t_graph, sp=sp)
        # returns the diameter of the graph G
        return round(nx.diameter(t_graph, e), 2)


def graph_of_team(team, l_graph):
    """
            return graph formed by team
            :param l_graph:
            :return:
            """
    nodes = set()
    # nodes.add(self.leader)
    import networkx as nx
    for nd1 in team:
        for nd2 in team:
            if nd1 != nd2:
                # Returns True if G has a path from source to target.
                if nx.has_path(l_graph, nd1, nd2):
                    # Returns the shortest weighted path from source to target in Graph
                    for node in nx.dijkstra_path(l_graph, nd1, nd2):
                        nodes.add(node)
                        # print('node', node)
    # Returns a SubGraph view of the subgraph induced on nodes
    return l_graph.subgraph(nodes).copy()

def sum_distance(team, l_graph, task) -> float:
    """
    returns sum of pairwise skills distance of task
    :param team:
    :param l_graph:
    :param task:
    :return:
    """
    import networkx as nx
    sd = 0
    expert_i = expert_j = ""
    for skill_i in task:
        for skill_j in task:
            if skill_i != skill_j:
                for node in team:
                    exp1_skills = l_graph.nodes[node]["skills"].split(",")
                    if str(skill_i) in exp1_skills:
                        expert_i = node
                    exp2_skills = l_graph.nodes[node]["skills"].split(",")
                    if str(skill_j) in exp2_skills:
                        expert_j = node
                if expert_i in l_graph and expert_j in l_graph and nx.has_path(l_graph, expert_i, expert_j):
                    sd += nx.dijkstra_path_length(l_graph, expert_i, expert_j, weight="cc")
    sd /= 2
    return round(sd, 3)






