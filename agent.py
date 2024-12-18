import mesa
from utils import *





def pick_a_cell_according_to_policy(agent,model):
    """
    This function is used to pick a cell according to the policy
    :param model: the model
    :return: the cell
    """
    pos = agent.pos
    
    # Get altruism variable
    altruism = agent.altruism
    
    empties = [cell[1] for cell in model.grid.coord_iter() if model.grid.is_cell_empty(cell[1])]
    
    selected_cell = (-1, -1)

    if agent.policy not in ["random", "distance", "relevance", "distance_relevance", 
                            "rich_neighborhood", "poor_neighborhood",
                              "minimum_improvement", "maximum_improvement", 
                              "recently_emptied", "historically_emptied", "empty_surrounded", 
                              "similar_neighborhood", "different_neighborhood", "similar_history_cell", "similar_history_neighborhood"]:
        raise Exception("Policy not recognized")

    if agent.policy == "random" and altruism == False:
        # pick a random empty cell
        selected_cell =  model.random.choice(empties)
        
    
    # Add altruism policy:
        
    if agent.altruism:
        empties2overall_happiness = {}
        for cell in empties:
            if is_improving_overall_happiness(model, agent, cell):
                empties2overall_happiness[cell] = 1
    
        if len(empties2overall_happiness) == 0:
            return agent.pos
    
        selected_cell = model.random.choice(list(empties2overall_happiness.keys()))


    if agent.policy == "minimum_improvement" and altruism == False:
        empties2alike_neighbors = {cell: calculate_alike_destination(model, agent, cell) for cell in empties}
        #filter out the keys with value <= 0 (no neighbors of the same type) or <model.homophily (no improvement)
        empties2alike_neighbors_filtered = {cell: 1/(empties2alike_neighbors[cell]) 
                                            for cell in empties 
                                                if empties2alike_neighbors[cell] >= model.homophily} #now in empties2alike_neighbors_filtered we have the number of alike neighbors for each empty cell that have at least model.homophily alike neighbors

        if len(empties2alike_neighbors_filtered) == 0:
            return agent.pos #if there are no cells with at least model.homophily alike neighbors, then the agent stays in the same cell


        #sort the dictionary by value
        empties2alike_neighbors_filtered = dict(sorted(empties2alike_neighbors_filtered.items(), key=lambda item: item[1], reverse=True))

        #pick the first k cells
        empties2alike_neighbors_filtered = dict(list(empties2alike_neighbors_filtered.items())[:model.k])

        #print(empties2alike_neighbors_filtered)
        selected_cell = model.random.choices(list(empties2alike_neighbors_filtered.keys()), weights=empties2alike_neighbors_filtered.values())[0]


    if agent.policy == "maximum_improvement" and altruism == False:
        empties2alike_neighbors = {cell: calculate_alike_destination(model, agent, cell) for cell in empties}
        empties2alike_neighbors_filtered = {cell: empties2alike_neighbors[cell] 
                                            for cell in empties 
                                                if empties2alike_neighbors[cell] >= model.homophily} #now in empties2alike_neighbors_filtered we have the number of alike neighbors for each empty cell that have at least model.homophily alike neighbors
    
        if len(empties2alike_neighbors_filtered) == 0:
            return agent.pos #if there are no cells with at least model.homophily alike neighbors, then the agent stays in the same cell

        #sort the dictionary by value
        empties2alike_neighbors_filtered = dict(sorted(empties2alike_neighbors_filtered.items(), key=lambda item: item[1], reverse=True))

        #pick the first k cells
        empties2alike_neighbors_filtered = dict(list(empties2alike_neighbors_filtered.items())[:model.k])

        selected_cell = model.random.choices(list(empties2alike_neighbors_filtered.keys()), weights=empties2alike_neighbors_filtered.values())[0]



    if agent.policy == "similar_neighborhood" and altruism == False:
        empties2similar_neighborhood = {cell: calculate_alike_destination_richness(model, agent, cell) for cell in empties}

        #sort the dictionary by value
        empties2similar_neighborhood = dict(sorted(empties2similar_neighborhood.items(), key=lambda item: item[1], reverse=True))

        #pick the first k cells
        empties2similar_neighborhood = dict(list(empties2similar_neighborhood.items())[:model.k])


        selected_cell = model.random.choices(list(empties2similar_neighborhood.keys()), weights=empties2similar_neighborhood.values())[0]


    if agent.policy == "different_neighborhood" and altruism == False:
        empties2different_neighborhood = {cell: calculate_different_destination_richness(model, agent, cell) for cell in empties}

        #sort the dictionary by value
        empties2different_neighborhood = dict(sorted(empties2different_neighborhood.items(), key=lambda item: item[1], reverse=True))

        #pick the first k cells
        empties2different_neighborhood = dict(list(empties2different_neighborhood.items())[:model.k])


        selected_cell = model.random.choices(list(empties2different_neighborhood.keys()), weights=empties2different_neighborhood.values())[0]








    
    if agent.policy == "distance_relevance" and altruism == False:
        empties2distances = {cell: 1/(get_distance(pos, cell)**2) for cell in empties}
        empties2relevances = {cell: (model.relevance_matrix[cell[0]][cell[1]])**2 for cell in empties}
        empties2distances_relevances = {cell: empties2distances[cell] * empties2relevances[cell] for cell in empties}
        
        #sort the dictionary by value
        empties2distances_relevances = dict(sorted(empties2distances_relevances.items(), key=lambda item: item[1], reverse=True))

        #pick the first k cells
        empties2distances_relevances = dict(list(empties2distances_relevances.items())[:model.k])


        selected_cell = model.random.choices(list(empties2distances_relevances.keys()), weights=empties2distances_relevances.values())[0]


    if agent.policy == "rich_neighborhood" and altruism == False:
        empties2richness = {cell: calculate_neighborhood_richness(model, cell) for cell in empties}

        #sort the dictionary by value
        empties2richness = dict(sorted(empties2richness.items(), key=lambda item: item[1], reverse=True))

        #pick the first k cells
        empties2richness = dict(list(empties2richness.items())[:model.k])

        
        selected_cell = model.random.choices(list(empties2richness.keys()), weights=empties2richness.values())[0]


    

        

    if agent.policy == "recently_emptied" and altruism == False:
        empties2emptiness_time_inv = {cell: 1/calculate_cell_emptiness_time(model, cell) for cell in empties }

        #sort the dictionary by value
        empties2emptiness_time_inv = dict(sorted(empties2emptiness_time_inv.items(), key=lambda item: item[1], reverse=True))

        #pick the first k cells
        empties2emptiness_time_inv = dict(list(empties2emptiness_time_inv.items())[:model.k])

        selected_cell = model.random.choices(list(empties2emptiness_time_inv.keys()), weights=empties2emptiness_time_inv.values())[0]

    if agent.policy == "historically_emptied" and altruism == False:
        empties2emptiness_time = {cell: calculate_cell_emptiness_time(model, cell) for cell in empties}


        #sort the dictionary by value
        empties2emptiness_time = dict(sorted(empties2emptiness_time.items(), key=lambda item: item[1], reverse=True))

        #pick the first k cells
        empties2emptiness_time = dict(list(empties2emptiness_time.items())[:model.k])

      
        selected_cell = model.random.choices(list(empties2emptiness_time.keys()), weights=empties2emptiness_time.values())[0]

    if agent.policy == "empty_surrounded" and altruism == False:
        empties2empties = {cell: calculate_empty_surrounded(model, cell) for cell in empties}

        #sort the dictionary by value
        empties2empties = dict(sorted(empties2empties.items(), key=lambda item: item[1], reverse=True))

        #pick the first k cells
        empties2empties = dict(list(empties2empties.items())[:model.k])


        selected_cell = model.random.choices(list(empties2empties.keys()), weights=empties2empties.values())[0]
        
    if agent.policy == "similar_history_cell" and altruism == False:
        empties2similar_history_cell = {cell: calculate_similarity_history_cell(model, agent, cell) for cell in empties}

        #sort the dictionary by value
        empties2similar_history_cell = dict(sorted(empties2similar_history_cell.items(), key=lambda item: item[1], reverse=True))

        #pick the first k cells
        empties2similar_history_cell = dict(list(empties2similar_history_cell.items())[:model.k])

        selected_cell = model.random.choices(list(empties2similar_history_cell.keys()), weights=empties2similar_history_cell.values())[0]
    
    if agent.policy == "similar_history_neighborhood" and altruism == False:
        empties2similar_history_cell = {cell: calculate_similarity_history_neighborhood(model, agent, cell) for cell in empties}

        #sort the dictionary by value
        empties2similar_history_cell = dict(sorted(empties2similar_history_cell.items(), key=lambda item: item[1], reverse=True))

        #pick the first k cells
        empties2similar_history_cell = dict(list(empties2similar_history_cell.items())[:model.k])

        selected_cell = model.random.choices(list(empties2similar_history_cell.keys()), weights=empties2similar_history_cell.values())[0]

    return selected_cell





class SchellingAgent(mesa.Agent):
    """
    Schelling segregation agent
    """

    def __init__(self, id, pos, model, agent_type, income, agent_policy, altruism = False):
        super().__init__(id, model)
        self.pos = pos
        self.type = agent_type
        self.policy = agent_policy
        self.income = income
        self.altruism = altruism

    def step(self):
        similar = sum(1 for neighbor in self.model.grid.iter_neighbors(self.pos, moore=True, include_center=False) if neighbor.type == self.type)
        # If unhappy, move:
        if similar < self.model.homophily:
            selected_cell = pick_a_cell_according_to_policy(self, self.model)
            if selected_cell != (-1, -1):
                self.model.grid.move_agent(self, selected_cell)
        else:
            self.model.happy += 1
