import networkx as nx
import matplotlib.pyplot as plt

def create_graph(file_path):

    G = nx.read_weighted_edgelist(file_path, create_using= nx.DiGraph)
    return G

def plot_graph(graph):

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True)
    weight = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=weight, font_size=8)
    plt.show()

def dijkstra(graph, source):
    # Initialize distances to infinity for all vertices except the source vertex
    distances = {vertex: float('inf') for vertex in graph.nodes}
    distances[source] = 0

    # Initialize paths as empty lists for all vertices except the source
    paths = {vertex: [] for vertex in graph.nodes}
    paths[source] = [source]

    # Set to track visited vertices
    visited = set()

    # Loop to visit all vertices in the graph
    while len(visited) < len(graph.nodes):
        
        current_vertex = None
        smallest_distance = float('inf')

        # Find the unvisited vertex with the smallest distance
        for vertex in distances:
            if vertex not in visited and distances[vertex] < smallest_distance:
                smallest_distance = distances[vertex]
                current_vertex = vertex 
        
        # Exit the loop if there are no more accessible vertices
        if current_vertex is None:
            break
        
        # Add the current vertex to the visited set
        visited.add(current_vertex)

        # Update distances and paths for the neighbors of the current vertex
        for neighbor in graph.neighbors(current_vertex):
            weight = graph[current_vertex][neighbor]['weight']
            distance = distances[current_vertex] + weight

            # Update distance if a shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                paths[neighbor] = paths[current_vertex] + [neighbor] 

    # Display the shortest paths to the destination vertices
    for destination in distances:
        if distances[destination] == float('inf'):
            print(f"There is no path from {source} to {destination}.")
        else:
            print(f"Shortest path from {source} to {destination}: {paths[destination]} with distance {distances[destination]}")




def main():

    text_file = "graph.txt"
    graph = create_graph(text_file)

    source = input("Enter the source vertex: ")
    
    dijkstra(graph, source)
    
    plot_graph(graph)


main()
