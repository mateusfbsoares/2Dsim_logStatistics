def posseDeBola(team):
    #Descobre o goleiro de cada time e a quantidade de catches desse goleiro
    numberOfCatches = 0
    encontrouGoleiro = False
    for i in range(0,11): #para cada robô
        for j in range(len(log)-1): #para cada showtime
            if(int(team.robots[i].counting_catch[j])>0 and encontrouGoleiro==False): #se o counting_catch for > 0
                team.goalKeeper_unum = team.robots[i].unum #atribua o unum deste robô como do goleiro
                encontrouGoleiro = True
            if(int(team.robots[i].counting_catch[j])>int(team.robots[i].counting_catch[j-1])): #se deu um catch
                team.goalKeeper_numberOfCatches += 1; #aumenta a contagem de catches
    if(encontrouGoleiro == False): #se não descobriu quem é o goleiro
        team.goalKeeper_unum = team.robots[i].unum = None
    #Usa o counting_kick como parâmetro para determinar a posse de bola
     
        
        #Descobre o goleiro de cada time e a quantidade de catches desse goleiro
        for t in range(2): #para cada time,
            self.teams[t].goleiro_numberOfCatches = 0
            encontrouGoleiro = False
            for i in range(0,11): #para cada robô,
                for j in range(len(log)-1): #para cada showtime,
                    if(int(self.teams[t].robots[i].counting_catch[j])>0 and encontrouGoleiro==False): #se o counting_catch for > 0
                        self.teams[t].goalKeeper_uNum = self.teams[t].robots[i].unum #atribua o unum deste robô como do goleiro
                        encontrouGoleiro = True
                    if(int(self.teams[t].robots[i].counting_catch[j])>int(self.teams[0].robots[i].counting_catch[j-1])): #se deu um catch
                        self.teams[t].goalKeeper_numberOfCatches += 1; #Aumenta a contagem de catches
            if(encontrouGoleiro == False): #Se não descobriu quem é o goleiro
                self.teams[t].goalKeeper_uNum = self.teams[t].robots[i].unum = None
        #Usa o counting_kick como parâmetro para determinar a posse de bola:
        for t in range(2): #Para cada time,
            self.teams[t].ballPossessionTotal = 0
            for robot in self.teams[t].robots: #para cada robô,
                robot.ballPossession = 0 
                for i in range(2,len(log)-1): #para cada linha showtime
                    if(robot.counting_kick[i]>robot.counting_kick[i-1]): #Se o robô deu um chute, 
                        robot.ballPossession += 1 #aumenta sua posse de bola de 1
                        self.teams[t].ballPossessionTotal += 1 #aumenta a posse de bola total do time de 1


#copy-paste do código principal:
#-------------------------------------------------------------------------------------------------------------------------------- 
        #Estatísticas sobre posse de bola
            #A maior posse de bola
        listOfPossessions = [game.teams[0].ballPossessionTotal,game.teams[1].ballPossessionTotal]
        self.biggestBallPossession = max(listOfPossessions)
            #Time com a maior posse de bola
        self.teamWithBiggestPossession = game.teams[listOfPossessions.index(self.biggestBallPossession)].name
            #Ordem decrescente dos jogadores de cada time e suas respectivas posses de bola
        self.ballPossessionSortedTeams = []
        for t in range(2): #para cada time
            self.ballPossessionSortedTeams.append([])
            for robot in game.teams[t].robots: #para cada robô
                self.ballPossessionSortedTeams[t].append(robot) #o adiciona na lista sorted
            self.ballPossessionSortedTeams.sort(key=lambda x: x[0].ballPossession) #põe a lista em ordem 
            
            #TODO:Implementar mais algumas estatísticas, e criar um arquivo em formato csv, depois exibir os dados utilizando chart.js)
#---------------------------------------------------------------------------------------------------------------------------------

#printa as distâncias que cada robô estava da bola no ciclo antes do chute
for t in game.teams:
    for r in t.robots:
        for i in range(0,6000):
            if(r.counting_kick[i]>r.counting_kick[i-1]):
                print(distance(float(r.x[i]),float(r.y[i]),float(game.ball.x[i]),float(game.ball.y[i])))


#tentativa: determinar se a bola estava em posse baseando-se na constância da distância entre a bola e o robo que chutou
#falhou pois a distância entre a bola e o robô que a possui não é constante.
for t in game.teams:
    for r in t.robots:
        for i in range(5,6000):
            distancia_inicial = distance(float(r.x[0]),float(r.y[0]),float(game.ball.x[0]),float(game.ball.y[0])) #distancia entre a bola e o robô
            posse = True #Determina se a bola estava em posse
            if(r.counting_kick[i]>r.counting_kick[i-1]):
                for j in range(0,1):
                    distancia_atual = distance(float(r.x[i-j]),float(r.y[i-j]),float(game.ball.x[i-j]),float(game.ball.y[i-j])) 
                    if(distancia_atual != distancia_inicial):
                        posse = False
        if(posse == True):
            print(distancia_inicial)

#tentei associar a posse de bola individual ao player_state mas sem sucesso em encontrar um padrão
for t in game.teams:
    for r in t.robots:
        for i in range(0,6000):
            if(r.counting_kick[i]>r.counting_kick[i-1]):
                print(r.state[i-1]) #printa o state um ciclo antes de ter chutado
                print(r.state[i]) #printa o state no ciclo do chute


#------------não deu certo por algum motivo desconhecido: a condição do if nunca era satisfeita quando deveria ser)
 #checa se a reta suporte passa perto do gol 
    x = float(game.ball.x[showtime])
    y = float(game.ball.y[showtime]) 
    passaPertoDoGol = False
    loopMustBreak = False
    i =0
    while(i<100 and x < dimensoes[0] and x > dimensoes[1] and y < dimensoes[2] and y > dimensoes[3]):
        if( ((abs(x)<10 and y<dimensoes[2] and y>dimensoes[3])) and (y-(dimensoes[2]/2)) < (larguraDoGol/2 + 2)):
            passaPertoDoGol = True
            break
            loopMustBreak = True
        if loopMustBreak: break
        x += float(vetorVelocidadeBolaNormalizado[0]) #Move (x,y) na reta suporte
        y += float(vetorVelocidadeBolaNormalizado[1])
        i += 1


#?????Porque isso não funciona?????
#calcula o número absoluto de chutes a gols e gols de cada robô e salva dentro de cada robõ mesmo
#def calculaChutesEGols():
#    totalGols = 0
#    for i in range(1,len(log)-2):
#        if(foiChuteAoGol(i)==True):
#            quemChutouABola(i).chutesAoGol += 1
#            #se houve um gol sem que ninguém possuisse a bola, aumenta a contagem de gols de quem chutou a bola
#            j = i+1
#            while(roboEmPosseDaBola(j)==None):
#                for t in game.teams:
#                    if(foiGol(j)): 
#                        quemChutouABola(i).gols += 1
#                        totalGols += 1
#                j += 1 


#exportar tudo para csv
#mostrar dados em chart.js
#mapa de temperatura da posição da bola e de cada jogador e cada time utilizando heatmap.js (para saber se um jogador está mantendo sua posição certa, etc)


#TODO:
#Adicionar no futuro:
#efetividade do goleiro em defender chutes ao gol
#quantidade e taxa de passes bem sucedidos de cada time e jogador
#quantidade de assistências (passes que levam a gols