class ReversiGame:
  #Comienza el raton, valor=-1
    def __init__(self,List_Boxes,color):
        self.List_Board=List_Boxes
        self.completo=False
        self.ganador=None
        self.jugador=color
    def Eval_Board(self):
        
        self.List_Board.count(1)+self.List_Board.count(-1)

def alfabeta(juego,etapa,alfa,beta,secuencia,secuencias): #r2=alfabeta(juego,1,-1000,1000,[],o2)
    if juego.estado_final():
        secuencias.append(secuencia.copy())
        return [juego.calcular_utilidad()]
    if etapa==1:
        valor=[-1000,None]
    else:
        valor=[1000,None]
    jugadas_posibles=juego.generar_jugadas_posibles()
    for jugada in jugadas_posibles:
        juego.jugar(jugada)
        secuencia.append(jugada)
        opcion=alfabeta(juego,etapa*-1,alfa,beta,secuencia,secuencias)
        if etapa==1:
            if opcion[0]>valor[0]:
                valor=[opcion[0],jugada]
                alfa=max(alfa,valor[0])
            if valor[0]>=beta:
                juego.deshacer_jugada(jugada)
                secuencia.pop()
                break
        else:
            if opcion[0]<valor[0]:
                valor=[opcion[0],jugada]
                beta=min(beta,valor[0])
            if valor[0]<=alfa:
                juego.deshacer_jugada(jugada)
                secuencia.pop()
                break
        juego.deshacer_jugada(jugada)
        secuencia.pop()
    return valor