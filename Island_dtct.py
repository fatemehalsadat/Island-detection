import numpy as np 
import networkx as nx

#data0,data1,data2,data3 = Line,LineStatus,Load_fact,Bus
T_isl = len(data2) #time duration in which islanding is examined
new_dict = dict.fromkeys([i for i in range(0,T_isl)]) #Graphs are saved as dictionaries, keys: hours starting from 0 
Base_graph = nx.Graph([(data0[j,1],data0[j,2]) for j in range(0,len(data0))]) #for j in range(0,len(C))
#for each hour create the network of nodes and edges (bus and line)
D0 = dict.fromkeys([i for i in range(0,T_isl)]) # graph informations: number of segments formed
A_temp = np.zeros((T_isl)) 

for i in range(0,T_isl):                
	C = np.delete(data0,np.where(data1[i,:]<1)[0],axis=0)  #line outages as data1 contains only 0 and 1
	new_dict[i] = nx.Graph([(C[j,1],C[j,2]) for j in range(0,len(C))]) #graphs
	D0[i] = Base_graph.nodes-new_dict[i].nodes  # the lone nodes #new_dict[0]          
for i in range(0,T_isl):   
	A_temp[i] = len(list(nx.connected_components(new_dict[i])))
	
A2 = A_temp.astype(int)
temp = np.max(A_temp).astype(int)
A1 = np.zeros((T_isl,temp))
for i in range(0,T_isl):
	A3 = A2[i]
	for j in range(0,A3):
		A1[i,j] = len(list(nx.connected_components(new_dict[i]))[j])
a_idx = np.argsort(-A1)
A4 = np.take_along_axis(A1, a_idx, axis=1)

U0,U_ind = np.unique(A4,axis=0,return_index=True)
U_i = np.flip(U_ind) #time index of change in segments
U = np.flipud(U0) #segments at each new division
