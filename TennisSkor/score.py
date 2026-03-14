class Player:
    def __init__(self,name):
        self.name=name
        self.pt=0
        self.tb=0
        self.set=[0,0,0]
        self.set_won=0
        self.ace=0
        self.df=0
        self.winner=0
        self.ue=0
        self.servpersen=0
        self.win1svr=0
        self.win2svr=0
        self.totalpoint=0
        self.servepoint=0
        self.returnpoint=0
        
    def __str__(self):
        return f'{self.name}'
        
        
class Match:
    def __init__(self,p1,p2,firstserver):
        self.p1=Player(p1)
        self.p2=Player(p2)
        self.current_set=0
        self.tiebreak=False
        self.current_tie_break=0
        self.finish=False
        self.winner=None
        self.loser=None
        self.score=[]
        self.firstserver=firstserver
        if firstserver == "p1":
            self.current_server = self.p1
        else:
            self.current_server = self.p2
        
    def check_match_finish(self,player,opponent):
        if player.set_won ==  2 or opponent.set_won == 2:
            self.finish=True
            if player.set_won > opponent.set_won:
                self.winner= player
                self.loser=opponent
            else:
                self.winner= opponent
                self.loser= player
                
            self.scoring()
            print("Finish")
        
    def tiebreak_scoring(self,player,opponent):
        self.current_tie_break +=1
        self.change_server_tiebreak()
        player.tb += 1
        if player.tb >= 7 and (player.tb - opponent.tb) >= 2:
            player.set[self.current_set] = 7
            opponent.set[self.current_set] = 6
            print("Set selesai via tiebreak")
            self.current_set += 1
            self.tiebreak = False
            player.set_won +=1
            player.tb = 0
            opponent.tb = 0
            self.check_match_finish(player,opponent)
            
    def check_tiebreak(self,player, opponent):
        print("Tie Break! Mode")
        self.tiebreak = True
        player.pt = 0
        opponent.pt = 0

    def check_set_finished(self, player, opponent):
        if player.set[self.current_set] == 6 and opponent.set[self.current_set] == 6:
            self.check_tiebreak(player, opponent)
            return

        if player.set[self.current_set] >= 2 and (player.set[self.current_set] - opponent.set[self.current_set] >= 2):
            print(f"set {self.current_set+1} selesai")

            self.current_set += 1
            player.pt = 0
            opponent.pt = 0
            player.set_won +=1
            
    def win_game(self,player,opponent):
        
        player.set[self.current_set] += 1
        self.change_server()
        player.pt = 0
        opponent.pt = 0
        self.check_set_finished(player, opponent)
        self.check_match_finish(player,opponent)
     
    def type_shot(self, pointWinner):
        player_id , shot = pointWinner.split("_")
        if player_id == "p1":
            shot_player = self.p1
            opponent = self.p2
        else:
            shot_player = self.p2
            opponent = self.p1
            
        if shot == "ace":
            shot_player.ace += 1
            print(f"Ace from {shot_player}")
            
        elif shot == "winner":
            shot_player.winner +=1
            print(f"Winner from {shot_player}")
            
        elif shot == "df":
            shot_player.df +=1
            print(f"Double Foult from {shot_player}")
            
        elif shot == "ue":
            shot_player.ue +=1
            print(f"Unforced error from {shot_player}")
            
        
               
    def win_point(self,player,opponent,pointWinner):    
        self.type_shot(pointWinner)
        
        if player == "p1":
            player = self.p1
            opponent = self.p2
        elif player == "p2":
            player = self.p2
            opponent = self.p1
        
        if self.finish:
            print(f"Pertandingan Selesai")
            return
            
        if self.tiebreak:
            print("MODE TIEBREAK START")
            self.tiebreak_scoring(player, opponent)
            return
        
        player.totalpoint +=1
         
        if player.pt == 0:
            player.pt = 15
           
        elif player.pt == 15:
            player.pt = 30
           
        elif player.pt == 30:
            player.pt = 40
           
        elif player.pt == 40 and opponent.pt == 40:
            player.pt = "AD"
            opponent.pt = "-"
            
        elif player.pt == "-":
            player.pt = 40
            opponent.pt = 40
           
        elif player.pt == "AD":
            self.win_game(player, opponent)
            
            
        elif player.pt == 40 and opponent.pt != 40:
            self.win_game(player, opponent)
            
    
    
    
    
    def scoring(self):
        for i in range(self.current_set):
            if self.winner == self.p1:
                self.score.append(f"{self.p1.set[i]}-{self.p2.set[i]}")
            else:
                self.score.append(f"{self.p2.set[i]}-{self.p1.set[i]}")

        self.score = " ".join(self.score)
        
    def change_server(self):
        if self.current_server == self.p1:
            self.current_server = self.p2
        else:
            self.current_server = self.p1
    
    def change_server_tiebreak(self):
        total = self.p1.tb + self.p2.tb

        if total % 2 == 1:
            self.change_server()
        
        
        
    def get_score(self):
        score= {
        "p1": {
            "pt": self.p1.pt, 
            "set": self.p1.set, 
            "tb":self.p1.tb, 
            "set_won": self.p1.set_won, 
            "tp": self.p1.totalpoint, 
            "ace": self.p1.ace,
            "df": self.p1.df,
            "winner": self.p1.winner,
            "ue": self.p1.ue,
            },
        "p2": {
            "pt": self.p2.pt, 
            "set": self.p2.set, 
            "tb":self.p2.tb, 
            "set_won": self.p2.set_won, 
            "tp": self.p2.totalpoint, 
            "ace": self.p2.ace,
            "df": self.p2.df,
            "winner": self.p2.winner,
            "ue": self.p2.ue,
            },
        "finish": self.finish,
        "result":{"winner":self.winner,"loser":self.loser},
        "score": self.score,
        "current_server": "p1" if self.current_server == self.p1 else "p2",
        }
        
        return score
    