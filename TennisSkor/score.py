class Player:
    def __init__(self,name):
        self.name=name
        self.pt=0
        self.tb=0
        self.set=[0,0,0]
        
class Match:
    def __init__(self,p1,p2, max_game=6):
        self.p1=Player(p1)
        self.p2=Player(p2)
        self.max_game=max_game
        self.current_set=0
        self.tiebreak=False
        
    def tiebreak_scoring(self,player,opponent):
        player.tb += 1
        if player.tb >= 7 and (player.tb - opponent.tb) >= 2:
            player.set[self.current_set] = 7
            opponent.set[self.current_set] = 6
            print("Set selesai via tiebreak")
            self.current_set += 1
            self.tiebreak = False
            player.tb = 0
            opponent.tb = 0
            
    def check_tiebreak(self,player, opponent):
        print("Tie Break! Mode")
        self.tiebreak = True
        player.pt = 0
        opponent.pt = 0

    def check_set_finished(self, player, opponent):
        if player.set[self.current_set] == 6 and opponent.set[self.current_set] == 6:
            self.check_tiebreak(player, opponent)
            return

        if player.set[self.current_set] >= 6 and (player.set[self.current_set] - opponent.set[self.current_set] >= 2):
            print(f"set {self.current_set+1} selesai")

            self.current_set += 1
            player.pt = 0
            opponent.pt = 0
            
        

    def win_point(self,player,opponent):
        if player == "p1":
            player = self.p1
            opponent = self.p2
        elif player == "p2":
            player = self.p2
            opponent = self.p1
            
        if self.tiebreak:
            print("MODE TIEBREAK START")
            self.tiebreak_scoring(player, opponent)
            return
        
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
            player.set[self.current_set] += 1
            player.pt = 0
            opponent.pt = 0
            self.check_set_finished(player, opponent)
        elif player.pt == 40 and opponent.pt != 40:
            player.set[self.current_set] += 1
            player.pt = 0
            opponent.pt = 0
            self.check_set_finished(player, opponent)
                
    def get_score(self):
        score= {
        "p1": {"pt": self.p1.pt, "set": self.p1.set, "tb":self.p1.tb},
        "p2": {"pt": self.p2.pt, "set": self.p2.set, "tb":self.p2.tb} }
        
        return score