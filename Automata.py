import json
import copy
import networkx as nx 
import matplotlib.pyplot as plt
from graphviz import Source

class Automata:

    def __init__(self, link):
        json_file= open(link,"r")
        self.automata= json.load(json_file)
        json_file.close()

    def printBonito(self):
        auto= self.automata
        print("alfabeto", auto["alphabeto"])
        print("estados:", auto["estados"])
        print("inicial:", auto["e_inicial"])
        print("finales:", auto["e_final"])
        print("transiciones:", auto["transiciones"])
        # for x in auto["estados"]:
        #     print("___________")
        #     print(x,":")
        #     for y in auto["alphabeto"]:
        #         print(y,":")
        #         tmp=[]
        #         for z in auto["transiciones"]:
        #             if z[0]==x and z[2]==y:
        #                 tmp.append(z[1])
        #         print(tmp)
        print("___________")


    def enfa_nfa(self):
        auto=self.automata
        alfa= auto["alphabeto"]
        esta= auto["estados"]
        tran= auto["transiciones"]

        #crear una copia del automata
        res= copy.deepcopy(auto)

        #quitar epsilon
        res["alphabeto"].remove("$")
        #quitar todas las transiciones
        res["transiciones"].clear()

        #volver a guardar las transacciones que no contengan epsilon
        for x in tran:
            if x[2] != "$":
                res["transiciones"].append(x)

        
        # declaramos las transiciones
        for al in alfa:
            for es in esta:
                for tr in tran:
                    #comprueba epsilon del estado tr
                    if tr[0] == es and tr[2]=="$":
                        act= tr[1]
                        for tr1 in tran:
                            # comprueba si el epsilon de tr tiene conexion por al 
                            if tr1[0]==act and tr1[2]==al:
                                act2= tr1[1]
                                for tr2 in tran:
                                    # comprieba si la conexion por al de tr1 tiene epsilon
                                    if act2 == tr2[0] and tr2[2]=="$":
                                        temp= [es,tr2[1],al]
                                        if temp not in res["transiciones"]:
                                            res["transiciones"].append(temp)

                                            
        check=[]
        for x in res["transiciones"]:
            if x[2] != "$":
                check.append(x)

        res["transiciones"].clear()
        res["transiciones"]=check
        self.automata= res

    def nfa_dfa(self):
        auto= self.automata
        #variables 

        alfabeto= auto["alphabeto"]
        estados= auto["estados"]
        transiciones= auto["transiciones"]
        inicial= auto["e_inicial"]
        final= auto["e_final"]
        #informacion para el nuevo diccionario saldra de aqui
        # print(inicial)
        dic= [self.creacombi(inicial,auto)]
        # print(self.creacombi(inicial,auto))
        #del=[[estado, [ estado_0 ,estado_1]][]]
        #copia del automata
        res= copy.deepcopy(auto)
        res["estados"].clear()
        res["e_final"].clear()
        res["transiciones"].clear()

        for x in dic:
            for y in x[1]:
                val=True
                for p in dic:
                    if y in p[0]:
                        val=False


                if val:
                    for z in x[1]:
                        if z in estados:
                            val2=True
                            for c in dic:
                                if z in c[0]:
                                    val2=False
                            
                            if val2:
                                #print(z,"aqi")
                                dic.append(self.creacombi(z,auto))
                        else:
                            dic.append(self.creacombi2(z,auto))
            
        self.dup(dic)

        for x in dic:
            cual= x[0][0]
            transi= x[1]
            for y in range(len(res["alphabeto"])):
                temp= [cual,transi[y],res["alphabeto"][y]]
                # res["transiciones"].append(temp)
                if "@" not in temp:
                    res["transiciones"].append(temp)
                    for z in range(2):
                        if temp[z] not in res["estados"]:
                            res["estados"].append(temp[z])

        for x in res["estados"]:
            for y in final:
                if y in x:
                    res["e_final"].append(x)
       
        self.automata=res

    def creacombi(self, letra, auto):
        alfabeto= auto["alphabeto"]
        transiciones= auto["transiciones"]
        # print(alfabeto,transiciones)
        res=[[letra]]
        res2=[]
        for x in alfabeto:
            combi=[]
            prueba=True
            for y in transiciones:
                if y[0] in letra and y[2]==x:
                    combi+=y[1]
                    prueba=False
            if prueba:
                res2.append("@")
            else:
                combi.sort()
                var= self.listToString(combi)
                res2.append(var)

        res.append(res2)
        # print(res)
        return res
    
    def creacombi2(self, letras, auto):
            alfabeto= auto["alphabeto"]
            transiciones= auto["transiciones"]
            res=[[letras]]
            letra= self.str_char(letras)
            res2=[]
            for x in alfabeto:
                combi=[]
                prueba=True
                for y in transiciones:
                    if y[0] in letra and y[2]==x:
                        if y[1] not in combi:
                            combi+=y[1]
                            prueba=False
                if prueba:
                    res2.append("@")
                else:
                    combi.sort()
                    var= self.listToString(combi)
                    res2.append(var)
            res.append(res2)
            return res
    
    def listToString(self, s): 
        str1 = ""  
        for ele in s:  
            str1 += ele   
        return str1  

    def dup(self, x):
        rep=[]
        for y in range(len(x)):
            for z in range(y,len(x)):
                if x[y] == x[z] and y!=z:
                    rep.append(z)
        res=[]
        for o in range(len(x)):
            if o not in rep:
                res.append(x[o])
        
        return res

    def str_char(self, x):
        res=[]
        for y in x:
            res.append(y)
        
        return res
    
    def is_ENFA(self):
        auto=self.automata
        res= copy.deepcopy(auto)
        if  "$" in res["alphabeto"]:
            for x in range(len(res["estados"])):
                if x != "$":
                    letra= res["estados"][x]
                    res["transiciones"].append([letra,letra,"$"])
            
            self.draw("e-nfa.dot")
            self.printBonito()
            self.automata=res
            self.enfa_nfa()
        
            self.draw("nfa.dot")
            self.printBonito()

            self.nfa_dfa()
           
            self.draw("dfa.dot")
            self.printBonito()

            self.dfa_evaluar()
        else:
            self.draw("nfa.dot")
            self.printBonito()

            self.nfa_dfa()
        
            self.draw("dfa.dot")
            self.printBonito()

            self.dfa_evaluar()

    def draw(self,name):
        trans= copy.deepcopy(self.automata["transiciones"])
        label={}
        cuales=[]
        edges=[]
        G= nx.DiGraph()
        print(name,":")
        for x in trans:
            temp= x[0] ,x[1] ,x[2]
            label[(x[0], x[1])] = x[2]

            if x[0] not in cuales:
                cuales.append(x[0])
                G.add_node(x[0])

            if x[1] not in cuales:
                cuales.append(x[1])
                G.add_node(x[1])

            if len(edges)==0:
                edges.append(x)
            else:
                paso=True
                for b in edges:
                    if b[0]== x[0] and b[1]==x[1]:
                        paso=False
                        b[2]=b[2]+self.listToString(x[2])
                if paso:
                    edges.append(x)

        for x in edges:
            G.add_edge(x[0],x[1], label=x[2])

        # print(edges)
        
        pos=nx.spring_layout(G)
        # plt.figure()(G, pos,edges_labels=label,font_color='red')
        path="./respuesta/"+name
        nx.drawing.nx_pydot.write_dot(G,path)
        # plt.show()
        
    def dfa_evaluar(self):
        auto=self.automata
        rep=True
        while rep:
            evaluar= input("Ingrese cadena a probar: ")
            current_state = auto["e_inicial"]
            transition_exists = True

            for char_index in range(len(evaluar)):
                current_char = evaluar[char_index]
                encontro= True
                for actual in range(len(auto["transiciones"])):
                    actual_nodo= auto["transiciones"][actual]
                    
                    if(current_state == actual_nodo[0] and current_char == actual_nodo[2]):
                        current_state= actual_nodo[1]
                        encontro=False
                        break
                if encontro:
                    transition_exists=False
                    break;

            if current_state in auto["e_final"] and transition_exists:
                    print ("Pertenece a L(M)")
            else: 
                print ("No pertenece a L(M)")

            res= input("Desea probar otra cadena? 1.Si 2.No ")
            if res =="2":
                break

        

        
    