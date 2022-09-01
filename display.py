from tkinter import *
from tkinter import messagebox
import numpy as np
class Reversi:

    def __init__(self):
        self.Principal_Window = Tk()
        self.Principal_Window.title('Inicio')
        self.Principal_Window.geometry('500x500')
        self.Principal_Window.eval('tk::PlaceWindow . center')
        #self.Principal_Window.iconbitmap('Sin título.ico')
        Label(self.Principal_Window,text='Seleccione color: ').pack()
        # Color 
        # 0: para vacio
        # 1: para AMARILLAS
        # -1: para AZULES
        self.Color =IntVar()
        self.Color.set(1)
        Radiobutton(self.Principal_Window,text='AMARILLAS',variable=self.Color,value=1).pack()
        Radiobutton(self.Principal_Window,text='AZULES',variable=self.Color,value=-1).pack()
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
        self.difficulty = StringVar()
        self.difficulty.set('1')
        difficulty_levels =[('Fácil','1'),('Normal','2'),('Difícil','3')]
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
        for i in range(self.Board_Size.get()):
            l=[]
            for j in range(self.Board_Size.get()):
                if (i==self.Board_Size.get()/2 and j==self.Board_Size.get()/2) or (i==(self.Board_Size.get()/2)-1 and j==(self.Board_Size.get()/2)-1):
                    b1=Button(self.Game_Window,image=self.W_Piece,width="80",height="80")
                    self.List_Boxes[i*self.Board_Size.get()+j]=1
                elif(i==self.Board_Size.get()/2 and j==(self.Board_Size.get()/2)-1) or (i==(self.Board_Size.get()/2)-1 and j== self.Board_Size.get()/2):
                    b1=Button(self.Game_Window,image=self.B_Piece,width="80",height="80")
                    self.List_Boxes[i*self.Board_Size.get()+j]=-1
                else:
                    b1=Button(self.Game_Window,image=self.Empty_space,width="80",height="80")
                b1.bind("<Button-1>",self.click)
                b1.x=i
                b1.y=j
                b1.grid(row=i,column=j)
                l.append(b1)
            self.boxes.append(l)
        self.def_pos()
        self.def_edge()
        self.who_is_playing()

    def who_is_playing(self):
        if self.Color.get()==1:
            print('JUEGAN LAS AMARILLAS')
            self.printListBoxes()
            print(self.possible_moves(self.Color.get()))     
        else:
            print('JUEGAN LAS AZULES')
            self.printListBoxes()
            print(self.possible_moves(self.Color.get())) 

    def def_pos(self):
        # 8 posiciones
        self.izq=-1
        self.der=1
        self.arr=-1*self.Board_Size.get()
        self.aba=self.Board_Size.get()
        self.dia=-1*(self.Board_Size.get()-1) #diagonal izquierda arriba
        self.dib=self.Board_Size.get()-1 #diagonal izquierda abajo
        self.dda=-1*(self.Board_Size.get()+1) #diagonal derecha arriba
        self.ddb=self.Board_Size.get()+1 #diagonal derecha abajo

    def def_edge(self):
        self.Top_Egde = [i for i in range(1,self.Board_Size.get()-1)]
        self.Bottom_Egde = [i for i in range(self.Board_Size.get()*(self.Board_Size.get()-1)+1,(self.Board_Size.get()**2)-1)]
        self.Left_Edge = [i for i in range(self.Board_Size.get(),self.Board_Size.get()*(self.Board_Size.get()-1),self.Board_Size.get())]
        self.Right_Egde = [i for i in range(self.Board_Size.get()+(self.Board_Size.get()-1),(self.Board_Size.get()**2)-1,self.Board_Size.get())]
        self.Edge_Positions = [0]+self.Top_Egde+[self.Board_Size.get()-1]+self.Left_Edge+self.Right_Egde+[(self.Board_Size.get()-1)*self.Board_Size.get()]+self.Bottom_Egde+[(self.Board_Size.get()**2)-1]

    def Edge_Exceptions(self,pos):
         #LAS 8 EXCEPCIONES
        if pos == 0: #First_Corner
            return [self.der,self.ddb,self.aba]
        if pos == self.Board_Size.get()-1: #Second_Corner 
            return [self.izq,self.dib,self.aba]
        if pos == (self.Board_Size.get()-1)*self.Board_Size.get():#Third_Corner =
            return [self.arr,self.dia,self.der] 
        if pos == (self.Board_Size.get()**2)-1:#Fourth_Corner = 
            return [self.izq,self.dda,self.arr]
        if pos in self.Top_Egde:# Top_Egde = 
            return [self.izq,self.ddb,self.aba,self.dib,self.der]
        if pos in self.Bottom_Egde: #Bottom_Egde = 
            return [self.izq,self.dia,self.arr,self.dda,self.der]
        if pos in self.Left_Edge: #Left_Edge = 
            return [self.arr,self.dia,self.der,self.ddb,self.aba]
        if pos in self.Right_Egde: #Right_Egde = 
            return [self.arr,self.dda,self.izq,self.dib,self.aba]
        else:
            return [self.dia,self.arr,self.dda,self.der,self.dib,self.aba,self.ddb,self.izq]

    def recursive_look_direction(self,pos, dir,color):
        if (pos+dir <0) or (pos+dir >(self.Board_Size.get()**2)): #fail verification
            return -1
        #if pos+dir in self.Edge_Positions and (dir not in self.Edge_Exceptions(pos+dir)):
            #return -1
        if(self.List_Boxes[pos+dir]==0):
            return pos+dir
        if(self.List_Boxes[pos+dir]==color):
            #se revisa en la sig
            return -1
        else: # entonces es el color contrario
            #if pos+dir in self.Edge_Positions: #si llega al borde 
            #    return -1
            #else:
            return self.recursive_look_direction(pos+dir,dir,color)

    def eatable(self,pos,dir,color):
        if pos+dir <0 or pos+dir >(self.Board_Size.get()**2): #fail verification
            return -1
        #if pos+dir in self.Edge_Positions: #si llega al borde 
            #return -1
        if (self.List_Boxes[pos+dir]==-1*color): #Donde tengo un color contrario adyacente
            p=self.recursive_look_direction(pos+dir,dir,color)
            if p!=-1:
                return p
            else:
                return -1
        else: #tengo 0 adyacente
            return -1

    def possible_moves(self,color):
        list_pm=[]
        for i in list(np.where(np.array(self.List_Boxes) == color)[0]):
            for j in self.Edge_Exceptions(i):
                pm=self.eatable(i,j,color)
                print("movimientos posibles")
                print("pos: ",i,"look_dir: ",i+j,"resp: ",pm) 
                if pm !=-1 and pm not in list_pm:
                    list_pm.append(pm)
        return list_pm        

    def recursive_get_direction(self,pos,dir,color):
        
        if ((pos+dir) <0) or ((pos+dir) >(self.Board_Size.get()**2)):
            return []
        #if dir not in self.Edge_Exceptions(pos+dir):
           # return [-1]
        print(pos+dir,self.List_Boxes[pos+dir])
        if(self.List_Boxes[pos+dir]==color):
            return [pos]
        if(self.List_Boxes[pos+dir]==-1*color)and dir in self.Edge_Exceptions(pos+dir):
        # and(self.List_Boxes[pos+dir] not in self.Edge_Positions):
            return [pos]+self.recursive_get_direction(pos+dir,dir,color)
        else:
            if self.List_Boxes[pos+dir]==0:
                return [-1]
            if self.List_Boxes[pos+dir] in self.Edge_Positions:
                return [-1]
            else:
                return []

    def changeable(self,pos,dir,color):
        if ((pos+dir) <0) or ((pos+dir) >=(self.Board_Size.get()**2)):
                return []
        
        if self.List_Boxes[pos+dir] == -1*color:
            change=self.recursive_get_direction(pos+dir,dir,color)
            print(change)
            if -1 in change:
                return []
            else:
                return change
        else:
            return []

    def change_color_eaten(self, pos, color):
        list_pos_to_change=[]
        for i in self.Edge_Exceptions(pos):
            box_to_change= self.changeable(pos,i,color)
            print("fichas a comer")
            print("pos: ",pos, "pos_a_diri: ",pos+i,"se cambian las pos: ", box_to_change)
            if len(box_to_change)!= 0:
                list_pos_to_change=list_pos_to_change+box_to_change
        for i in list_pos_to_change:
            if self.Color.get()==1:
                self.boxes[self.conv_pos(i)[0]][self.conv_pos(i)[1]].config(image=self.W_Piece)
                self.List_Boxes[i]=1
            else:
                self.boxes[self.conv_pos(i)[0]][self.conv_pos(i)[1]].config(image=self.B_Piece)
                self.List_Boxes[i]=-1

    def conv_pos(self,pos):
        return[pos//self.Board_Size.get(),pos%self.Board_Size.get()]
        
    def click(self,event):
        if self.List_Boxes[event.widget.x*self.Board_Size.get()+event.widget.y] ==0:
            if self.Color.get()==1:
                if event.widget.x*self.Board_Size.get()+event.widget.y not in self.possible_moves(self.Color.get()):
                    print('JUGADA INVALIDA')
                    print(self.possible_moves(self.Color.get()))
                if len(self.possible_moves(self.Color.get()))==0:
                    print('AMARILLAS NO TIENEN JUGADAS')
                    self.Color.set(-1)
                    self.who_is_playing()
                    
                if event.widget.x*self.Board_Size.get()+event.widget.y in self.possible_moves(self.Color.get()):
                    self.change_color_eaten(event.widget.x*self.Board_Size.get()+event.widget.y,self.Color.get())
                    event.widget['image'] = self.W_Piece
                    self.List_Boxes[event.widget.x*self.Board_Size.get()+event.widget.y]=1
                    self.Color.set(-1)
                    self.who_is_playing()
                
            else:
                if event.widget.x*self.Board_Size.get()+event.widget.y not in self.possible_moves(self.Color.get()):
                    print('JUGADA INVALIDA N')
                    print(self.possible_moves(self.Color.get()))
                if len(self.possible_moves(self.Color.get()))==0:
                    print('AZULES NO TIENEN JUGADAS')
                    self.Color.set(1)
                    self.who_is_playing()
                if event.widget.x*self.Board_Size.get()+event.widget.y in self.possible_moves(self.Color.get()):
                
                    self.change_color_eaten(event.widget.x*self.Board_Size.get()+event.widget.y,self.Color.get())
                    event.widget['image'] = self.B_Piece
                    self.List_Boxes[event.widget.x*self.Board_Size.get()+event.widget.y]=-1
                    
                    self.Color.set(1)
                    self.who_is_playing()

    def printListBoxes(self):
        for i in range(self.Board_Size.get()):
            for j in range(self.Board_Size.get()):
                if self.List_Boxes[i*self.Board_Size.get()+j]>=0:
                    print(' ',end='')
                print(self.List_Boxes[i*self.Board_Size.get()+j],end=' ')
            print()
        #print()

game= Reversi()
mainloop()
