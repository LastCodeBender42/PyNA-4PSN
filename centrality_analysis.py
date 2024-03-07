import sys
import pandas as pd
import networkx as nx
import os
import csv
        
def generate_graph(file_path):
    # Read data and create graph
    df = pd.read_csv(file_path, sep='\t')
    subset_df = df.loc[(df['NodeId1'].str.contains('A:')) & (df['NodeId2'].str.contains('A:'))]
    G = nx.from_pandas_edgelist(subset_df, 'NodeId1', 'NodeId2', create_using=nx.Graph())
    
    eigen_centr = nx.eigenvector_centrality_numpy(G)
    eigendf = pd.DataFrame(list(eigen_centr.items()), columns=['node', 'value'])
    eigendf['norm_val'] = eigendf['value'] / eigendf['value'].max()
    


    output_file_path = os.path.join("eigenvector_centrality.csv")
    eigendf.to_csv(output_file_path, index=False)
  

    close_centr = nx.closeness_centrality(G)
    closedf = pd.DataFrame(list(close_centr.items()), columns=['node', 'value'])
    closedf['norm_val'] = closedf['value'] / closedf['value'].max()
    output_file_path = os.path.join("closeness_centrality.csv")
    closedf.to_csv(output_file_path, index=False)

       
    degr_centr = nx.degree_centrality(G)
    degrdf = pd.DataFrame(list(degr_centr.items()), columns=['node', 'value'])
    degrdf['norm_val'] = degrdf['value'] / degrdf['value'].max()
    output_file_path = os.path.join("degree_centrality.csv")
    degrdf.to_csv(output_file_path, index=False)

         
    betw_centr = nx.betweenness_centrality(G)
    betwdf = pd.DataFrame(list(betw_centr.items()), columns=['node', 'value'])
    betwdf['norm_val'] = betwdf['value'] / betwdf['value'].max()
    output_file_path = os.path.join("betweenness_centrality.csv")
    betwdf.to_csv(output_file_path, index=False)

            
    edge_betw = nx.edge_betweenness_centrality(G)
    edge_betwdf = pd.DataFrame(list(edge_betw.items()), columns=['Pair', 'Edge Value'])
    edge_betwdf[['Node1', 'Node2']] = pd.DataFrame(edge_betwdf['Pair'].tolist(), index=edge_betwdf.index)
    edge_betwdf = edge_betwdf[['Node1', 'Node2', 'Edge Value']]
    edge_betwdf['Norm Value'] = edge_betwdf['Edge Value'] / edge_betwdf['Edge Value'].max()
    output_file_path = os.path.join("edge_betweenness_centrality.csv")
    edge_betwdf.to_csv(output_file_path, index=False)


    output_file = "edge_weights.txt"
    with open("edge_betweenness_centrality.csv", 'r') as csvfile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(csvfile)
        fieldnames = ['weight', 'normal', 'source', 'target']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            source = int(row['Node1'].split(':')[1])
            target = int(row['Node2'].split(':')[1])
            weight = row['Edge Value']
            normal = row['Norm Value']
            writer.writerow({'weight': weight, 'normal': normal, 'source': source, 'target': target})




       

