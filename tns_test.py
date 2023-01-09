import numpy as np
import tkinter as tk
from tkinter import ttk
import numpy as np
from tkinter import messagebox
import pandas as pd
from os.path import exists
import csv

root = tk.Tk()
root.title("Sampanec")
my_notebook = ttk.Notebook(root)
my_notebook.grid(row = 0, column = 0)
my_frame1 = ttk.Frame(my_notebook)
my_notebook.add(my_frame1, text = "Generacija kol")
my_notebook.grid(row = 0, column = 0)

mapa_za_shranjevanje = "C:\\Users\\LENOVO\\Documents\\GitHub\\Tenis_sampanec"

navodilo_st_kol = tk.Label(my_frame1, text = "Vpiši število kol: ").grid(row = 0,column = 1)
stevilo_kol = tk.Entry(my_frame1, width = 20)
stevilo_kol.grid(row = 0, column = 2)

navodilo_st_igralcev = tk.Label(my_frame1, text = "Vpiši število igralcev: ").grid(row = 1,column = 1)
stevilo_igralcev = tk.Entry(my_frame1, width = 20)
stevilo_igralcev.grid(row = 1, column = 2)

def zapisi(podatki,st_kol, st_igralcev, ime = "test"):
    podatki.insert(0, [st_kol, st_igralcev])
    df = pd.DataFrame(podatki)
    df.to_csv(str(mapa_za_shranjevanje + ime + ".txt"), sep = "\t", encoding='utf-8', index = False, header = False)
    
def zapisi_le_kola(podatki, ime = "generirana_kola"):
    df = pd.DataFrame(podatki)
    df.to_csv(str(ime + ".txt"), sep = "\t", encoding='utf-8', index = False, header = False)

def generacija_kol(st_kol = 3, st_igralcev = 24):
    kola = []
    poraba = []
    breaker = False
    
    if ((st_igralcev/4).is_integer()) == False:
        tk.messagebox.showinfo(title="Warning", message="Število igralcev ni deljivo s 4.")
    
    else: # če število igralcev je deljivo s 4
        [poraba.append([i]) for i in range(st_igralcev)] 
        i = 0
        j = 0
        while i < st_kol: #dokler niso vsa kola definirana
            kola.append([])
            nabor = np.arange(st_igralcev)        
            k = 0
            
            while len(nabor)>0: #dokler niso vsi igralci v kolu izbrani
                j = j+1
                k = k+1            
                
                if k == 150: #če je že velikokrat probal generirati kolo
                    kola = [[]]
                    nabor = np.arange(st_igralcev)
                    poraba = []
                    [poraba.append([i]) for i in range(st_igralcev)]
                    i = 0
                    k = 0
                
                elif j == 50000: #Če je že tolikokrat probal da izgleda ne gre
                    tk.messagebox.showinfo(title="Warning", message="Število kol je preveliko za tako število igralcev.")
                    breaker = True
                
                else:
                    pol_dol_nabora = len(nabor)//2
                    a = nabor[np.random.randint(pol_dol_nabora)]
                    b = nabor[np.random.randint(pol_dol_nabora)]
                    
                    if b!=a and (b in poraba[a]) == False:
                        c = nabor[np.random.randint(pol_dol_nabora) + pol_dol_nabora]
                        
                        if c!=a and b!=c and (c in poraba[b]) == False and (c in poraba[a]) == False:
                            d = nabor[np.random.randint(pol_dol_nabora) + pol_dol_nabora]
                            
                            if d!=a and d!=b and d!=c and (d in poraba[a]) == False and (d in poraba[b]) == False and (d in poraba[c]) == False:
                                kola[i].append([a,b,c,d])
                                
                                nabor = np.delete(nabor, np.argwhere(nabor==a))
                                nabor = np.delete(nabor, np.argwhere(nabor==b))
                                nabor = np.delete(nabor, np.argwhere(nabor==c))
                                nabor = np.delete(nabor, np.argwhere(nabor==d))
                                
                                poraba[a].append(b)
                                poraba[a].append(c)
                                poraba[a].append(d)
                                
                                poraba[b].append(a)
                                poraba[b].append(c)
                                poraba[b].append(d)
                                
                                poraba[c].append(b)
                                poraba[c].append(a)
                                poraba[c].append(d)
                                
                                poraba[d].append(b)
                                poraba[d].append(c)
                                poraba[d].append(a)
                if breaker :
                    break
            
            if breaker :
                kola = []
                break

            
            i = i+1
        return kola        

def generacija_in_zapis_kol():
    global st_kol
    global st_igralcev
    global kola
    global imena_igralcev_entry
    imena_igralcev_entry = []
    st_kol = int(stevilo_kol.get())
    st_igralcev = int(stevilo_igralcev.get())

    kola = generacija_kol(st_kol, st_igralcev)
                
    navodilo_prvi_boben = tk.Label(my_frame1, text = "Prvi boben").grid(row = 3, column = 0)
    navodilo_drugi_boben = tk.Label(my_frame1, text = "Drugi boben").grid(row = 3, column = 2)
    for i in range(st_igralcev//2): #naredijo se prostori za imena za prvi boben
        imena_igralcev_entry.append(tk.Entry(my_frame1, width = 20))
        imena_igralcev_entry[i].grid(row = 4+2*i, column = 0)
        presledek = tk.Label(my_frame1, text = "").grid(row = 5+2*i, column = 0)
        
    for i in range(st_igralcev//2): #naredijo se prostori za imena za drugi boben
        imena_igralcev_entry.append(tk.Entry(my_frame1, width = 20))
        imena_igralcev_entry[i + st_igralcev//2].grid(row = 4+2*i, column = 2)
        

def shrani_imena_v_spomin():
    global imena_igralcev
    imena_igralcev = []
    for i in range(st_igralcev):
        imena_igralcev.append(imena_igralcev_entry[i].get())    
    koncni_razpored = []
    for i in range(st_kol):
        koncni_razpored.append([])
        with open("razpored.txt", "a") as f:
                f.write("\n"+str(i+1) + ". kolo")
                f.close()
        for j in range(st_igralcev//4):
            koncni_razpored[i].append([])
            for k in range(4):
                koncni_razpored[i][j].append(imena_igralcev[kola[i][j][k]])
                if k == 1:
                    koncni_razpored[i][j].append(":")
            
            with open("razpored.txt", "a") as f:
                f.write("\n")
                f.write('\t'.join(koncni_razpored[i][j]))
                
    

gumb_za_kola = tk.Button(my_frame1, text = "Imena igralcev", command = generacija_in_zapis_kol)
gumb_za_kola.grid(row = 2, column = 2)

gumb_za_pobrati_imena = tk.Button(my_frame1, text = "Imena igralcev vpisana", command = shrani_imena_v_spomin)
gumb_za_pobrati_imena.grid(row = 40, column = 3)

root.mainloop()