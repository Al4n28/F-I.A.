from contextlib import ContextDecorator
from tkinter import *
from tkinter import messagebox
import numpy as np
class UI_Reversi:

    def __init__(self):
        self.Principal_Window = Tk()
        self.Principal_Window.title('Inicio')
        self.Principal_Window.geometry('500x500')
        self.Principal_Window.eval('tk::PlaceWindow . center')
        #self.Principal_Window.iconbitmap('Sin título.ico')
        Label(self.Principal_Window,text='Seleccione color: ').pack()
        # Color 
        # 0: para vacio
        # 1: para BLANCAS
        # -1: para NEGRAS
        #turno=1
        self.Color =IntVar()
        self.Color.set(1)
        #self.Color=turno
        Radiobutton(self.Principal_Window,text='BLANCAS',variable=self.Color,value=1).pack()
        Radiobutton(self.Principal_Window,text='NEGRAS',variable=self.Color,value=-1).pack()
        Label(self.Principal_Window,text='Seleccione color: ').pack()
        # Color del Tema 
        # 0: Normal
        # 1: Crypto
        self.Theme =IntVar()
        self.Theme.set(0)
        Radiobutton(self.Principal_Window,text='NORMAL',variable=self.Theme,value=0).pack()
        Radiobutton(self.Principal_Window,text='CRYPTO',variable=self.Theme,value=1).pack()
        Label(self.Principal_Window,text='Seleccione modo de juego: ').pack()
        self.GameMode =IntVar()
        self.GameMode.set(1) # MODIFICAR AL IMPLEMENTAR IA
        # 0 : 1vsIA
        # 1 : 1vs1 
        Radiobutton(self.Principal_Window,text='1vsIA',variable=self.GameMode,value=0).pack()
        Radiobutton(self.Principal_Window,text='1vs1',variable=self.GameMode,value=1).pack()
        Label(self.Principal_Window,text='Seleccione dificultad: ').pack()
        # SE PUEDEN AGReGAR LAS DIFICULTADES PRINCIPIANTE (0) Y EXPERTO (4)
        self.difficulty = IntVar()
        self.difficulty.set(3)
        difficulty_levels =[('Fácil',1),('Normal',3),('Difícil',5)]
        self.array_difi=[1,6,10]
        for level, num in difficulty_levels:
            Radiobutton(self.Principal_Window,text=level,variable=self.difficulty,value=num).pack()

        Label(self.Principal_Window,text='Seleccione tamaño del tablero: ').pack()
        self.Board_Size =IntVar()
        self.Board_Size.set(6)
        Radiobutton(self.Principal_Window,text='6x6',variable=self.Board_Size,value=6).pack()
        Radiobutton(self.Principal_Window,text='8x8',variable=self.Board_Size,value=8).pack()

        self.winner=None
        self.complete=False

        Button(self.Principal_Window,text='INICIAR JUEGO',command=lambda:self.init_game()).pack(pady=10)

    def init_game(self):
        self.Game_Window = Toplevel()
        self.Game_Window.title("Reversi")
        #self.Game_Window.eval('tk::PlaceWindow . center')
        self.boxes=[]
        
        self.List_Boxes=[0]*(self.Board_Size.get()**2)
        #self.Game_Window.resizable(0, 0)
        #self.Game_Window.columnconfigure(0, weight=1)
        #self.Game_Window.columnconfigure(1, weight=1)
        self.def_pos()
        self.def_edge()
        self.grid_edge()
        #self.Space=PhotoImage(file="space.gif")
        if self.Theme.get() ==0:
            self.B_Piece=PhotoImage(file="black_piece.gif")
            self.W_Piece=PhotoImage(file="white_piece.gif")
            self.Empty_space=PhotoImage(file="wood_space.gif")
            self.Full_Space=PhotoImage(file='full_wood_space.gif')
        else:
            self.B_Piece=PhotoImage(file="blue_piece.gif")
            self.W_Piece=PhotoImage(file="yellow_piece.gif")
            self.Empty_space=PhotoImage(file="empty_space.gif")
            self.Full_Space=PhotoImage(file='full_space.gif')
        # self.juego=aisearch.JuegoGato()

        #Label(self.Game_Window,text='Seleccione color: ', width=80, height=80).grid(row=0,column=0)
        #Label(self.Game_Window,text='').grid(row=8,column=8)
        for i in range(self.Board_Size.get()+2):
            l=[]
            for j in range(self.Board_Size.get()+2):
                if (i*(self.Board_Size.get()+2)+j) in self.Edge_Positions_grid:
                    b=Label(self.Game_Window, width="2", height="2")
                    b.x=(i)
                    b.y=(j)
                    b.grid(row=i,column=j)
                else:
                    if (i==(self.Board_Size.get()+2)/2 and j==(self.Board_Size.get()+2)/2) or (i==((self.Board_Size.get()+2)/2)-1 and j==((self.Board_Size.get()+2)/2)-1):
                        b1=Button(self.Game_Window,image=self.W_Piece,width="80",height="80")
                        self.List_Boxes[(i-1)*(self.Board_Size.get())+(j-1)]=1
                    elif(i==(self.Board_Size.get()+2)/2 and j==((self.Board_Size.get()+2)/2)-1) or (i==((self.Board_Size.get()+2)/2)-1 and j== (self.Board_Size.get()+2)/2):
                        b1=Button(self.Game_Window,image=self.B_Piece,width="80",height="80")
                        self.List_Boxes[(i-1)*(self.Board_Size.get())+(j-1)]=-1
                    else:
                        b1=Button(self.Game_Window,image=self.Empty_space,width="80",height="80")
                    
                    b1.bind("<Button-1>",self.click)
                    b1.x=(i-1)
                    b1.y=(j-1)
                    b1.grid(row=i,column=j)
                    l.append(b1)
            if l:
                self.boxes.append(l)
        Label(self.Game_Window, width="2", height="2",text= "blanca").grid(row=0,column=3)

       
        self.who_is_playing()
        #print(self.Edge_Positions)






    #def MiniMax(self,color):


    #     def max(color):
    #         global contador
    #         contador+=1
    #         if self.difficulty==contador:
    #             return self.

    # def Eval_(self):
    #     self.Eval_Funtion=0
    #     for i in range(len(self.List_Boxes)):
    #         if self.List_Boxes[i] ==0:
    #             continue
    #         if i in self.Corners:
    #             self.Eval_Funtion += self.List_Boxes[i]*3
    #         if i in (self.Top_Egde or self.Bottom_Egde or self.Left_Edge or self.Right_Egde):
    #             self.Eval_Funtion += self.List_Boxes[i]*2
    #         else:
    #             self.Eval_Funtion += self.List_Boxes[i]
    #     print("eval --> ",self.Eval_Funtion)

    # def alfabeta(self,alfa,beta,secuencia,secuencias):
    #     #self.List_boxes_to_play =self.List_Boxes
    #     if self.check_win_condition():
    #         secuencias.append(secuencia.copy())
    #         return [self.Utility_Funtion()]
    #     if self.Color.get()==1:
    #         valor=[-1000,None]
    #     else:
    #         valor=[1000,None]
    #     jugadas_posibles=self.possible_moves(self.Color.get())
    #     print(self.Color.get(),jugadas_posibles,secuencia)
    #     self.printListBoxes()
    #     if not jugadas_posibles:
    #         self.Color.set(self.Color.get()*-1)
    #     else:
    #         for jugada in jugadas_posibles:
    #             self.List_Boxes[jugada]= self.Color.get()
    #             cc_list =self.change_color(jugada,self.Color.get())
    #             self.change_color_list_Boxes(cc_list)
    #             self.Color.set(self.Color.get()*-1)
    #             secuencia.append(jugada)
    #             opcion=self.alfabeta(alfa,beta,secuencia,secuencias)
    #             print(jugada,opcion,valor)
    #             if opcion != None:
    #                 if self.Color.get()==1:
    #                     if opcion[0]>valor[0]:
    #                         valor=[opcion[0],jugada]
    #                         alfa=max(alfa,valor[0])
    #                     if valor[0]>=beta:
    #                         self.List_Boxes[jugada]= 0
    #                         for i in cc_list:
    #                             self.List_Boxes[i]= 0
    #                         self.Color.set(self.Color.get()*-1)
    #                         secuencia.pop()
    #                         break
    #                 else:
    #                     if opcion[0]<valor[0]:
    #                         valor=[opcion[0],jugada]
    #                         beta=min(beta,valor[0])
    #                     if valor[0]<=alfa:
    #                         self.List_Boxes[jugada]= 0
    #                         for i in cc_list:
    #                             self.List_Boxes[i]= 0
    #                         self.Color.set(self.Color.get()*-1)
    #                         secuencia.pop()
    #                         break
    #             self.List_Boxes[jugada]= 0
    #             for i in cc_list:
    #                         self.List_Boxes[i]= 0
    #             self.Color.set(self.Color.get()*-1)
    #             secuencia.pop()
        
            
    #     print(valor)
    #     return valor

    def who_is_playing(self):
        # etiqueta= Label(self.Game_Window,text="piezas Blancas: " + str(self.List_Boxes.count(1)))
        # etiqueta.place(x=0, y=0, width=100, height=20)
        # etiqueta= Label(self.Game_Window,text="piezas Negras: " + str(self.List_Boxes.count(-1)))
        # etiqueta.place(x=100, y=0, width=100, height=20)
        if self.Color.get()==1:
            print('JUEGAN LAS BLANCAS')
            self.printListBoxes()
            print(self.possible_moves(self.Color.get(),self.List_Boxes))     
        else:
            print('JUEGAN LAS NEGRAS')
            self.printListBoxes()
            print(self.possible_moves(self.Color.get(),self.List_Boxes))

    def def_pos(self):
        # 8 posiciones
        self.izq=-1
        self.der=1
        self.arr=-1*self.Board_Size.get()
        self.aba=self.Board_Size.get()
        self.dia=-1*(self.Board_Size.get()+1) #diagonal izquierda arriba
        self.dib=self.Board_Size.get()-1 #diagonal izquierda abajo
        self.dda=-1*(self.Board_Size.get()-1) #diagonal derecha arriba
        self.ddb=self.Board_Size.get()+1 #diagonal derecha abajo

    def grid_edge(self):
        Top_Egde_grid = [i for i in range(1,(self.Board_Size.get()+2)-1)]
        Bottom_Egde_grid = [i for i in range((self.Board_Size.get()+2)*((self.Board_Size.get()+2)-1)+1,((self.Board_Size.get()+2)**2)-1)]
        Left_Edge_grid = [i for i in range((self.Board_Size.get()+2),(self.Board_Size.get()+2)*((self.Board_Size.get()+2)-1),(self.Board_Size.get()+2))]
        Right_Egde_grid = [i for i in range((self.Board_Size.get()+2)+((self.Board_Size.get()+2)-1),((self.Board_Size.get()+2)**2)-1,(self.Board_Size.get()+2))]
        Corners_grid = [0]+[(self.Board_Size.get()+2)-1]+[((self.Board_Size.get()+2)-1)*(self.Board_Size.get()+2)]+[((self.Board_Size.get()+2)**2)-1]
        self.Edge_Positions_grid = Top_Egde_grid+Bottom_Egde_grid+Left_Edge_grid+Right_Egde_grid+Corners_grid
        
    def def_edge(self):
        self.Top_Egde = [i for i in range(1,self.Board_Size.get()-1)]
        self.Bottom_Egde = [i for i in range(self.Board_Size.get()*(self.Board_Size.get()-1)+1,(self.Board_Size.get()**2)-1)]
        self.Left_Edge = [i for i in range(self.Board_Size.get(),self.Board_Size.get()*(self.Board_Size.get()-1),self.Board_Size.get())]
        self.Right_Egde = [i for i in range(self.Board_Size.get()+(self.Board_Size.get()-1),(self.Board_Size.get()**2)-1,self.Board_Size.get())]
        self.Corners = [0]+[self.Board_Size.get()-1]+[(self.Board_Size.get()-1)*self.Board_Size.get()]+[(self.Board_Size.get()**2)-1]
        self.Edge_Positions = self.Corners+self.Top_Egde+self.Left_Edge+self.Right_Egde+self.Bottom_Egde
        
    def Edge_Exceptions(self,pos):
         #LAS 8 EXCEPCIONES
        if pos == 0: #First_Corner
            return [self.der,self.ddb,self.aba]
        if pos == self.Board_Size.get()-1: #Second_Corner 
            return [self.aba,self.dib,self.izq]
        if pos == (self.Board_Size.get()-1)*self.Board_Size.get():#Third_Corner =
            return [self.arr,self.dda,self.der] 
        if pos == (self.Board_Size.get()**2)-1:#Fourth_Corner = 
            return [self.dia,self.arr,self.izq]
        if pos in self.Top_Egde:# Top_Egde = 
            return [self.der,self.ddb,self.aba,self.dib,self.izq]
        if pos in self.Bottom_Egde: #Bottom_Egde = 
            return [self.dia,self.arr,self.dda,self.der,self.izq]
        if pos in self.Left_Edge: #Left_Edge = 
            return [self.arr,self.dda,self.der,self.ddb,self.aba]
        if pos in self.Right_Egde: #Right_Egde = 
            return [self.dia,self.arr,self.aba,self.dib,self.izq]
        else:
            return [self.dia,self.arr,self.dda,self.der,self.ddb,self.aba,self.dib,self.izq]

    def conv_pos(self,pos):
        return[pos//self.Board_Size.get(),pos%self.Board_Size.get()]
    
    def recursive_look(self,pos,dir,color):
        if ((pos+dir)>=0) and ((pos+dir)<=((self.Board_Size.get()**2)-1)):
            if (pos+dir) in self.Edge_Positions:
                if self.List_Boxes[pos+dir]==color:
                    return -1
                elif self.List_Boxes[pos+dir]==0:
                    return pos+dir
                #elif (self.List_Boxes[pos+dir]==-1*color) :}
                elif dir in self.Edge_Exceptions(pos+dir):
                    return self.recursive_look(pos+dir,dir,color)
                else:
                    return -1
            else:
                if self.List_Boxes[pos+dir]==color:
                    return -1
                elif self.List_Boxes[pos+dir]==0:
                    return pos+dir
                #elif (self.List_Boxes[pos+dir]==-1*color) :}
                else:
                    return self.recursive_look(pos+dir,dir,color)
        else:
            #print('OUT OF RANGE LOOK')
            return -1
        
    def possible_moves(self,color,List_Boxes):
        possible_moves_list=[]
        for i in list(np.where(np.array(List_Boxes) == color)[0]):
             for j in self.Edge_Exceptions(i):
                if (i+j) in self.Edge_Positions and j not in self.Edge_Exceptions(i+j):
                    continue
                elif List_Boxes[i+j]==0 or List_Boxes[i+j]==color:#or (i+j) in self.Edge_Positions:
                    continue
                else:
                    pm=self.recursive_look(i+j,j,color)
                    if pm>=0 and pm not in possible_moves_list:
                        possible_moves_list.append(pm)
                    else:
                        continue
        return sorted(possible_moves_list)

    def recursive_color(self,pos,dir,color):
        if ((pos+dir)>=0) and ((pos+dir)<=((self.Board_Size.get()**2)-1)):
            if (pos+dir) in self.Edge_Positions:
                if self.List_Boxes[pos+dir]==0:
                    return [-1]
                elif self.List_Boxes[pos+dir]==color:
                    return [pos]
                elif dir in self.Edge_Exceptions(pos+dir):
                    return [pos]+self.recursive_color(pos+dir,dir,color)
                else:
                    return [-1]#[pos]+self.recursive_color(pos+dir,dir,color)
            else:
                if self.List_Boxes[pos+dir]==0:
                    return [-1]
                elif self.List_Boxes[pos+dir]==color:
                    return [pos]
                else:
                    return [pos]+self.recursive_color(pos+dir,dir,color)
        else:
            #print('OUT OF RANGE COLOR')
            return [-1]
        
    def change_color(self,pos,color,List_Boxes):
        cc_list=[]
        for i in self.Edge_Exceptions(pos):
            
            if List_Boxes[pos+i]==0 or List_Boxes[pos+i]==color:
                continue
            else:
                if i not in self.Edge_Exceptions(pos+i):
                    continue
                else:
                    cc= self.recursive_color(pos+i,i,color)
                    if -1 in cc:
                        continue
                    else:
                        cc_list=cc_list+cc
        #self.change_bottoms(cc_list)
        print(cc_list)
        return cc_list
        
    def change_color_list_Boxes(self,l,List_Boxes):
        
        if len(l)!= 0:
            for i in l:
                if self.Color.get()==1:
                    #self.boxes[self.conv_pos(i)[0]][self.conv_pos(i)[1]].config(image=self.W_Piece)
                    List_Boxes[i]=1
                else:
                    #self.boxes[self.conv_pos(i)[0]][self.conv_pos(i)[1]].config(image=self.B_Piece)
                    List_Boxes[i]=-1
        

    def change_bottoms(self,l):
        if len(l)!= 0:
            for i in l:
                if self.Color.get()==1:
                    self.boxes[self.conv_pos(i)[0]][self.conv_pos(i)[1]].config(image=self.W_Piece)
                    #self.List_Boxes[i]=1
                else:
                    self.boxes[self.conv_pos(i)[0]][self.conv_pos(i)[1]].config(image=self.B_Piece)
                    #self.List_Boxes[i]=-1
    # def check_win_condition(self):
    #     if self.List_Boxes.count(0)==0 or ((len(self.possible_moves(1))==0) and (len(self.possible_moves(-1))==0)):
    #         self.Utility_Funtion()
    #         return True
    #     else:
    #         return False

    # def Utility_Funtion(self):
    #     if self.Count_White>self.Count_Black:
    #         messagebox.showinfo("REVERSI", "GANAN LAS BLANCAS!")
    #         return True
    #     elif self.Count_White<self.Count_Black:
    #         messagebox.showinfo("REVERSI", "GANAN LAS NEGRAS!")
    #         return False
    #     else:
    #         messagebox.showinfo("REVERSI", "EMPATE!")
    #         return 0



    def Utility_Funtion(self):
        if self.Count_White>self.Count_Black:
            return 1
        elif self.Count_White<self.Count_Black:
            return -1
        else:
            return 0

    def check_win_condition(self,color):

        if self.contar == color:
            return True
        else:
            return False
        
        # if self.List_Boxes.count(0)==0 or ((len(self.possible_moves(1))==0) and (len(self.possible_moves(-1))==0)):
        #     self.Utility_Funtion()
        #     return True
        # else:
        #     return False

    # def estado_final(self):
    #     self.evaluar()
    #     if self.winner is not None or self.complete:
    #         return True
    #     else:
    #         return False

    # def evaluar(self):
    #     if 0 not in self.List_Boxes:
    #         self.complete=True
    #     else:
    #         self.complete=False
    #         estado=[]
    #     if int(self.Board_Size.get()) == 6:
    #         for i in [0,6,12,18,24,30]:
    #             estado.append(sum(self.List_Boxes[i:i+6]))
    #         for i in [0,1,2,3,4,5]:
    #             estado.append(self.List_Boxes[i]+self.List_Boxes[i+6]+self.List_Boxes[i+12]+self.List_Boxes[i+18]+self.List_Boxes[i+24]+self.List_Boxes[i+30])
    #             estado.append(self.List_Boxes[0]+self.List_Boxes[7]+self.List_Boxes[14]+self.List_Boxes[21]+self.List_Boxes[28]+self.List_Boxes[35])
    #             estado.append(self.List_Boxes[5]+self.List_Boxes[10]+self.List_Boxes[15]+self.List_Boxes[20]+self.List_Boxes[25]+self.List_Boxes[30])
    #     else:
    #         for i in [0,8,16,24,32,40,48,56]:
    #             estado.append(sum(self.List_Boxes[i:i+8]))
    #         for i in [0,1,2,3,4,5,6,7]:
    #             estado.append(self.List_Boxes[i]+self.List_Boxes[i+8]+self.List_Boxes[i+16]+self.List_Boxes[i+24]+self.List_Boxes[i+32]+self.List_Boxes[i+40]+self.List_Boxes[i+48]+self.List_Boxes[i+56])
    #             estado.append(self.List_Boxes[0]+self.List_Boxes[9]+self.List_Boxes[18]+self.List_Boxes[27]+self.List_Boxes[36]+self.List_Boxes[45]+self.List_Boxes[54]+self.List_Boxes[63])
    #             estado.append(self.List_Boxes[7]+self.List_Boxes[14]+self.List_Boxes[21]+self.List_Boxes[28]+self.List_Boxes[35]+self.List_Boxes[42]+self.List_Boxes[49]+self.List_Boxes[56])
    #     for valor in estado:
    #         if valor==3 or valor==-3:
    #             self.winner=valor//3
    #             return
    #     if self.complete:
    #         self.winner=0
    #     else:
    #         self.winner=None

    def contar(self):
        blanca=self.List_Boxes.count(1)
        negra=self.List_Boxes.count(-1)
        if blanca > negra:
            self.winner.set(1)
            return 1
        else:
            if blanca < negra:
                self.winner.set(-1)
                return -1
            else:
                self.winner.set(0)
                return 0

    def calcular_utilidad(self):
        return self.winner

    def jugar(self,jugada):
        self.List_Boxes[jugada]=self.Color.get()
        #self.Color.set(self.Color.get()*-1)

    def deshacer_jugada(self,jugada,cc_list):       
        self.List_Boxes[jugada]=0
        #self.Color.set(self.Color.get()*-1)

    def cambiar(self,pos):
        print("Entro con", pos)
        aux=self.conv_pos(pos)
        if self.Color.get()==1:
            self.boxes[aux[0]][aux[1]].config(image=self.W_Piece)
            #self.List_Boxes[i]=1
        if self.Color.get()==-1:
            self.boxes[aux[0]][aux[1]].config(image=self.B_Piece)

        # cc_list=self.change_color(pos,self.Color.get())
        # self.change_color_list_Boxes(cc_list)
        # self.change_bottoms(cc_list)
        
        # for i in self.List_Boxes:
        #     aux=self.conv_pos(i)
        #     if self.Color.get()==1:
        #         self.boxes[aux[0]][aux[1]].config(image=self.W_Piece)
        #         #self.List_Boxes[i]=1
        #     if self.Color.get()==-1:
        #         self.boxes[aux[0]][aux[1]].config(image=self.B_Piece)

    def minimax(self,etapa,secuencia,secuencias,contador1,List_Boxes2):
        print("_____________________________________") 
        if self.check_win_condition(self.Color.get()):
            secuencias.append(secuencia.copy())
            #print("aaaaaaa",secuencias)
            return [self.calcular_utilidad()]
        if int(self.Color.get())==1:
            #print("Entra")
            valor=[-1000,None]
        else:
            valor=[1000,None]
        #print(contador)
        if contador1<int(self.difficulty.get()):
            print("calcula las jugadas posibles para ", self.Color.get())
            jugadas_posibles = self.possible_moves(self.Color.get(),List_Boxes2)
            for jugada in jugadas_posibles:
                print("=======================")
                print("llamada con la jugada", jugada, " del turno ", self.Color.get())
                self.jugar(jugada)
                #self.List_Boxes[jugada]= self.Color.get()
                cc_list =self.change_color(jugada,self.Color.get(),List_Boxes2)
                #print("CC",cc_list)
                self.change_color_list_Boxes(cc_list,List_Boxes2)
                self.Color.set(self.Color.get()*-1)

                secuencia.append(jugada)
                print(self.Color.get(),jugadas_posibles,secuencia)
                self.printListBoxes()
                
                opcion=self.minimax(etapa*-1,secuencia,secuencias,contador1+1,List_Boxes2)
                #maximizar
                if etapa==1:
                    if valor[0]<opcion[0]:
                        valor=[opcion[0],jugada]                    
                else:
                #minimizar
                    if valor[0]>opcion[0]:
                        valor=[opcion[0],jugada]      
                self.deshacer_jugada(jugada,cc_list)
                for i in cc_list:
                    List_Boxes2[i]= self.Color.get()
                self.Color.set(self.Color.get()*-1)
                # self.List_Boxes[jugada]= 0
                # self.Color.set(self.Color.get()*-1)
                secuencia.pop()
                print("=======================")
                print("Secuencia:", secuencia)
                print("VALOR1: ",valor)
            #self.cambiar(valor[1])
            print("VALOR[1]", valor[1])     
            return valor
        else:
            contador1=0
            #print("VALOR2: ",valor)
            return valor 
               
    def click(self,event):
        
        if self.List_Boxes[event.widget.x*self.Board_Size.get()+event.widget.y] ==0:
            print('JUGADA ---->  ', event.widget.x*self.Board_Size.get()+event.widget.y)
            if self.Color.get()==1:
                if not self.possible_moves(self.Color.get(),self.List_Boxes):
                    print('BLANCAS NO TIENEN JUGADAS')
                    self.Color.set(-1)
                    self.who_is_playing()
                elif event.widget.x*self.Board_Size.get()+event.widget.y not in self.possible_moves(self.Color.get(),self.List_Boxes):
                    print('JUGADA INVALIDA')
                    print(self.possible_moves(self.Color.get(),self.List_Boxes))# crear metodo para que no calcule de nuevo todo
                elif event.widget.x*self.Board_Size.get()+event.widget.y in self.possible_moves(self.Color.get(),self.List_Boxes):
                    cc_list =self.change_color(event.widget.x*self.Board_Size.get()+event.widget.y,self.Color.get(),self.List_Boxes)
                    self.change_bottoms(cc_list)
                    self.change_color_list_Boxes(cc_list,self.List_Boxes)
                    event.widget['image'] = self.W_Piece
                    self.List_Boxes[event.widget.x*self.Board_Size.get()+event.widget.y]=1
                    self.Color.set(-1)
                    self.who_is_playing()
            #elif self.Color.get()==-1:
            else:
                if not self.possible_moves(self.Color.get(),self.List_Boxes):
                    print('NEGRAS NO TIENEN JUGADAS')
                    self.Color.set(1)
                    self.who_is_playing()
                elif event.widget.x*self.Board_Size.get()+event.widget.y not in self.possible_moves(self.Color.get(),self.List_Boxes):
                    print('JUGADA INVALIDA N')
                    print(self.possible_moves(self.Color.get(),self.List_Boxes))
                elif event.widget.x*self.Board_Size.get()+event.widget.y in self.possible_moves(self.Color.get(),self.List_Boxes):
                    cc_list=self.change_color(event.widget.x*self.Board_Size.get()+event.widget.y,self.Color.get(),self.List_Boxes)
                    self.change_bottoms(cc_list)
                    self.change_color_list_Boxes(cc_list,self.List_Boxes)
                    event.widget['image'] = self.B_Piece
                    self.List_Boxes[event.widget.x*self.Board_Size.get()+event.widget.y]=-1
                    self.Color.set(1)
                    self.who_is_playing()
            self.Count_White = self.List_Boxes.count(1)
            self.Count_Black = self.List_Boxes.count(-1)
            self.check_win_condition(self.Color.get())
            #self.Eval_()
            print("llamada minimax", self.Color.get())
            self.List_Boxes2=self.List_Boxes
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",self.minimax(self.Color.get(),[],[],0,self.List_Boxes2))
            if self.minimax(self.Color.get(),[],[],0,self.List_Boxes2)[1]!=None:
                self.cambiar(self.minimax(self.Color.get(),[],[],0,self.List_Boxes2)[1])
                cc_list=self.change_color(self.minimax(self.Color.get(),[],[],0,self.List_Boxes2)[1],self.Color.get(),self.List_Boxes)
                self.change_bottoms(cc_list)
                self.change_color_list_Boxes(cc_list,self.List_Boxes)
                self.Color.set(self.Color.get()*-1)
            else:
                print("a")

    def printListBoxes(self):
        for i in range(self.Board_Size.get()):
            for j in range(self.Board_Size.get()):
                if self.List_Boxes[i*self.Board_Size.get()+j]>=0:
                    print(' ',end='')
                print(self.List_Boxes[i*self.Board_Size.get()+j],end=' ')
            print()

game= UI_Reversi()
mainloop()
