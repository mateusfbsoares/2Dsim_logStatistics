#obs: código adaptado devido a arquivo .csv com erro: o showtime pula de 2999 para 3001 sem passar pelo 3000;
#     por conta disso, onde deveria ter apenas "len(log)", tem "len(log)-1". se o arquivo .csv utilizado estiver correto, deve-se deixar "len(log)" apenas.
#     em alguns lugares, len(log)-1 ainda assim dá index fora da lista, então tive que deixar len(log)-2 para não dar erro (não descobri o motivo para isso)

#Constantes
raioRoboMaisBola = 1 #colocar o valor correto aqui (o valor atual foi obtido através de experimentação)
larguraDoGol = 5  #colocar o valor correto aqui (o valor atual é arbitrário obitido através da dedução olhando imagens de jogos em campeonatos)
distanciaPosse = 3.9 #colocar o valor correto, valor atual obtido de forma experimental

#Importação de bibliotecas e declaração de variáveis globais
import math
    #Importa a biblioteca que cuida da leitura do .csv
import csv 

    #Declaração de variáveis globais
log = [] #Array que guardará o conteúdo do .csv
i=0; #Variável auxiliar
j=0; #Variável auxiliar

#Guarda o conteúdo do .csv na matriz log (não guarda linhas repetidas)
with open('log.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    i=0
    j=0
    anterior = -1
    for line in csv_reader:
        if (line[0]!=anterior):
            log.append([])
            for collum in line:
                log[i].append(collum)
                j += 1
            i += 1
        anterior = line[0] 

#Criando classes para organizar as informações que estão na matriz log + uma classe para guardar os resultados
    #Classes:
    #Classe da bola
class ball:
    def __init__(self,log):
        #Declaração de cada array campo de informação de ball 
        self.x = []
        self.y = []
        self.vx = []
        self.vy = []
        #Guarda os valores de cada linha de log no campo de informação correspondente à respectiva coluna
        for i in range(1,len(log)-1):
            self.x.append(log[i][10])
            self.y.append(log[i][11])
            self.vx.append(log[i][12])
            self.vy.append(log[i][13])

    #Classe dos robôs
class robot:
    def __init__(self,log,side,number):        
        self.side = side
        self.team = 0 if side=="l" else 1
        self.number = number
        offset = 13 + (31*number) + (0 if side=="l" else (11*31)) #Isso daqui retorna o número da coluna anterior à primeira coluna
        #                                                              referente ao robô de número <num> e lado <side>
        #      (n1) + (    n2    ) * (          n3         ) --> explicações:
        #                                                      n1(número de colunas antes da primeira coluna do robô 1l)
        #                                                      n2(retorna 0 para o primeiro robô, 31 para o segundo... pois cada robô possui 31 colunas 
        #                                                      n3(retorna (11*31) para time 'r' pois o primeiro robô de r está a (11*31) colunas à direita
       
        #Declaração de cada array campo de informação de ball 
        self.chutesAoGol = 0 
        self.gols = 0
        self.efetividadeGols = 0
        self.periculosidade = 0
        self.unum = log[1][2+offset]
        self.type = log[1][3+offset]
        self.state = []
        self.x = []
        self.y = []
        self.vx = []
        self.vy = []
        self.body = []
        self.neck = []
        self.point_to_x = []
        self.point_to_y = []
        self.view_quality = []
        self.view_width = []
        self.attribute_stamina = []
        self.attribute_effort = []
        self.attribute_recovery = []
        self.attribute_stamina_capacity = []
        self.focus_side = []
        self.focus_unum = []
        self.counting_kick = []
        self.counting_dash = []
        self.counting_turn = []
        self.counting_catch = []
        self.counting_move = []
        self.counting_turn_neck = []
        self.counting_change_view = []
        self.counting_say = []
        self.counting_tackle = []
        self.counting_point_to = []
        self.counting_attention_to = []
        for i in range(1,len(log)-1):
            #Guarda os valores de cada linha de log no campo de informação correspondente à respectiva coluna
            self.state.append(log[i][4 + offset] if log[i][4 + offset]!="" else None)
            self.x.append(log[i][5 + offset] if log[i][5 + offset]!="" else None)
            self.y.append(log[i][6 + offset] if log[i][6 + offset]!="" else None)
            self.vx.append(log[i][7 + offset] if log[i][7 + offset]!="" else None)
            self.vy.append(log[i][8 + offset] if log[i][7 + offset]!="" else None)
            self.body.append(log[i][9 + offset] if log[i][9 + offset]!="" else None)
            self.neck.append(log[i][10 + offset] if log[i][10 + offset]!="" else None)
            self.point_to_x.append(log[i][11 + offset] if log[i][11 + offset]!="" else None)
            self.point_to_y.append(log[i][12 + offset] if log[i][12 + offset]!="" else None)
            self.view_quality.append(log[i][13 + offset] if log[i][13 + offset]!="" else None)
            self.view_width.append(log[i][14 + offset] if log[i][14 + offset]!="" else None)
            self.attribute_stamina.append(log[i][15 + offset] if log[i][15 + offset] else None)
            self.attribute_effort.append(log[i][16 + offset] if log[i][16 + offset] else None)
            self.attribute_recovery.append(log[i][17 + offset] if log[i][17 + offset] else None)
            self.attribute_stamina_capacity.append(log[i][18 + offset] if log[i][18 + offset] else None)
            self.focus_side.append(log[i][19 + offset] if log[i][19 + offset]!="" else None)
            self.focus_unum.append(log[i][20 + offset] if log[i][20 + offset]!="" else None)
            self.counting_kick.append(log[i][21 + offset] if log[i][21 + offset] else None)
            self.counting_dash.append(log[i][22 + offset] if log[i][22 + offset] else None)
            self.counting_turn.append(log[i][23 + offset] if log[i][23 + offset] else None)
            self.counting_catch.append(log[i][24 + offset] if log[i][24 + offset] else None)
            self.counting_move.append(log[i][25 + offset] if log[i][25 + offset] else None)
            self.counting_turn_neck.append(log[i][26 + offset] if log[i][26 + offset] else None)
            self.counting_change_view.append(log[i][27 + offset] if log[i][27 + offset] else None)
            self.counting_say.append(log[i][28 + offset] if log[i][28 + offset] else None)
            self.counting_tackle.append(log[i][29 + offset] if log[i][29 + offset] else None)
            self.counting_point_to.append(log[i][30 + offset] if log[i][30 + offset] else None)
            self.counting_attention_to.append(log[i][31 + offset] if log[i][31 + offset] else None) 

    #Classe dos times
class team:
    def __init__(self,log,side):
        #Declaração de cada array campo de informação de team
        self.num = 0 if side=="l" else 1 
        self.score = []
        self.pen_score = []
        self.pen_miss = []
        self.robots = []
        self.chutesAoGol = 0
        self.efetividadeGols = 0
        self.periculosidade = 0
        #Guarda os valores de cada linha de log no campo de informação correspondente à respectiva coluna
        self.name = log[1][2 if side=="l" else 3] 
        for i in range(1,len(log)-1): 
            self.score.append(log[i][4 if side=="l" else 5])
            self.pen_score.append(log[i][6 if side=="l" else 7])
            self.pen_miss.append(log[i][8 if side=="l" else 9])
        #Cria as instâncias dos robôs do time dentro de team (no array self.robots) 
        for i in range(0,11):
            self.robots.append(robot(log,side,i)) 
        #Descobre quem é o goleiro do time
        self.goleiro = None
        for r in self.robots: #Para cada robô
            for i in range(1,5998): #a cada showtime
                if(r.counting_catch[i] > r.counting_catch[i-1]): #se houve um catch
                    self.goleiro = r
                    break
                    

    #Classe do jogo
class game:
    def __init__(self,log):
        #Declaração de cada array campo de informação de game
        self.show_time = []
        self.playmode = []
        self.teams = []
        #Guarda os valores de cada linha de log no campo de informação correspondente à respectiva coluna
        for i in range(1,len(log)-1): 
            self.show_time.append(log[i][0])
            self.playmode.append(log[i][1])
        #Cria a instância da bola dentro de game (em self.ball)
        self.ball = ball(log)
        #Cria as instâncias dos dois times
        self.teams.append(team(log,"l"))
        self.teams.append(team(log,"r"))

    #Classe dos resultados
class results:
    def __init__(self,game):
        #draw --> True==empate ; False==não-empate
        self.draw = game.teams[0].score[-1]==game.teams[1].score[-1]
        #winner --> nome do time ganhador 
        if (self.draw == False):
            self.winner_name = game.teams[0].name if game.teams[0].score[-1]>game.teams[1].score[-1] else game.teams[1].name
        else:
            self.winner_name = None
        #Resultado final: quem ganhou ou se deu empate 
        self.final_result = self.winner_name + " vencedor!" if self.draw==False else "empate"

#Cria e guarda uma instância de game e results
game = game(log)
results = results(game)

#Declaração de funções para computações de dados e estatísticas -------------------------------------------------------------
    #Retorna True se houve um gol no dado ciclo, ou False caso contrário
def foiGol(showtime):
    for t in game.teams:
        if(t.score[showtime] > t.score[showtime-1]):
            return True
    return False

    #Retorna a distância de um ponto (x1,y1) a um ponto (x2,y2)
def distance(x1,y1,x2,y2):
    distance = math.sqrt(math.pow((x2-x1),2)+math.pow((y2-y1),2))
    return distance
   
    #retorna o robô que está em posse da bola: mais perto da bola (distância max: <distanciaPosse>) ou None se nenhum robô estiver a menos de <distanciaPosse> unidades da bola
def roboEmPosseDaBola(showTime):
    distanciasl = []
    distanciasr = []
    distancias = [distanciasl,distanciasr]
    for t in game.teams:
        for r in t.robots:
            r.distanciaDaBola = distance(float(r.x[showTime]),float(r.y[showTime]),float(game.ball.x[showTime]),float(game.ball.y[showTime])) #guarda no robô, a atual distância à bola
            distancias[t.num].append(r) #append cada robô à lista do time, cada um agora contendo a atual distância à bola
        distancias[t.num].sort(key=lambda x: x.distanciaDaBola) #ordena a lista do robô com a menor distância ao com a maior distância
    roboDeMenorDistancia = distancias[0][0] if (distancias[0][0].distanciaDaBola <= distancias[1][0].distanciaDaBola) else distancias[1][0] #Descobre o robô mais próximo da bola dos dois times
    return roboDeMenorDistancia if roboDeMenorDistancia.distanciaDaBola < distanciaPosse else None 

    #Distância percorrida por cada robô
def calculaDistanciaPercorrida(robot):
    robot.distanciaPercorrida = 0
    for i in range(1,len(log)-2):
        robot.distanciaPercorrida += distance(float(robot.x[i]),float(robot.y[i]),float(robot.x[i-1]),float(robot.y[i-1])) #Adiciona a distância percorrida de um ciclo ao próximo
    return robot.distanciaPercorrida
    
    #Printa as distâncias percorridas de cada um dos robôs
def printaDistanciasAll():
    for t in game.teams:
        print("time: " + t.name)
        for r in t.robots:
            print("Robot " + r.unum + ": " + str(calculaDistanciaPercorrida(r)))
        print("")

    #Retorna qual o robô que correu mais em dado time
def quemCorreuMais(team):
    maiorDistancia = 0
    for r in team.robots:
        if (calculaDistanciaPercorrida(r) >= maiorDistancia):
            maiorDistancia = r.distanciaPercorrida
            robo = r
    return robo

    #Cria um vetor em cada robô contendo o dado de se ele está ou não em posse da bola em cada ciclo
def calculaPosseGeral():
    for t in game.teams:
        for r in t.robots:
            r.emPosseDaBola = []
            for i in range(0,len(log)-2):
                r.emPosseDaBola.append(True if roboEmPosseDaBola(i)==r else False)

    #retorna a posse de bola absoluta de um robô
def posseAbsolutaRobo(robo):
    posseAbsoluta = 0
    for i in range(0,len(log)-2):
        if(robo.emPosseDaBola[i] == True):
            posseAbsoluta += 1
    return posseAbsoluta

    #retorna a posse de bola absoluta de um dado time
def posseAbsolutaTime(team):
    posseAbsoluta = 0
    for r in team.robots:
        posseAbsoluta += posseAbsolutaRobo(r)
    return posseAbsoluta

    #retorna a posse de um robô específico em relação ao seu time
def posseRelativaRobo_time(robo):
    return (100*posseAbsolutaRobo(robo))/posseAbsolutaTime(game.teams[robo.team])
    
    #retorna a posse de um robô específico em relação a todos os robôs dos dois times
def posseRelativaRobo_geral(robo):
    return (100*posseAbsolutaRobo(robo))/(posseAbsolutaTime(game.teams[0]) + posseAbsolutaTime(game.teams[1]))

    #retorna a posse de um time em relação à posse total
def posseRelativaTime(time):
    return (100*posseAbsolutaTime(time))/(posseAbsolutaTime(game.teams[0]) + posseAbsolutaTime(game.teams[1]))

    #retorna uma lista contendo as dimensões virtuais da quadra [maior_x,menor_x,maior_y,menor_y] (só deve ser utilizado em caso de não se conhecer as dimensões da quadra)
def encontraDimensoesVirtuais(): #A dimensão virtual da quadra é definida por até onde a bola alcançou durante a partida
    maior_x = 0
    menor_x = 30 #número arbitrário
    maior_y = 0
    menor_y = 30 #número arbitrário
    for i in range(0,len(log)-2):
        if (float(game.ball.x[i])>maior_x):
            maior_x = float(game.ball.x[i])
        if (float(game.ball.x[i])<menor_x):
            menor_x = float(game.ball.x[i])
        if (float(game.ball.y[i])>maior_y):
            maior_y = float(game.ball.y[i])
        if (float(game.ball.y[i])<menor_y):
            menor_y = float(game.ball.y[i])
    return [maior_x,menor_x,maior_y,menor_y] 

#analisa se alguém chutou (se sim, quem), retorna o objeto que chutou ou None se não houve chute
def quemChutouABola(showtime):
    quemChutou = None 
    loopMustBreak = False
    for t in game.teams:
        for r in t.robots:
            if(r.counting_kick[showtime] > r.counting_kick[showtime-1]):
                quemChutou = r
                loopMustBreak = True
                break
        if loopMustBreak: break
    #se não houve chute, retorna None
    if(quemChutou == None):
        return None
    else:
        return quemChutou

    #Retorna True se foi um chute ao gol ou False não foi, retorna None se não houve chute naquele ciclo; obstacle é uma lista que recebe o obstáculo à bola
def foiChuteAoGol(showtime,obstacle=None): #Analisa se há algum robô na reta suporte do vetor velocidade da bola adiante a quem chuta, a menos do goleiro, e retorna True se não há, e se e o vetor velocidade da bola apontar em direção ou próximo ao gol
    quemChutou = quemChutouABola(showtime)
    #Se não houve chute, retorna None
    if(quemChutou == None):
        return None
    #se houve chute, contiua
    #desobre se há alguém adiante de quem chuta na reta suporte do vetor velocidade da bola, a menos do goleiro e guarda a resposta em <resultado> 
    dimensoes = encontraDimensoesVirtuais() 
    x = float(game.ball.x[showtime])
    y = float(game.ball.y[showtime])
    obstaculo = False
    moduloVetorVelocidadeBola = math.sqrt(math.pow(float(game.ball.vx[showtime]),2) + math.pow(float(game.ball.vy[showtime]),2))
    if(moduloVetorVelocidadeBola!=0):
        vetorVelocidadeBolaNormalizado = [float(game.ball.vx[showtime])/moduloVetorVelocidadeBola,float(game.ball.vy[showtime])/moduloVetorVelocidadeBola]
    else:
        vetorVelocidadeBolaNormalizado = [0,0] 
    loopMustBreak = False 
    while(x < dimensoes[0] and x > dimensoes[1] and y < dimensoes[2] and y > dimensoes[3]): #enquanto (x,y) estiver dentro do campo, move (x,y) ao longo da reta suporte e checa se tem alguém nessa posição
        for t in game.teams:
            for r in t.robots:
                if(abs(float(r.x[showtime])-x)<raioRoboMaisBola and abs(float(r.y[showtime])-y)<raioRoboMaisBola): #checa em cada robô, se ele está na dada posição, se sim, obstaculo = True
                    if(t.goleiro != r): 
                        obstaculo = True
                        loopMustBreak = True
                        if(obstacle!=None):
                            obstacle[0] = r
                        break
            if loopMustBreak: break
        if loopMustBreak: break
        x += vetorVelocidadeBolaNormalizado[0] #Move (x,y) na reta suporte
        y += vetorVelocidadeBolaNormalizado[1]
    #descobre se quem chutou estava na área do inimigo quando chutou (chutes ao gol ocorrem no campo inimigo)
    estavaNoCampoInimigo = (float(quemChutou.x[showtime])<(dimensoes[0]/2)) if quemChutou.side=="r" else (float(quemChutou.x[showtime])>(dimensoes[0]/2))
    #checa se a reta suporte passa perto do gol
    passaPertoDoGol = False 
    x = float(game.ball.x[showtime])
    y = float(game.ball.y[showtime])
    if(quemChutou.side=="l"):
        while(x<dimensoes[0] and x>dimensoes[1] and y<dimensoes[2] and y>dimensoes[3] and vetorVelocidadeBolaNormalizado[0]!=0 and vetorVelocidadeBolaNormalizado[1]!=0):
            if(abs(x-dimensoes[0]<2*vetorVelocidadeBolaNormalizado[0])):
                passaPertoDoGol = True
                break
            x += vetorVelocidadeBolaNormalizado[0]
            y += vetorVelocidadeBolaNormalizado[1]
    else:
        while(x<dimensoes[0] and x>dimensoes[1] and y<dimensoes[2] and y>dimensoes[3] and vetorVelocidadeBolaNormalizado[0]!=0 and vetorVelocidadeBolaNormalizado[1]!=0):
                if(x<2*vetorVelocidadeBolaNormalizado[0]):
                    passaPertoDoGol = True
                    break
                x += vetorVelocidadeBolaNormalizado[0]
                y += vetorVelocidadeBolaNormalizado[1]
    #Se não há obstáculos à frente e quem chutou estava no campo inimigo, então foi um chute ao gol
    if(obstaculo==False and estavaNoCampoInimigo and passaPertoDoGol):
        return True

#Calula o número de chutes ao gol e de gols de cada robô e time e salva nos próprios objetos
def calculaChutesEGols():
    totalGols = 0
    for i in range(1,len(log)-2):
        for t in game.teams:
            if(t.score[i]>t.score[i-1]):
                j = i
                while(quemChutouABola(j)==None):
                    j -= 1
                quemChutouABola(j).gols +=1
            for r in t.robots:
                if(r.counting_kick[i]>r.counting_kick[i-1] and foiChuteAoGol(i)):
                    r.chutesAoGol += 1
    for t in game.teams:
        t.chutesAoGol = 0
        for r in t.robots:
            t.chutesAoGol += r.chutesAoGol

#Calcula a efetividade de um robô (taxa de gols/chutesAoGol), retorna e guarda no próprio objeto
def calculaEfetividadeRobo(robo):
    robo.efetividadeGols = (100*robo.gols)/robo.chutesAoGol if robo.chutesAoGol!=0 else None
    return robo.efetividadeGols

#Calcula a efetividade de um time (taxa de gols/chutesAoGol), retorna e guarda no próprio objeto
def calculaEfetividadeTime(time):
    chutesAoGolTotal = 0 
    golsTotal = 0 
    for r in time.robots:
        chutesAoGolTotal += r.chutesAoGol
        golsTotal += r.gols
    time.efetividadeGols = (100*golsTotal)/chutesAoGolTotal if chutesAoGolTotal!=0 else 0
    return time.efetividadeGols


#Calcula o quanto um jogador é agressivo (tenta fazer gols) em relação aos outros da partida, retorna e guarda o dado no próprio objeto
def periculosidadeRobo(robo):
    chutesAoGolTotalPartida = 0
    for t in game.teams:
        for r in t.robots:
            chutesAoGolTotalPartida += r.chutesAoGol
    robot.periculosidade = (100*robo.chutesAoGol)/chutesAoGolTotalPartida if chutesAoGolTotalPartida!=0 else 0
    return robot.periculosidade

#Calcula o quanto um time é agressivo (tenta fazer gols) em relação aos dois times entre si
def periculosidadeTime(time):
    chutesAoGolTotalPartida = 0
    for t in game.teams:
        for r in t.robots:
            chutesAoGolTotalPartida += r.chutesAoGol
    time.periculosidade = (100*time.chutesAoGol)/chutesAoGolTotalPartida if chutesAoGolTotalPartida!=0 else 0
    return time.periculosidade
#-----------------------------------------------------------------------------------------------------------------------------

calculaPosseGeral()
calculaChutesEGols()
for t in game.teams:
    calculaEfetividadeTime(t)
    periculosidadeTime(t)
    for r in t.robots:
        calculaEfetividadeRobo(r)
        periculosidadeRobo(t)

#Empacotamento dos dados estatísticos em uma matriz
matrizDeDados = [[''for x in range(len(log))] for y in range(60)]
totalChutesAoGolTimel = 0
totalChutesAoGolTimer = 0
totalGolsTimel = 0
totalGolsTimer = 0
totalDistanciaTimel = 0
totalDistanciaTimer = 0
for t in game.teams:
    matrizDeDados[1][t.num+1] = posseAbsolutaTime(t)
    matrizDeDados[4][t.num+1] = posseRelativaTime(t)
    matrizDeDados[5][t.num+1] = quemCorreuMais(t).unum
    matrizDeDados[8][t.num+1] = periculosidadeTime(t)
    matrizDeDados[11][t.num+1] = calculaEfetividadeTime(t)
    for r in t.robots:
        matrizDeDados[1][2 + (int(r.unum) if t.num==0 else 1 + int(r.unum)+11)] = posseAbsolutaRobo(r)
        matrizDeDados[2][2 + (int(r.unum) if t.num==0 else 1 + int(r.unum)+11)] = posseRelativaRobo_time(r)
        matrizDeDados[3][2 + (int(r.unum) if t.num==0 else 1 + int(r.unum)+11)] = posseRelativaRobo_geral(r) 
        matrizDeDados[7][2 + (int(r.unum) if t.num==0 else 1 + int(r.unum)+11)] = calculaDistanciaPercorrida(r)
        matrizDeDados[8][2 + (int(r.unum) if t.num==0 else 1 + int(r.unum)+11)] = periculosidadeRobo(r)
        matrizDeDados[11][2 + (int(r.unum) if t.num==0 else 1 + int(r.unum)+11)] = calculaEfetividadeRobo(r)
        matrizDeDados[9][2 + (int(r.unum) if t.num==0 else 1 + int(r.unum)+11)] = r.chutesAoGol
        matrizDeDados[10][2 + (int(r.unum) if t.num==0 else 1 + int(r.unum)+11)] = r.gols
        totalChutesAoGolTimel += r.chutesAoGol if t.num==0 else 0
        totalChutesAoGolTimer += r.chutesAoGol if t.num==1 else 0
        totalGolsTimel += r.gols if t.num==0 else 0
        totalGolsTimer += r.gols if t.num==1 else 0
        totalDistanciaTimel += calculaDistanciaPercorrida(r) if t.num==0 else 0
        totalDistanciaTimer += calculaDistanciaPercorrida(r) if t.num==1 else 0
        matrizDeDados[6][1] = quemCorreuMais(game.teams[0]).unum if calculaDistanciaPercorrida(quemCorreuMais(game.teams[0])) > calculaDistanciaPercorrida(quemCorreuMais(game.teams[1])) else quemCorreuMais(game.teams[1]).unum
    matrizDeDados[9][1] = totalChutesAoGolTimel
    matrizDeDados[9][2] = totalChutesAoGolTimer
    matrizDeDados[10][1] = totalGolsTimel
    matrizDeDados[10][2] = totalGolsTimer
    matrizDeDados[7][1] = totalDistanciaTimel
    matrizDeDados[7][2] = totalDistanciaTimer
    for i in range(len(log)-2):
        matrizDeDados[12][i+1] = game.ball.x[i]
        matrizDeDados[13][i+1] = game.ball.y[i]

    for i in range(22):
        for j in range(len(log)-2):
            matrizDeDados[14+i][j+1] = game.teams[int(i/11)].robots[i if i<11 else i-11].x[j]
    for i in range(22):
        for j in range(len(log)-2):
            matrizDeDados[36+i][j+1] = game.teams[int(i/11)].robots[i if i<11 else i-11].x[j]
#Criando labels para a matriz
matrizDeDados[0][1] = game.teams[0].name
matrizDeDados[0][2] = game.teams[1].name
for i in range(1,23):
    matrizDeDados[0][3+i-1] = ("robô " + str(i if i<12 else i-11) + "_" + ("l" if i<12 else "r"))
matrizDeDados[1][0] = "posse absoluta"
matrizDeDados[2][0] = "posse relativa ao time"
matrizDeDados[3][0] = "posse relativa a todos"
matrizDeDados[4][0] = "posse relativa entre os times"
matrizDeDados[5][0] = "quem correu mais no time"
matrizDeDados[6][0] = "quem correu mais no total"
matrizDeDados[7][0] = "distâncias percorridas"
matrizDeDados[8][0] = "periculosidade"
matrizDeDados[9][0] = "chutes ao gol"
matrizDeDados[10][0] = "número de gols"
matrizDeDados[11][0] = "efetividade"
matrizDeDados[12][0] = "posição x da bola"
matrizDeDados[13][0] = "posição y da bola"
for i in range(1,23):
    matrizDeDados[13+i][0] = "posição x do robô " + str(i if i<12 else i-11) + "_" + ("l" if i<12 else "r")
    matrizDeDados[22+13+i][0] = "posição y do robô " + str(i if i<12 else i-11) + "_" + ("l" if i<12 else "r")
#Exportação da matriz em formato .csv
with open('dados.csv','w',newline='') as f:
    thewriter = csv.writer(f)

    for i in range(60):
        thewriter.writerow(matrizDeDados[i])
