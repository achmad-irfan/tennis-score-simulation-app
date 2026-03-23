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
        self.totalservice=0
        self.firstservetotal=0
        self.secondservetotal=0
        self.firstservewin=0
        self.secondservewin=0
        self.totalpoint=0
        self.servepoint=0
        self.totalpointsvr=0
        self.breakpoint=0
        self.breakpointwon=0
        self.returnpoint=0
        self.returnpointwon=0
        self.fe=0 
    
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
        self.status=None
        self.set_winner= []
        self.lastpoints= []
        # sementara default server p1 (belum pakai input user)
        self.current_server = self.p1
        
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
        player.totalpoint +=1
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
        if player.set[self.current_set] == 2 and opponent.set[self.current_set] == 2:
            self.check_tiebreak(player, opponent)
            return

        if player.set[self.current_set] >= 6 and (player.set[self.current_set] - opponent.set[self.current_set] >= 2):
            print(f"set {self.current_set+1} selesai")
            self.current_set += 1
            player.pt = 0
            opponent.pt = 0
            player.set_won +=1
            if player == self.p1:
                self.set_winner.append("p1")
            else:
                self.set_winner.append("p2")
            
            
    def win_game(self,player,opponent):
        self.breakpointwon(player)
        player.set[self.current_set] += 1
        self.change_server()
        player.pt = 0
        opponent.pt = 0
        self.check_set_finished(player, opponent)
        self.check_match_finish(player,opponent)
        self.status = f"*Game {player}"
    
   
     
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
            self.status= f"*Ace from {shot_player}"
            
        elif shot == "winner":
            shot_player.winner +=1
            self.status= f"*Winner from {shot_player}"
            
        elif shot == "df":
            shot_player.df +=1
            self.status= f"*Double Fault from {shot_player}"
            
        elif shot == "fe":
            shot_player.fe += 1
            self.status= f"*Forced Error from {shot_player}"
            
        elif shot == "ue":
            shot_player.ue +=1
            self.status= f"*Unforced Error from {shot_player}"
            
           
    
    def breakpoint_check(self):
        server = self.current_server
        returner = self.p1 if server == self.p2 else self.p2

        if (returner.pt == 40 and server.pt != 40) or returner.pt == "AD":
            returner.breakpoint += 1
            print("break point")
            
    def breakpointwon(self, player):
        if player != self.current_server:
            player.breakpointwon +=1
            
    def serve_win(self, player, serve_type):
        if serve_type == "first":
            player.firstservewin += 1
            # self.update_serve_pct(player)
        else:
            player.secondservewin += 1
            # self.update_serve_pct(player)
        
         
    
    def serve_types(self, serve_type):
        if self.current_server==self.p1:
            self.p1.totalservice += 1
            self.p2.returnpoint +=1
        else:
            self.p2.totalservice += 1
            self.p1.returnpoint +=1
            
        if serve_type == "first":
            self.current_server.firstservetotal += 1
        else:
            self.current_server.secondservetotal +=1
    
    
    def win_point(self,player,opponent,pointWinner, serve_type):  
        self.serve_types(serve_type)  
        self.type_shot(pointWinner)
       
        if player == "p1":
            player = self.p1
            opponent = self.p2
            self.lastpoints.append("p1")
        elif player == "p2":
            player = self.p2
            opponent = self.p1
            self.lastpoints.append("p2")
            
        self.lastpoints= self.lastpoints[-15:]
        
        if self.finish:
            print(f"Pertandingan Selesai")
            return
            
        if self.tiebreak:
            print("MODE TIEBREAK START")
            self.tiebreak_scoring(player, opponent)
            return
        
        player.totalpoint +=1
        if player == self.current_server:
            self.serve_win(player, serve_type)
        else:
            player.returnpointwon +=1
            
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
            
        self.breakpoint_check()
            
    def scoring(self):
        self.score = [] 
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
        if self.current_tie_break % 2 == 1:
            self.change_server()
            
    def calc_pct(self, win, total):          
        return round((win / total) * 100) if total else 0        
  
    def get_score(self):
       
        stats = ["ace", "df", "winner", "ue", "fe", "totalpoint"]
        new_stats={}
        for stat in stats:
            new_stats["total_"+stat]=getattr(self.p1, stat) + getattr(self.p2, stat)
        players = {"p1": self.p1, "p2": self.p2}
                    
        score = {
        key: {
            "pt": p.pt,
            "set": p.set,
            "tb": p.tb,
            "set_won": p.set_won,
            "totalpoint": p.totalpoint,
            "ace": p.ace,
            "df": p.df,
            "winner": p.winner,
            "ue": p.ue,
            "fe" : p.fe,
            "firstservetotal" : p.firstservetotal,
            "secondservetotal":p.secondservetotal,
            "totalservice" : p.totalservice,
            "firstservewin": p.firstservewin,
            "secondservewin" : p.secondservewin,
            "breakpoint": p.breakpoint,
            "breakpointwon":p.breakpointwon,
            "returnpoint": p.returnpoint,
            "returnpointwon": p.returnpointwon, 
            "first_serve_pct" : self.calc_pct(p.firstservetotal, p.totalservice),
            "return_pct" : self.calc_pct(p.returnpointwon, p.returnpoint),
            "first_serve_win_pct": self.calc_pct(p.firstservewin, p.firstservetotal),
            "second_serve_win_pct":self.calc_pct(p.secondservewin, p.secondservetotal),
            "break_point_won_pct": self.calc_pct(p.breakpointwon, p.breakpoint),
            "total_ace": self.calc_pct(p.ace,new_stats['total_ace']),
            "total_df" : self.calc_pct(p.df,new_stats['total_df']),
            "total_fe" : self.calc_pct(p.fe, new_stats['total_fe']),
            "total_ue" : self.calc_pct(p.ue, new_stats['total_ue']),
            "total_winner" : self.calc_pct(p.winner, new_stats['total_winner']),
            "total_totalpoint" : self.calc_pct(p.totalpoint, new_stats['total_totalpoint'])
        }
        
        for key, p in players.items()}
        score.update({
        "finish": self.finish,
        "result": {"winner": self.winner, "loser": self.loser},
        "score": self.score,
        "current_server": "p1" if self.current_server == self.p1 else "p2",
        "status": self.status, 
        "set_winner": self.set_winner,
        "lastpoints" : self.lastpoints,
        "current_set":self.current_set,
        "tiebreak": self.tiebreak,
        "current_tie_break": self.current_tie_break
        })
        
        return score
    