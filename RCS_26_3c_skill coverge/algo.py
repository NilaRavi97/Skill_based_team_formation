import math
import matplotlib.pyplot as plt
import utilities
import random
import Team
import rarestfirst
from src.RCS_26 import tfs
import UtilFunctions
import CBRFunctions


def max_logit_algo(graph1, task1, N, tau):
    """
    :param graph1: graph structure passed as input
    :param task1: task contains set of skills required for the team
    :param N: No of iterations
    :param tau: smoothing factor
    :return: best team
    """
    # 1. Randomly  select  candidate  for  each  role  and  generate  a team T, set Tbest←T
    # skill_experts contains skills - set of experts possess that skill
    # example: '1401': ['12824', '9026', '8210']
    skill_experts = utilities.get_skill_experts_dict(graph1)

    # extracting only the required skills for the task
    # '245': ['1757', '2054', '8638', '13623', '5414', '3744', '12551', '8129']
    # '1240': ['11128', '7880', '4728', '13881', '11329', '1247']
    # '1177': ['1432', '7078']
    # '681': ['3748', '2793', '3463', '14144', '11128', '12449', '7880', '13613', '7744', '8294', '3655', '3800', '2041', '2563', '8970', '13623', '2191', '5596', '14912', '4076', '11977', '13457', '5784', '2141', '7115', '165', '54', '9709', '14169', '12220', '10956', '12110', '2740', '10834', '14087', '2635', '8868', '14792', '11635', '7486', '674', '14415', '13049', '6052', '4003', '4854']
    required_skills = {key: skill_experts[key] for key in skill_experts.keys() & task1}

    # form a random team T (comprising random person for each skill)
    # {'245': '12551', '1240': '11128', '1177': '7078', '681': '7744'}
    random_team = {key: random.choice(required_skills[key]) for key in required_skills.keys()}
    print("random team T", random_team)

    # team members
    # ['12551','11128','7078','7744']
    T = list(random_team.values())
    print("random team T members", T)

    # assign list value to set
    # teamT = Team()
    # for i in T:
    # teamT.experts.add(i)

    # setting the randomly selected team as the best team.
    Tbest = T
    iterations = []
    costs = []
    for i in range(1, N):
        iterations.append(i)
        # 2. calculate the cost of the randomly selected team T
        costT = cost(T, graph1)

        # Randomly select a role, and replace it with a randomly selected alternative candidate, get a new teamT′
        random_skill = random.choice(list(random_team))
        print('picking random skill from Team T', random_skill)
        # find an random person for the random skill
        random_person = random.choice(required_skills[random_skill])
        print('picking random person for the random skill', random_person)

        random_team.update({random_skill: random_person})
        print('New team T"', random_team)
        T_dash = list(random_team.values())
        print('New team T" members', T_dash)

        # assign list value to set
        # teamTd = Team()
        # for i in T_dash:
        # teamTd.experts.add(i)

        # 3. calculate the cost of the newly selected team T"
        costTd = cost(T_dash, graph1)

        # calculate the probability
        prob = probability(costT, costTd, tau)
        r = random.uniform(0, 1)

        if r <= prob:
            T = T_dash
            if cost(T, graph1) < cost(Tbest, graph1):
                Tbest = T

        costs.append(cost(Tbest, graph1))

    #return Tbest, cost(Tbest, graph1), iterations, costs
    return Tbest, cost(Tbest, graph1)


def probability(costT, costTd, tau):
    try:
        vt = math.exp(-costT / tau)
    except OverflowError:
        vt = math.inf if costT < 0 else 0
    try:
        vtd = math.exp(-costTd / tau)
    except OverflowError:
        vtd = math.inf if costTd < 0 else 0
    if max(vt, vtd) != 0:
        prob = vtd / max(vt, vtd)
    else:
        prob = 1
    return prob


def cost(team, graph1):
    return Team.diameter(team, graph1)


if __name__ == "__main__":
    import networkx as nx

    # reading the graph file
    graph = nx.read_gml("dblp.gml")
    print(graph)
    # skills required for the task
    # task = ["1240", "1177", "245", "681"]

    '''final_team, team_cost, it, cos = max_logit_algo(graph, task, 100, 0.05)
    print('iteration', it)
    print('cost', cos)

    plt.plot(it, cos)
    plt.xlabel('iterations')
    plt.ylabel('calculated costs')

    # show the plt
    plt.show()

    print('Team formed for the given task - Max Logit')
    print(final_team)
    print('Cost of the team')
    print(team_cost)

    team_list = utilities.get_author_name_from_label(graph, final_team)
    print('Final team list', team_list)

    team_r, team_cost_r = rarestfirst.rarestfirst(graph, task)
    print('Team formed for the given task - rarest first')
    print(team_r)
    print('Cost of the team')
    print(team_cost_r)

    team_r = str(team_r)
    tlist = team_r.split(":")
    team_list1 = utilities.get_author_name_from_label(graph, tlist)
    print('Final team list', team_list1)
'''
    # case based reasoning
    global df_a_p, df_p_s, df_a_s, df_skill, df_author, \
        query_skills, dict_a_s, case_base

    #UtilFunctions.print_header("Load data and transform")
    df_a_p, df_p_s, df_a_s, df_skill, df_author = UtilFunctions.read_data()

    #UtilFunctions.print_header("author & publication")
    df_a_p_transformed, dict_p_a = UtilFunctions.transform_data(df_a_p, 'Publication')

    #UtilFunctions.print_header("publication & skill")
    UtilFunctions.drop_null_value(df_p_s, 'Skill')
    df_p_s_transformed, dict_p_s = UtilFunctions.transform_data(df_p_s, 'Skill')

    #UtilFunctions.print_header("author & skill")
    df_a_s_transformed, dict_a_s = UtilFunctions.transform_data(df_a_s, 'Skill')

    # Case base creation
    #UtilFunctions.print_header("Creating knowledge base")
    case_base = CBRFunctions.create_knowledge_base(dict_p_s, dict_p_a)

    # Problem description
    #UtilFunctions.print_header("Query skills")

    #task_skills = ['2770', '4481']
    # task_skill as set of ID

    # Initialize an empty set to store the unique skills
    skills_set = set()

    # Iterate through the nodes in the graph
    for node in graph.nodes():
        # Check if the node has a 'skills' attribute
        if 'skills' in graph.nodes[node]:
            # Split the skills string into a list of individual skills
            skills = graph.nodes[node]['skills'].split(',')
            # Add the skills to the skills set
            skills_set.update(skills)

    # Convert the set to a list
    unique_skills = list(skills_set)
    print(unique_skills)
    # 2493
    print(len(unique_skills))

    import random
    import matplotlib.pyplot as plt
    import time

    # A function that takes the number of skills and returns the cost using the max-logit algorithm
    def calculate_cost(selected_skills):
        # max-logit algorithm goes here
        final_team, team_cost = max_logit_algo(graph, selected_skills, 100, 0.05)

        #team_r, team_cost_r = rarestfirst.rarestfirst(graph, selected_skills)

        team_tfs, leader_cost = tfs.tfs(graph, selected_skills, 1, 1)

        query_skills = CBRFunctions.problem_description(selected_skills, df_skill)
        final_team_cbr = CBRFunctions.solve_problem_cbr(query_skills, case_base, dict_a_s, df_a_p_transformed, dict_p_s,
                                                    df_author)

        return final_team, team_tfs, final_team_cbr

    # A list to store the number of skills
    x_values = []
    # A list to store the average cost of 50 tasks with each number of skills
    y_values = []
    y_values_r = []
    y_values_tfs= []
    # A list to store the execution time of each algorithm
    y_values_max_logit = []
    y_values_rarest_first = []
    y_values_tfs = []
    y_values_cbr = []

    # Iterate through the number of skills
    for num_skills in range(4, 12):
        x_values.append(num_skills)
        # Initialize a variable to store the total cost of 50 tasks with this number of skills
        # Perform 50 tasks with this number of skills
        total_max = 0
        total_tfs = 0
        total_cbr = 0
        max_logit_coverage = 0
        tfs_coverage = 0
        cbr_coverage = 0
        for i in range(10):
            selected_skills = random.sample(unique_skills, num_skills)
            #total_cost += calculate_cost(selected_skills)
            #total_cost, total_cost_r,leader_cost = calculate_cost(selected_skills)
            #total_cost1 += total_cost
            #total_cost_r1 += total_cost_r
            #total_cost_leader += leader_cost
            max_logit_team, tfs_team,cbr_team = calculate_cost(selected_skills)
            print('Selected skills', selected_skills)
            # Max Logit
            print('Max Logit team', max_logit_team)
            max_logit_coverage += UtilFunctions.skill_coverage(selected_skills, max_logit_team)
            # Tfs
            tfs_team = str(tfs_team)
            pairs = tfs_team.split(":")
            print('Tfs team', pairs)
            tfs_coverage += UtilFunctions.skill_coverage(selected_skills, pairs)
            print('cbr team', cbr_team)
            cbr_coverage += UtilFunctions.skill_coverage(selected_skills, cbr_team)

        # Calculate the average cost of the 10 tasks
        #average_cost = total_cost1 / 10
        #average_cost_r = total_cost_r1 / 10
        #average_cost_leader = total_cost_leader / 10
        #y_values.append(average_cost)
        #y_values_r.append(average_cost_r)
        #y_values_tfs.append(average_cost_leader)
        average_cov_max_logit = max_logit_coverage/10
        average_cov_tfs = tfs_coverage/10
        average_cov_cbr = cbr_coverage/10
        y_values_max_logit.append(average_cov_max_logit )
        y_values_tfs.append(average_cov_tfs)
        y_values_cbr.append(average_cov_cbr)
    plt.plot(x_values, y_values_max_logit, '-o', label='Max-Logit algorithm')
    #plt.plot(x_values, y_values_rarest_first, '-o', label='Rarest First algorithm')
    plt.plot(x_values, y_values_tfs, '-o', label='TPL closest algorithm')
    plt.plot(x_values, y_values_cbr, '-o', label='Case-based reasoning')
    # Plot the graph
    #plt.plot(x_values, y_values)
    plt.xlabel('Number of Skills')
    plt.ylabel('Skill coverage')
    plt.legend()
    plt.show()


