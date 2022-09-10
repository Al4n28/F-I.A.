from tkinter import *
from tkinter import messagebox
import numpy as np
import time
from csv import writer

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
        self.Color =IntVar()
        self.Color.set(1)
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
        self.GameMode.set(0) # MODIFICAR AL IMPLEMENTAR IA
        # 0 : 1vsIA
        # 1 : 1vs1 
        Radiobutton(self.Principal_Window,text='1vsIA',variable=self.GameMode,value=0).pack()
        Radiobutton(self.Principal_Window,text='1vs1',variable=self.GameMode,value=1).pack()
        Label(self.Principal_Window,text='Seleccione dificultad: ').pack()
        # SE PUEDEN AGReGAR LAS DIFICULTADES PRINCIPIANTE (0) Y EXPERTO (4)
        self.difficulty = IntVar()
        self.difficulty.set(3) 
        difficulty_levels =[('Principiante',1),('Fácil',2),('Normal',3),('Difícil',5),('Experto',10)]
        for level, num in difficulty_levels:
            Radiobutton(self.Principal_Window,text=level,variable=self.difficulty,value=num).pack()

        Label(self.Principal_Window,text='Seleccione tamaño del tablero: ').pack()
        self.Board_Size =IntVar()
        self.Board_Size.set(6)
        Radiobutton(self.Principal_Window,text='6x6',variable=self.Board_Size,value=6).pack()
        Radiobutton(self.Principal_Window,text='8x8',variable=self.Board_Size,value=8).pack()

        Button(self.Principal_Window,text='INICIAR JUEGO',command=lambda:self.init_game()).pack(pady=10)

    def init_game(self):
        self.Game_Window = Toplevel()
        self.Game_Window.title("Reversi")
        #self.Game_Window.eval('tk::PlaceWindow . center')
        self.boxes=[]
        self.List_Boxes=[0]*(self.Board_Size.get()**2)
        self.depth=0
        self.def_pos()
        self.def_edge()
        self.grid_edge()
        self.Space=PhotoImage(file="space.gif")
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
                    b1.bind("<Enter>",self.select_move_in)
                    b1.bind("<Leave>", self.select_move_out)#(self.conv_pos(i)[0],self.conv_pos(i)[1],self.boxes))
                    b1.x=(i-1)
                    b1.y=(j-1)
                    b1.grid(row=i,column=j)
                    l.append(b1)
            if l:
                self.boxes.append(l)
        self.print_turn_color()
        self.background()
        self.stickers()
        if self.GameMode.get()==0 and self.Color.get()==-1:
            self.Color.set(1)
            self.Board_List =self.List_Boxes
            self.Count_White = self.Board_List.count(1)
            self.Count_Black = self.Board_List.count(-1)
            self.who_plays=self.Color.get()
            self.Expansions = -1
            inicio = time.time()
            sec=[]
            IA_Play=self.alfabeta(self.Color.get(),-1000,1000,[],sec,0)[1]
            #IA_Play=self.minimax(self.Color.get(),[],sec,0)[1]
            fin = time.time()
            self.Time_IA_Thinks=fin-inicio
            print("expansions",self.Expansions)
            print("Time",self.Time_IA_Thinks) 
            with open('bd_IA.csv', 'a', newline='') as f_object:  
                writer_object = writer(f_object)
                writer_object.writerow([self.List_Boxes,IA_Play,self.Expansions,self.Time_IA_Thinks,self.difficulty.get(),1])  
                f_object.close()
            
            print("LA IA JUEGA EN ------> ",IA_Play)
            cc_list =self.change_color_List_Boxes(IA_Play,self.Color.get())
            self.change_bottoms(cc_list)
            #self.change_color_list_Boxes(self.List_Boxes,cc_list)
            self.boxes[self.conv_pos(IA_Play)[0]][self.conv_pos(IA_Play)[1]].image=self.W_Piece
            self.boxes[self.conv_pos(IA_Play)[0]][self.conv_pos(IA_Play)[1]].config(image=self.W_Piece)
            #event.widget['image'] = self.W_Piece
            self.List_Boxes[IA_Play]=1
            self.Color.set(-1)
            self.print_turn_color()

    def minimax(self,Turn_Color,secuencia,secuencias,d): #r1=minimax(juego,1,[],o1)
        self.Expansions +=1
        # self.Board_List =self.List_Boxes
        #     Turn_Color = self.Color
        if self.Test_Final_State():
            secuencias.append(secuencia.copy())
            #self.Expansions +=1
            return [self.Utility_Funtion(self.Color.get())]
        #print('pro: ',self.depth)
        if d >=self.difficulty.get():
        #     print(valor)
            secuencias.append(secuencia.copy())
            #self.Expansions +=1
            return [self.Eval_Funtion(self.Color.get())]
        #if self.Color.get()==1:
        # self.vMax=[-1000,None]
        # #else:
        # self.vMin=[1000,None]  
        if Turn_Color==self.Color.get():
            v=[-1000,None]
        else:
            v=[1000,None]
        jugadas_posibles=self.possible_moves(self.Board_List,Turn_Color)
        # print()
        # self.printListBoxes()
        # print()
        #print(self.Color.get(),jugadas_posibles,secuencia)

        # if not jugadas_posibles:
        #     Turn_Color.set(Turn_Color.get()*-1)
        for jugada in jugadas_posibles:
            #jugadas_posibles.remove(jugada)
            #if len(jugadas_posibles)==1:
                #self.depth +=1
            #print(jugadas_posibles)
            self.Board_List[jugada]= Turn_Color
            cc_list =self.change_color_Board_List(jugada,Turn_Color)
            #self.change_color_list_Boxes(self.Board_List,cc_list)
            self.who_plays*=-1
            # if len(secuencia)+1==self.difficulty.get():
            #     continue
            
            secuencia.append(jugada)
            opcion=self.minimax(Turn_Color*-1,secuencia,secuencias,d+1)
            #self.printListBoxes(self.Board_List)
            #print(jugadas_posibles)
            #print(self.Color.get(),jugadas_posibles,secuencia,d)
            #print(Turn_Color,v,opcion,secuencia, self.Color.get())
            #maximizar
            if Turn_Color==self.Color.get():
                if v[0]<opcion[0]:
                    v=[opcion[0],jugada]
            else:
            #minimizar
                if v[0]>opcion[0]:
                    v=[opcion[0],jugada]
            #print("cc l", cc_list)

            self.Board_List[jugada]= 0
            #cc_list =self.change_color_Board_List(jugada,Turn_Color*-1)
            for i in cc_list:
                self.Board_List[i]= Turn_Color*-1
            #self.printListBoxes(self.Board_List)
            #print(self.Color.get(),jugadas_posibles,secuencia,cc_list)
            self.who_plays*=-1
            secuencia.pop()
        #print("v",v)
        return v

    def alfabeta(self,Turn_Color,alfa,beta,secuencia,secuencias,d): #r1=minimax(juego,1,[],o1)
        # self.Board_List =self.List_Boxes
        #     Turn_Color = self.Color
        self.Expansions +=1
        if self.Test_Final_State():
            secuencias.append(secuencia.copy())
            return [self.Utility_Funtion(self.Color.get())]
        #print('pro: ',self.depth)
        if d >=self.difficulty.get():
        #     print(valor)
            secuencias.append(secuencia.copy())
            #print(secuencia,self.Eval_Funtion(self.Color.get()))
            return [self.Eval_Funtion(self.Color.get())]
        #if self.Color.get()==1:
        # self.vMax=[-1000,None]
        # #else:
        # self.vMin=[1000,None]  
        if Turn_Color==self.Color.get():
            v=[-1000,None]
        else:
            v=[1000,None]
        jugadas_posibles=self.possible_moves(self.Board_List,Turn_Color)
        
        # print()
        # self.printListBoxes()
        # print()
        

        # if not jugadas_posibles:
        #     Turn_Color.set(Turn_Color.get()*-1)
        for jugada in jugadas_posibles:
            
            #jugadas_posibles.remove(jugada)
            #if len(jugadas_posibles)==1:
                #self.depth +=1
            self.Board_List[jugada]= Turn_Color
            cc_list =self.change_color_Board_List(jugada,Turn_Color)
            #self.change_color_list_Boxes(self.Board_List,cc_list)
            self.who_plays*=-1
            # if len(secuencia)+1==self.difficulty.get():
            #     continue
            secuencia.append(jugada)
            
            opcion=self.alfabeta(Turn_Color*-1,alfa,beta,secuencia,secuencias,d+1)
            self.printListBoxes(self.Board_List)
            print(Turn_Color,jugadas_posibles,secuencia,v,opcion)
            #maximizar
            if Turn_Color==self.Color.get():
                if v[0]<opcion[0]:
                    v=[opcion[0],jugada]
                    #self.Expansions +=1
                    alfa=max(alfa,v[0])
                if v[0]>=beta:
                    self.Board_List[jugada]= 0
                    for i in cc_list:
                        self.Board_List[i]= Turn_Color*-1
                    self.who_plays*=-1
                    secuencia.pop()
                    break
            else:
            #minimizar
                if v[0]>opcion[0]:
                    v=[opcion[0],jugada]
                    beta=min(beta,v[0])
                if v[0]<=alfa:
                    #self.Expansions +=1
                    self.Board_List[jugada]= 0
                    for i in cc_list:
                        self.Board_List[i]= Turn_Color*-1
                    self.who_plays*=-1
                    secuencia.pop()
                    break
            #print("cc l", cc_list)
            self.Board_List[jugada]= 0
            for i in cc_list:
                self.Board_List[i]= Turn_Color*-1
            # print("dev")
            # self.printListBoxes()
            # print()
            self.who_plays*=-1
           
            secuencia.pop()
        #print("v",v)
        return v 
    
    def Utility_Funtion(self,Color):
        if self.Count_White>self.Count_Black:
            return 1000*Color
        elif self.Count_White<self.Count_Black:
            return -1000*Color
        else:
            return 0

    def Test_Final_State(self):
        if self.List_Boxes.count(0)==0 or ((len(self.possible_moves(self.List_Boxes,1))==0) and (len(self.possible_moves(self.List_Boxes,-1))==0)):
            return True
        else:
            return False

    def Eval_Funtion(self,Color):
        self.Eval_Num=0
        for i in range(len(self.List_Boxes)):
            if self.List_Boxes[i] ==0:
                continue
            if i in self.Corners:
                self.Eval_Num += self.List_Boxes[i]*3
            if i in (self.Top_Egde or self.Bottom_Egde or self.Left_Edge or self.Right_Egde):
                self.Eval_Num += self.List_Boxes[i]*2
            else:
                self.Eval_Num += self.List_Boxes[i]
        #print(self.Eval_Num)
        return self.Eval_Num*Color
    
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
        
    def possible_moves(self,l,color):
        possible_moves_list=[]
        for i in list(np.where(np.array(l) == color)[0]):
             for j in self.Edge_Exceptions(i):
                if (i+j) in self.Edge_Positions and j not in self.Edge_Exceptions(i+j):
                    continue
                elif l[i+j]==0 or l[i+j]==color:#or (i+j) in self.Edge_Positions:
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
        
    def change_color_List_Boxes(self,pos,color):
        cc_list=[]
        for i in self.Edge_Exceptions(pos):
            if self.List_Boxes[pos+i]==0 or self.List_Boxes[pos+i]==color:
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
        if len(cc_list)!= 0:
            for i in cc_list:
                if self.Color.get()==1:
                    self.List_Boxes[i]=1
                else:
                    self.List_Boxes[i]=-1
        return cc_list

    def change_color_Board_List(self,pos,color):
        cc_list=[]
        for i in self.Edge_Exceptions(pos):
            if self.Board_List[pos+i]==0 or self.Board_List[pos+i]==color:
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
        if len(cc_list)!= 0:
            for i in cc_list:
                if color==1:
                    self.Board_List[i]=1
                else:
                    self.Board_List[i]=-1
        return cc_list

    def change_bottoms(self,l):
        if len(l)!= 0:
            for i in l:
                if self.Color.get()==1:
                    self.boxes[self.conv_pos(i)[0]][self.conv_pos(i)[1]].config(image=self.W_Piece)
                    self.List_Boxes[i]=1
                else:
                    self.boxes[self.conv_pos(i)[0]][self.conv_pos(i)[1]].config(image=self.B_Piece)
                    self.List_Boxes[i]=-1

    def one_vs_one(self,pos_play):
        if self.Color.get()==1:
            if not self.possible_moves(self.List_Boxes,self.Color.get()):
                print('BLANCAS NO TIENEN JUGADAS')
                self.Color.set(-1)
                self.print_turn_color()
            elif pos_play not in self.possible_moves(self.List_Boxes,self.Color.get()):
                print('JUGADA INVALIDA')
                print(self.possible_moves(self.List_Boxes,self.Color.get()))# crear metodo para que no calcule de nuevo todo
            elif pos_play in self.possible_moves(self.List_Boxes,self.Color.get()):
                cc_list =self.change_color_List_Boxes(pos_play,self.Color.get())
                self.change_bottoms(cc_list)
                #self.change_color_list_Boxes(self.List_Boxes,cc_list)
                self.boxes[self.conv_pos(pos_play)[0]][self.conv_pos(pos_play)[1]].image=self.W_Piece
                self.boxes[self.conv_pos(pos_play)[0]][self.conv_pos(pos_play)[1]].config(image=self.W_Piece)
                #event.widget['image'] = self.W_Piece
                self.List_Boxes[pos_play]=1
                self.Color.set(-1)
                self.print_turn_color()
        else:
                if not self.possible_moves(self.List_Boxes,self.Color.get()):
                    print('NEGRAS NO TIENEN JUGADAS')
                    self.Color.set(1)
                    self.print_turn_color()
                elif pos_play not in self.possible_moves(self.List_Boxes,self.Color.get()):
                    print('JUGADA INVALIDA N')
                    print(self.possible_moves(self.List_Boxes,self.Color.get()))
                elif pos_play in self.possible_moves(self.List_Boxes,self.Color.get()):
                    cc_list=self.change_color_List_Boxes(pos_play,self.Color.get())
                    self.change_bottoms(cc_list)
                    #self.change_color_list_Boxes(self.List_Boxes,cc_list)
                    self.boxes[self.conv_pos(pos_play)[0]][self.conv_pos(pos_play)[1]].image=self.B_Piece
                    self.boxes[self.conv_pos(pos_play)[0]][self.conv_pos(pos_play)[1]].config(image=self.B_Piece)
                    #event.widget['image'] = self.B_Piece
                    self.List_Boxes[pos_play]=-1
                    self.Color.set(1)
                    self.print_turn_color()

    def one_vs_IA(self,pos_play):
        if self.Color.get()==1:
            if not self.possible_moves(self.List_Boxes,self.Color.get()):
                print('BLANCAS NO TIENEN JUGADAS')
                self.Color.set(-1)
                self.print_turn_color()
            elif pos_play not in self.possible_moves(self.List_Boxes,self.Color.get()):
                print('JUGADA INVALIDA')
                print(self.possible_moves(self.List_Boxes,self.Color.get()))# crear metodo para que no calcule de nuevo todo
            elif pos_play in self.possible_moves(self.List_Boxes,self.Color.get()):
                cc_list =self.change_color_List_Boxes(pos_play,self.Color.get())
                self.change_bottoms(cc_list)
                #self.change_color_list_Boxes(self.List_Boxes,cc_list)
                self.boxes[self.conv_pos(pos_play)[0]][self.conv_pos(pos_play)[1]].image=self.W_Piece
                self.boxes[self.conv_pos(pos_play)[0]][self.conv_pos(pos_play)[1]].config(image=self.W_Piece)
                #event.widget['image'] = self.W_Piece
                self.List_Boxes[pos_play]=1
                self.Color.set(-1)
                #self.print_turn_color()
            
            self.Board_List =self.List_Boxes
            self.Count_White = self.Board_List.count(1)
            self.Count_Black = self.Board_List.count(-1)
            self.who_plays=self.Color.get()
            self.Expansions = -1
            inicio = time.time()
            sec=[]
            IA_Play=self.alfabeta(self.Color.get(),-1000,1000,[],sec,0)[1]
            #IA_Play=self.minimax(self.Color.get(),[],sec,0)[1]
            fin = time.time()
            self.Time_IA_Thinks=fin-inicio
            print("expansions",self.Expansions)
            print("Time",self.Time_IA_Thinks) 
            with open('bd_IA.csv', 'a', newline='') as f_object:  
                writer_object = writer(f_object)
                writer_object.writerow([self.List_Boxes,IA_Play,self.Expansions,self.Time_IA_Thinks,self.difficulty.get(),-1])  
                f_object.close()
            if not self.possible_moves(self.List_Boxes,self.Color.get()):
                print('IA NO TIENEN JUGADAS')
                self.Color.set(1)
                self.print_turn_color()
            elif IA_Play==None:
                print('IA NO ENCONTRO JUGADAS?')
                self.print_turn_color()
            else:
                print("LA IA JUEGA EN ------> ",IA_Play)
                cc_list =self.change_color_List_Boxes(IA_Play,self.Color.get())
                self.change_bottoms(cc_list)
                #self.change_color_list_Boxes(self.List_Boxes,cc_list)
                self.boxes[self.conv_pos(IA_Play)[0]][self.conv_pos(IA_Play)[1]].image=self.B_Piece
                self.boxes[self.conv_pos(IA_Play)[0]][self.conv_pos(IA_Play)[1]].config(image=self.B_Piece)
                #event.widget['image'] = self.W_Piece
                self.List_Boxes[IA_Play]=-1
                self.Color.set(1)
                self.print_turn_color()
                
        elif self.Color.get()==-1:
            if not self.possible_moves(self.List_Boxes,self.Color.get()):
                print('NEGRAS NO TIENEN JUGADAS')
                self.Color.set(1)
                self.print_turn_color()
            elif pos_play not in self.possible_moves(self.List_Boxes,self.Color.get()):
                print('JUGADA INVALIDA')
                print(self.possible_moves(self.List_Boxes,self.Color.get()))# crear metodo para que no calcule de nuevo todo
            elif pos_play in self.possible_moves(self.List_Boxes,self.Color.get()):
                cc_list =self.change_color_List_Boxes(pos_play,self.Color.get())
                self.change_bottoms(cc_list)
                #self.change_color_list_Boxes(self.List_Boxes,cc_list)
                self.boxes[self.conv_pos(pos_play)[0]][self.conv_pos(pos_play)[1]].image=self.B_Piece
                self.boxes[self.conv_pos(pos_play)[0]][self.conv_pos(pos_play)[1]].config(image=self.B_Piece)
                #event.widget['image'] = self.W_Piece
                self.List_Boxes[pos_play]=-1
                self.Color.set(1)
                #self.print_turn_color()
            self.Board_List =self.List_Boxes
            self.Count_White = self.Board_List.count(1)
            self.Count_Black = self.Board_List.count(-1)
            self.who_plays=self.Color.get()
            self.Expansions = -1
            inicio = time.time()
            sec=[]
            IA_Play=self.alfabeta(self.Color.get(),-1000,1000,[],sec,0)[1]
            #IA_Play=self.minimax(self.Color.get(),[],sec,0)[1]
            fin = time.time()
            self.Time_IA_Thinks=fin-inicio
            print("expansions",self.Expansions)
            print("Time",self.Time_IA_Thinks) 
            with open('bd_IA.csv', 'a', newline='') as f_object:  
                writer_object = writer(f_object)
                writer_object.writerow([self.List_Boxes,IA_Play,self.Expansions,self.Time_IA_Thinks,self.difficulty.get(),1])  
                f_object.close()
            if not self.possible_moves(self.List_Boxes,self.Color.get()) :
                print('IA NO TIENEN JUGADAS')
                self.Color.set(1)
                self.print_turn_color()
            elif IA_Play==None:
                print('IA NO ENCONTRO JUGADAS?')
                self.print_turn_color()
            else:
                print("LA IA JUEGA EN ------> ",IA_Play)
                cc_list =self.change_color_List_Boxes(IA_Play,self.Color.get())
                self.change_bottoms(cc_list)
                #self.change_color_list_Boxes(self.List_Boxes,cc_list)
                self.boxes[self.conv_pos(IA_Play)[0]][self.conv_pos(IA_Play)[1]].image=self.W_Piece
                self.boxes[self.conv_pos(IA_Play)[0]][self.conv_pos(IA_Play)[1]].config(image=self.W_Piece)
                #event.widget['image'] = self.W_Piece
                self.List_Boxes[IA_Play]=1
                self.Color.set(-1)
                self.print_turn_color()
        #print([(i,self.Eval_Funtion(self.Color.get())) for i in sec])

    def click(self,event):
        if self.List_Boxes[event.widget.x*self.Board_Size.get()+event.widget.y] ==0:
            print('JUGADA ---->  ', event.widget.x*self.Board_Size.get()+event.widget.y)
            if self.GameMode.get()==1:
                self.one_vs_one(event.widget.x*self.Board_Size.get()+event.widget.y)
            else:
                self.one_vs_IA(event.widget.x*self.Board_Size.get()+event.widget.y)
            
            self.background()
            self.stickers()
            self.check_win_condition()
            print("Eval: ",self.Eval_Funtion_bar())
            # sec=[]
            # self.Board_List =self.List_Boxes
            # #Turn_Color = self.Color.get()
            # self.who_plays=self.Color.get()
            # #print("color entra minimax",self.Color.get())
            # print("result: ",self.minimax(self.Color.get(),[],sec,0))
           # print(sec)
            

    

    ## ------------------------------------------------------------------------------------------------------------------------------------------
        #                     UI
    def background(self):
        rellenos= Label(self.Game_Window,bg="#E67E22")
        rellenos.place(width=100000, height=35)

        if self.Board_Size.get() == 6:
            rellenoi= Label(self.Game_Window,bg="#E67E22")
            rellenoi.place(x=0, y=550,width=100000, height=500)
            rellenoli= Label(self.Game_Window,bg="#E67E22")
            rellenoli.place(x=0, y=0,width=20, height=10000)
            rellenold= Label(self.Game_Window,bg="#E67E22")
            rellenold.place(x=535, y=0,width=10000, height=10000)
            w = Button (self.Game_Window, text="JUGADA RECOMENDADA")
            w.place(x=200,y=560)
        
        else:
            rellenoi= Label(self.Game_Window,bg="#E67E22")
            rellenoi.place(x=0, y=720,width=100000, height=500)
            rellenoli= Label(self.Game_Window,bg="#E67E22")
            rellenoli.place(x=0, y=0,width=20, height=10000)
            rellenold= Label(self.Game_Window,bg="#E67E22")
            rellenold.place(x=705, y=0,width=10000, height=10000)
            w = Button (self.Game_Window, text="JUGADA RECOMENDADA")
            w.place(x=290,y=730)         

    def stickers(self):
        etiqueta= Label(self.Game_Window,text="piezas Blancas: " + str(self.List_Boxes.count(1)),fg="black")
        etiqueta.place(x=20, y=0, width=100, height=35)
        etiqueta= Label(self.Game_Window,text="piezas Negras: " + str(self.List_Boxes.count(-1)),bg="#E67E22",fg="white")
        etiqueta.place(x=120, y=0, width=100, height=35)
        if self.Color.get()==1:
            if self.Board_Size.get() == 6:
                etiquetaturno= Label(self.Game_Window,text="Turno: BLANCAS",bg="#E67E22",fg="black")
                etiquetaturno.place(x=435, y=0, width=100, height=35)

            else:
                etiquetaturno= Label(self.Game_Window,text="Turno: BLANCAS",bg="#E67E22",fg="black")
                etiquetaturno.place(x=605, y=0, width=100, height=35)


        else:
            if self.Board_Size.get() == 6:
                etiquetaturno= Label(self.Game_Window,text="Turno: NEGRAS",bg="#E67E22",fg="white")
                etiquetaturno.place(x=435, y=0, width=100, height=35)

            else:
                etiquetaturno= Label(self.Game_Window,text="Turno: NEGRAS",bg="#E67E22",fg="white")
                etiquetaturno.place(x=605, y=0, width=100, height=35)

    def Eval_Funtion_bar(self):
        self.Eval_Num=0
        for i in range(len(self.List_Boxes)):
            if self.List_Boxes[i] ==0:
                continue
            if i in self.Corners:
                self.Eval_Num += self.List_Boxes[i]*3
            if i in (self.Top_Egde or self.Bottom_Egde or self.Left_Edge or self.Right_Egde):
                self.Eval_Num += self.List_Boxes[i]*2
            else:
                self.Eval_Num += self.List_Boxes[i]
        #print(self.Eval_Num)
        return self.Eval_Num

    def check_win_condition(self):
        if self.List_Boxes.count(0)==0:
            if self.Count_White>self.Count_Black:
                messagebox.showinfo("REVERSI", "GANAN LAS BLANCAS!")
            elif self.Count_White<self.Count_Black:
                messagebox.showinfo("REVERSI", "GANAN LAS NEGRAS!")
            else:
                messagebox.showinfo("REVERSI", "EMPATE!")

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

    def print_turn_color(self):
        if self.Color.get()==1:
            print('JUEGAN LAS BLANCAS')
            self.printListBoxes(self.List_Boxes)
            print(self.possible_moves(self.List_Boxes,self.Color.get()))     
        else:
            print('JUEGAN LAS NEGRAS')
            self.printListBoxes(self.List_Boxes)
            print(self.possible_moves(self.List_Boxes,self.Color.get())) 

    def printListBoxes(self,l):
        for i in range(self.Board_Size.get()):
            for j in range(self.Board_Size.get()):
                if l[i*self.Board_Size.get()+j]>=0:
                    print(' ',end='')
                print(l[i*self.Board_Size.get()+j],end=' ')
            print()

    def select_move_in(self,event):
        if event.widget.x*self.Board_Size.get()+event.widget.y in self.possible_moves(self.List_Boxes,self.Color.get()):
            self.boxes[self.conv_pos(event.widget.x*self.Board_Size.get()+event.widget.y)[0]][self.conv_pos(event.widget.x*self.Board_Size.get()+event.widget.y)[1]].config(image=self.Full_Space)        #matriz[x][y].config(image=my_pic)
            self.boxes[self.conv_pos(event.widget.x*self.Board_Size.get()+event.widget.y)[0]][self.conv_pos(event.widget.x*self.Board_Size.get()+event.widget.y)[1]].image=self.Full_Space

    def select_move_out(self,event):
        if event.widget.x*self.Board_Size.get()+event.widget.y in self.possible_moves(self.List_Boxes,self.Color.get()):
            self.boxes[self.conv_pos(event.widget.x*self.Board_Size.get()+event.widget.y)[0]][self.conv_pos(event.widget.x*self.Board_Size.get()+event.widget.y)[1]].config(image=self.Empty_space)        #matriz[x][y].config(image=my_pic)
            self.boxes[self.conv_pos(event.widget.x*self.Board_Size.get()+event.widget.y)[0]][self.conv_pos(event.widget.x*self.Board_Size.get()+event.widget.y)[1]].image=self.Empty_space

game= UI_Reversi()
mainloop()
