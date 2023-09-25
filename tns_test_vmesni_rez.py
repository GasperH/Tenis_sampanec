import numpy as np
import tkinter as tk
from tkinter import ttk
import pandas as pd
import os

root = tk.Tk()
root.title("Sampanec")
my_notebook = ttk.Notebook(root)
my_notebook.grid(row = 0, column = 0)
my_frame1 = ttk.Frame(my_notebook)
my_frame2 = ttk.Frame(my_notebook)

my_frame3 = ttk.Frame(my_notebook)
my_notebook.add(my_frame1, text = "Generacija kol")
my_notebook.add(my_frame2, text = "Razpored")
my_notebook.add(my_frame3, text = "Koncni razpored")
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
    #print(stevilo_igralcev)
    global preveliko_st_kol
    global ni_deljivo_s_stiri
    preveliko_st_kol = False
    ni_deljivo_s_stiri = False
    
    if ((st_igralcev/4).is_integer()) == False:
        tk.messagebox.showinfo(title="Warning", message="Število igralcev ni deljivo s 4.")
        ni_deljivo_s_stiri = True
    
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
                    preveliko_st_kol = True
                
                else:
                    pol_dol_nabora = len(nabor)//2
                    a = nabor[np.random.randint(pol_dol_nabora)]
                    b = nabor[np.random.randint(pol_dol_nabora)]
                    
                    if b!=a and (b in poraba[a]) == False:
                        c = nabor[np.random.randint(pol_dol_nabora) + pol_dol_nabora]
                        
                        if c!=a and b!=c and (c in poraba[b]) == False and (c in poraba[a]) == False:
                            d = nabor[np.random.randint(pol_dol_nabora) + pol_dol_nabora]
                            
                            if d!=a and d!=b and d!=c and (d in poraba[a]) == False and (d in poraba[b]) == False and (d in poraba[c]) == False:
                                kola[i].append([a,c,b,d])
                                
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
    global prvic
    global navodilo_prvi_boben
    global navodilo_drugi_boben
    
    if os.path.exists("vmes_razpored.txt"): #pobrise datoteko z razporedom, če slučajno obstaja
        os.remove("vmes_razpored.txt")
    
    try:
        st_kol = int(stevilo_kol.get())
        st_igralcev = int(stevilo_igralcev.get())

        kola = generacija_kol(st_kol, st_igralcev)
                
        if preveliko_st_kol == False and ni_deljivo_s_stiri == False:
        
            if prvic == False:
                for i in range(len(imena_igralcev_entry)):
                    imena_igralcev_entry[i].destroy()
            imena_igralcev_entry = []
            navodilo_prvi_boben = tk.Label(my_frame1, text = "Prvi boben").grid(row = 3, column = 0)
            navodilo_drugi_boben = tk.Label(my_frame1, text = "Drugi boben").grid(row = 3, column = 2)
            
            for i in range(st_igralcev//2): #naredijo se prostori za imena za prvi boben
                imena_igralcev_entry.append(tk.Entry(my_frame1, width = 20))
                imena_igralcev_entry[i].grid(row = 4+2*i, column = 0)
                presledek = tk.Label(my_frame1, text = "").grid(row = 5+2*i, column = 0)
                
            for i in range(st_igralcev//2): #naredijo se prostori za imena za drugi boben
                imena_igralcev_entry.append(tk.Entry(my_frame1, width = 20))
                imena_igralcev_entry[i + st_igralcev//2].grid(row = 4+2*i, column = 2)
                
            for i in range(st_kol):
                with open("vmes_razpored.txt", "a") as f:
                        f.write("\n"+str(i+1) + ". kolo")
                        f.close()
                for j in range(st_igralcev//4):                        
                    with open("vmes_razpored.txt", "a") as f:
                        f.write("\n")
                        f.write('\t'.join(str(kola[i][j])))
                           
            gumb_za_pobrati_imena["state"] = "normal"
            prvic = False
            
    except:
        tk.messagebox.showinfo(title="Warning", message="Vpišite pravilno število kol in igralcev")
        
def shrani_imena_v_spomin():
    global imena_igralcev
    global rezultati_entry
    rezultati_entry = []
    imena_igralcev = []
    
    if os.path.exists("razpored.txt"): #pobrise datoteko z razporedom, če slučajno obstaja
        os.remove("razpored.txt")
    
    for i in range(st_igralcev):
        #imena_igralcev.append(str(i) + ". igralec")
        imena_igralcev.append(imena_igralcev_entry[i].get())    
    koncni_razpored = []
    for i in range(st_kol):
        rezultati_entry.append([])
        koncni_razpored.append([])
        prikaz_imen_kol = ttk.Label(my_frame2, text = str(i+1) + ". kolo").grid(row = i*(st_igralcev//4+2), column = 0)
        with open("razpored.txt", "a") as f:
                f.write("\n"+str(i+1) + ". kolo")
                f.close()
        for j in range(st_igralcev//4):
            rezultati_entry[i].append([])
            koncni_razpored[i].append([])
            for k in range(4):
                koncni_razpored[i][j].append(imena_igralcev[kola[i][j][k]])
                if k == 1:
                    koncni_razpored[i][j].append(":")
            for g in range(2):
                rezultati_entry[i][j].append([])
                rezultati_entry[i][j][g] = tk.Entry(my_frame2, width = 5)
                rezultati_entry[i][j][g].insert(0,0)
                rezultati_entry[i][j][g].grid(row = i*(st_igralcev//4+2)+j+1, column = 2*g+5)
            dvopicje = tk.Label(my_frame2, text = " : ").grid(row = i*(st_igralcev//4+2)+j+1, column = 6)
            for k in range(5):        
                prikaz_imen_igralcev = tk.Label(my_frame2, text = koncni_razpored[i][j][k]).grid(row = i*(st_igralcev//4+2)+j+1, column = k)
            
            with open("razpored.txt", "a") as f:
                f.write("\n")
                f.write('\t'.join(koncni_razpored[i][j]))

    gumb_za_pobrati_imena["state"] = "disabled"
    
def preberi_rezultate_in_sestej():
    global rezultati
    global prvic_sestevam
    global izpis_rezultatov_imena
    global izpis_rezultatov_tocke
    rezultati = []
    try:
        for i in range(st_kol):
            rezultati.append([])
            for j in range(st_igralcev//4):
                rezultati[i].append([])
                for k in range(2):
                    rezultati[i][j].append(int(rezultati_entry[i][j][k].get()))
                    #rezultati[i][j].append(np.random.randint(9))
                    
        igralci_in_st_tock = []    
        [igralci_in_st_tock.append([imena_igralcev[i],0]) for i in range(st_igralcev)]
        
        if prvic_sestevam == False:
            for i in range(st_igralcev):
                izpis_rezultatov_imena[i].destroy()
                izpis_rezultatov_tocke[i].destroy()
        
        izpis_rezultatov_imena = np.empty(st_igralcev, dtype = object)
        izpis_rezultatov_tocke = np.empty(st_igralcev, dtype = object)
    
        
        for i in range(st_kol):
            for j in range(st_igralcev//4):
                for k in range(2):
                    igralci_in_st_tock[kola[i][j][2*k]][1]+=rezultati[i][j][k]
                    igralci_in_st_tock[kola[i][j][2*k+1]][1]+=rezultati[i][j][k]
        
        def takeSecond(elem):
            return elem[1]
    
        igralci_in_st_tock.sort(key= takeSecond, reverse = True)
        izpis_prve_vrstice = ttk.Label(my_frame3, text = "Mesto").grid(row = 0, column = 0)
        izpis_prve_vrstice = ttk.Label(my_frame3, text = "Ime").grid(row = 0, column = 2)
        izpis_prve_vrstice = ttk.Label(my_frame3, text = "Točke").grid(row = 0, column = 4)
        for i in range(len(igralci_in_st_tock)):
            izpis_rezultatov = ttk.Label(my_frame3, text = str(i + 1) + ".").grid(row = i+1, column = 0)
            izpis_rezultatov = ttk.Label(my_frame3, text = "      ").grid(row = i+1, column = 1)
            izpis_rezultatov = ttk.Label(my_frame3, text = igralci_in_st_tock[i][0]).grid(row = i+1, column = 2)
            izpis_rezultatov_imena[i] = ttk.Label(my_frame3, text = igralci_in_st_tock[i][0])
            izpis_rezultatov = ttk.Label(my_frame3, text = "      ").grid(row = i+1, column = 3)
            izpis_rezultatov = ttk.Label(my_frame3, text = igralci_in_st_tock[i][1]).grid(row = i+1, column = 4)
            izpis_rezultatov_tocke[i] = ttk.Label(my_frame3, text = igralci_in_st_tock[i][1])
            
        prvic_sestevam = False
            
    except:
        tk.messagebox.showinfo(title="Warning", message="Pravilno vpišite rezultate")

prvic = True
prvic_sestevam = True

gumb_za_kola = tk.Button(my_frame1, text = "Število kol in igralcev določeno", command = generacija_in_zapis_kol)
gumb_za_kola.grid(row = 2, column = 2)

gumb_za_pobrati_imena = tk.Button(my_frame1, text = "Imena igralcev vpisana", command = shrani_imena_v_spomin)
gumb_za_pobrati_imena.grid(row = 40, column = 3)

gumb_za_prebrati_rezultate = tk.Button(my_frame2, text = "Rezultati vpisani", command = preberi_rezultate_in_sestej)
gumb_za_prebrati_rezultate.grid(row = 0, column = 10)

root.mainloop()