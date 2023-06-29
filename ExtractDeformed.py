from odbAccess import *
import os
current_directory = os.getcwd()
filename="ODB_FILE_NAME.odb"
odb_path = os.path.join(current_directory, filename)
# Open the ODB file
odb = openOdb(odb_path)
node_set = ' ALL NODES'
node_ids = [342579,342581]

#Extract the Deformed values
keys = []
node_index=[]
node_num = 0
with open('Results.txt','a') as f:
    f.write('node_id'+','+'Step'+','+'Increment=step time'+','+'X_original'+','+'Y_original'+','+'Z_Original'+','+'X_Deformed'+','+'Y_Deformed'+','+'Z_Deformed'+'\n')
while(node_num!=len(node_ids)):
    #with open(file_path,'a') as f:
            #f.write('node id:' + str(node_ids[node_num]) +',')
    for i in odb.steps.keys():
        keys.append(i)         #steps =['Step-1', 'Step-2']
    for step in range(len(keys)):
        frames_data=odb.steps[keys[step]].frames
        #with open(file_path,'a') as f:
                #f.write(keys[step]+',')
        for frame in range(len(frames_data)):
            deformed_obj = frames_data[frame].fieldOutputs['U'].values #the one with len around 60000
            with open('Results.txt','a') as f:
                f.write(str(node_ids[node_num]) +',')
                f.write(keys[step]+','+frames_data[frame].description+',')
            for j in range(len(deformed_obj)):
                if deformed_obj[j].nodeLabel==node_ids[node_num]:
                    node_index.append(j)
                    deformed_values=deformed_obj[node_index[node_num]].data
                    #Extract the original Coordinates
                    assembly = odb.rootAssembly
                    node_sets = assembly.nodeSets[node_set]
                    node = node_sets.nodes[0]
                    original_coordinates = node[node_index[node_num]].coordinates
                    #Extract the Deformed Coordinates
                    with open('Results.txt','a') as f:
                        f.write(str(original_coordinates[0])+','+str(original_coordinates[1])+','+str(original_coordinates[2])+',')
                        f.write(str(deformed_values[0]+original_coordinates[0])+','+str(deformed_values[1]+original_coordinates[1])+','+str(deformed_values[2]+original_coordinates[2])+'\n')
    node_num+=1


odb.close()
