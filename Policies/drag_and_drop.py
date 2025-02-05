import shutil
import os 

def drag_and_drop(dico) :
    for router in dico.keys():
        og_filename = "i" + router[1:3] + "_startup-config.cfg"
        new_filename = dico[router][1] + "_startup-config.cfg"
        os.rename(og_filename, new_filename)
        
        # CHEMIN A ADAPTER
        chemin = f"./project-files/dynamips/{dico[router][0]}/configs/{new_filename}" 
        
        new_dest = shutil.move(new_filename, chemin)
