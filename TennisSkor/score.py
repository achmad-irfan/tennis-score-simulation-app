from copy import deepcopy

# Atribut dalam objek player
player_attrs= [
            "point", "tiebreak_point_win", "ace", "double_fault", "winner", 
            "unforced_error", "first_serve_total", "second_serve_total", 
            "total_service", "first_serve_win", "second_serve_win", 
            "break_point", "break_point_win", "return_point", 
            "return_point_win", "total_point", "forced_error", "set_win", 
        ]
# Atribut dalam objek match , dibedakan berdasarkan value default atribut
match_attrs= {"data_int":['current_set', "current_tiebreak" ],
                "data_bool": ["is_tiebreak", "finish"],
                "data_none": ['match_winner', "match_loser","status"],
                "data_list" :["score", "set_winner", "last_points"]}

# Tipe data default dari atribut objek match
type_defaults = {
    "data_int": 0,
    "data_bool": False,
    "data_none": None,
    "data_list": []
}

# Atribut total data statistik 2 pemain
total_stats = ["ace", "double_fault", "winner", 
              "unforced_error", "forced_error", "total_point"]

# Atribut presentase service dan return pemain
service_stats = ["first_serve", "return_point","first_serve_win", 
                 "second_serve_win","break_point_win"]

class Player:
    def __init__(self,name):
        self.name=name
        self.sets=[0,0,0]
        for attr in player_attrs:
            setattr(self,attr, 0)
            
    def __str__(self):
        return f'{self.name}'
        
class Match:
    def __init__(self,p1,p2,first_server):
        self.p1=Player(p1)
        self.p2=Player(p2)
        self.first_server=first_server
        self.current_server = self.p1

        # looping inisialisasi atribut
        for group, attrs in match_attrs.items():
            for attr in attrs:
                default = type_defaults[group]
                if isinstance(default, list):
                    setattr(self, attr, default.copy())
                else:
                    setattr(self, attr, default)
        
    def check_match_finish(self,player,opponent):
        if player.set_win ==  2 or opponent.set_win == 2:
            self.finish=True
            if player.set_win > opponent.set_win:
                self.match_winner = player
                self.match_loser  = opponent
            else:
                self.match_winner = opponent
                self.match_loser  = player
            self.scoring()
            print("Finish")
        
    def tiebreak_scoring(self,player,opponent):
        self.current_tiebreak +=1
        self.change_server_tiebreak()
        player.tiebreak_point_win += 1
        player.total_point +=1
        if player.tiebreak_point_win >= 7 and (player.tiebreak_point_win - opponent.tiebreak_point_win) >= 2:
            player.sets[self.current_set] = 7
            opponent.sets[self.current_set] = 6
            print("Set selesai via tiebreak")
            self.current_set += 1
            self.is_tiebreak = False
            player.set_win +=1
            player.tiebreak_point_win = 0
            opponent.tiebreak_point_win = 0
            self.check_match_finish(player,opponent)
 
    def check_tiebreak(self,player, opponent):
        print("Tie Break! Mode")
        self.is_tiebreak = True
        player.point = 0
        opponent.point = 0

    def check_set_finished(self, player, opponent):
        if player.sets[self.current_set] == 6 and opponent.sets[self.current_set] == 6:
            self.check_tiebreak(player, opponent)
            return

        if player.sets[self.current_set] >= 6 and (player.sets[self.current_set] - opponent.sets[self.current_set] >= 2):
            print(f"set {self.current_set+1} selesai")
            self.current_set += 1
            player.point = 0
            opponent.point = 0
            player.set_win +=1
            if player == self.p1:
                self.set_winner.append("p1")
            else:
                self.set_winner.append("p2")
            
            
    def win_game(self,player,opponent):
        self.increment_break_point_win(player)
        player.sets[self.current_set] += 1
        self.change_server()
        player.point = 0
        opponent.point = 0
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
            shot_player.double_fault +=1
            self.status= f"*Double Fault from {shot_player}"
            
        elif shot == "fe":
            shot_player.forced_error += 1
            self.status= f"*Forced Error from {shot_player}"
            
        elif shot == "ue":
            shot_player.unforced_error +=1
            self.status= f"*Unforced Error from {shot_player}"
            
    def break_point_check(self):
        server = self.current_server
        returner = self.p1 if server == self.p2 else self.p2

        if (returner.point == 40 and server.point != 40) or returner.point == "AD":
            returner.break_point += 1
            print("break point")
            
    def increment_break_point_win(self, player):
        if player != self.current_server:
            player.break_point_win +=1
            
    def serve_win(self, player, serve_type):
        if serve_type == "first":
            player.first_serve_win += 1
            # self.update_serve_pct(player)
        else:
            player.second_serve_win += 1
            # self.update_serve_pct(player)
        
    def serve_types(self, serve_type):
        if self.current_server==self.p1:
            self.p1.total_service += 1
            self.p2.return_point +=1
        else:
            self.p2.total_service += 1
            self.p1.return_point +=1
            
        if serve_type == "first":
            self.current_server.first_serve_total += 1
        else:
            self.current_server.second_serve_total +=1
    
    def win_point(self,player,opponent,pointWinner, serve_type):  
        self.serve_types(serve_type)  
        self.type_shot(pointWinner)
       
        if player == "p1":
            player = self.p1
            opponent = self.p2
            self.last_points.append("p1")
        elif player == "p2":
            player = self.p2
            opponent = self.p1
            self.last_points.append("p2")
            
        self.last_points= self.last_points[-15:]
        
        if self.finish:
            print(f"Pertandingan Selesai")
            return
            
        if self.is_tiebreak:
            print("MODE TIEBREAK START")
            self.tiebreak_scoring(player, opponent)
            return
        
        player.total_point +=1
        if player == self.current_server:
            self.serve_win(player, serve_type)
        else:
            player.return_point_win +=1
            
        if player.point == 0: 
            player.point = 15
           
        elif player.point == 15:
            player.point = 30
           
        elif player.point == 30:
            player.point = 40
           
        elif player.point == 40 and opponent.point == 40:
            player.point = "AD"
            opponent.point = "-"
            
        elif player.point == "-":
            player.point = 40
            opponent.point = 40
           
        elif player.point == "AD":
            self.win_game(player, opponent)
            
        elif player.point == 40 and opponent.point != 40:
            self.win_game(player, opponent)
            
        self.break_point_check()
            
    def scoring(self):
        self.score = [] 
        for i in range(self.current_set):
            if self.match_winner == self.p1:
                self.score.append(f"{self.p1.sets[i]}-{self.p2.sets[i]}")
            else:
                self.score.append(f"{self.p2.sets[i]}-{self.p1.sets[i]}")

        self.score = " ".join(self.score)
        
    def change_server(self):
        if self.current_server == self.p1:
            self.current_server = self.p2
        else:
            self.current_server = self.p1
    
    def change_server_tiebreak(self):
        if self.current_tiebreak % 2 == 1:
            self.change_server()      
    

 
    
    
    
class MatchSerializer:
    def __init__(self, match):
        self.match = match
        
    def calc_pct(self, win, total): 
        return round((win / total) * 100) if total else 0

    def get_player_data(self, player):
        # Ambil semua atribut player + persentase stats + sets
        player_data = {}
        for attr in player_attrs:
            value = getattr(player, attr)
            player_data[attr] = value
            
            
        # Khusus atribut sets pada player
        player_data['sets'] = player.sets
        player_data['name']=  player.name

        # Persentase service & points
        player_data.update({
            "first_serve_pct": self.calc_pct(player.first_serve_total, player.total_service),
            "second_serve_win_pct": self.calc_pct(player.second_serve_win, player.second_serve_total),
            "first_serve_win_pct": self.calc_pct(player.first_serve_win, player.first_serve_total),
            "return_point_pct": self.calc_pct(player.return_point_win, player.return_point),
            "break_point_win_pct": self.calc_pct(player.break_point_win, player.break_point),
        })
        
        return player_data

    def totals_stats_data(self):
        # Hitung persentase total stats antar pemain
        totals = {}
        for stat in total_stats:
            total = getattr(self.match.p1, stat) + getattr(self.match.p2, stat)
            totals[f"total_{stat}_pct1"] = self.calc_pct(getattr(self.match.p1, stat), total)
            totals[f"total_{stat}_pct2"] = self.calc_pct(getattr(self.match.p2, stat), total)
        
        return totals

    def match_info(self):
        match_stat = {}
        
        for group, attrs in match_attrs.items():
            for attr in attrs:
                match_stat[attr] = getattr(self.match, attr, None)
        
        match_stat.update({
        "current_server": "p1" if self.match.current_server == self.match.p1 else "p2",
        "match_winner": self.match.match_winner.name if self.match.match_winner else None,
        "match_loser": self.match.match_loser.name if self.match.match_loser else None,
        })
        
        return match_stat

    def to_dict(self):
        # Kembalikan dictionary final skor + info match + totals
        return {
            "p1": self.get_player_data(self.match.p1),
            "p2": self.get_player_data(self.match.p2),
            "totals": self.totals_stats_data(), 
            **self.match_info()
        }