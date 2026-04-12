from datetime import datetime
from .calculator import calc_pct, build_player_stats

# Atribut dalam objek player
player_attrs= [
            "point", "tiebreak_point_win", "ace", "double_fault", "winner", 
            "unforced_error", "first_serve_total", "second_serve_total", 
            "total_service", "first_serve_win", "second_serve_win", 
            "break_point", "break_point_win", "return_point", 
            "return_point_win", "total_point", "forced_error", "set_win", "game_point"
        ]
# Atribut dalam objek match , dibedakan berdasarkan value default atribut
match_attrs= {"data_int":['current_set', "current_tiebreak" ],
                "data_bool": ["is_tiebreak", "finish", "is_last_set", "is_changing_game"],
                "data_none": ['match_winner', "match_loser","status", "first_server_tiebreak", "last_winner_point"],
                "data_list" :["score", "set_winner", "last_points", "history", "set_snapshot", "all_set_snapshot"],
                "data_dict": []}

# Tipe data default dari atribut objek match
type_defaults = {
    "data_int": 0,
    "data_bool": False,
    "data_none": None,
    "data_list": [],
    "data_dict" : {}
}

player_attr_list = ['sets','tiebreak_display_score' ]

# Atribut total data statistik 2 pemain
total_stats = ["ace", "double_fault", "winner", 
              "unforced_error", "forced_error", "total_point"]

# Atribut presentase service dan return pemain
service_stats = ["first_serve_total", "return_point","first_serve_win",  
                 "second_serve_win","break_point_win", "return_point_win"]


# Stat for table statistic
table_match_stats = [
    {"key": "ace", "label": "Ace"},
    {"key": "double_fault", "label": "Double Fault"},
    {"type": "separator"},
    {"key": "first_serve_total", "label": "First Serve",  "pair": "total_service" },
    {"key": "first_serve_win", "label": "First Serve Win", "pair" :"first_serve_total"},
    {"key": "second_serve_win", "label": "Second Serve Win", "pair": "second_serve_total"},
    {"type": "separator"},
    {"key": "return_point_win", "label": "Return Point", "pair": "return_point"},
    {"key": "break_point_win", "label": "Break Point", "pair": "break_point"},
    {"type": "separator"},
    {"key": "winner", "label": "Winner"},
    {"key": "forced_error", "label": "Forced Error"},
    {"key": "unforced_error", "label": "Unforced Error"},
    {"key": "total_point", "label": "Total Point"},
]
  
for stat in table_match_stats:
    key = stat.get("key")
    
    if key in service_stats:
        stat["category"] = "service"
    else:
        stat["category"] = "general"

for stat in table_match_stats:
    key = stat.get("key")
    stat["pct"]= f"{key}_pct"
        
        
class Player:
    def __init__(self,name):
        self.name=name
        self.sets=[0,0,0]
        self.tiebreak_display_score = [0,0,0]
        self.total_statistics_all_set= []
        for attr in player_attrs:
            setattr(self,attr, 0)
            
    def __str__(self):
        return f'{self.name}'
        
class Match:
    def __init__(self,p1,p2,first_server, final_set):
        self.p1=Player(p1)
        self.p2=Player(p2)
        self.first_server=first_server
        self.current_server = self.p1
        self.start_time = datetime.now() 
        self.duration = [0,0,0]
        self.final_set= final_set

        # looping inisialisasi atribut
        for group, attrs in match_attrs.items():
            for attr in attrs:
                default = type_defaults[group]
                if isinstance(default, list):
                    setattr(self, attr, default.copy())
                else:
                    setattr(self, attr, default)
                    
        self.scoring = ScoringSystem()
        
    def player_category(self, point_event):
        player_id, shot = point_event.split("_")
        if shot in ['df', 'ue']:
            if player_id == "p2":
                player = self.p1
                opponent = self.p2
            else:
                player = self.p2
                opponent = self.p1
                
        else:
            if player_id == "p2":
                player = self.p2
                opponent = self.p1
            else:
                player = self.p1
                opponent = self.p2
                
        return player, opponent
        
    def play_point(self, point_event, serve_type):
        player, opponent = self.player_category(point_event)
        self.history.append({"event": point_event, "serve": serve_type})
        
        self.scoring.process_point(self, player, opponent, point_event, serve_type)          
            
    
    def cancel_point(self):
        if self.history:
            self.history.pop()
    
        # Simpan start_time sebelum bikin match baru
        start_time_backup = self.start_time
        duration_backup = self.duration.copy()
        
        # Buat objek baru
        new_match = Match(self.p1.name, self.p2.name, self.first_server, self.final_set)
        
        for shot in self.history:
            new_match.play_point(shot["event"], shot["serve"])
        
        new_match.start_time = start_time_backup
        new_match.duration = duration_backup
        
        return new_match

class ScoringSystem:
    def process_point(self, match, player, opponent, point_event, serve_type):
        # 1. Serve & shot
        self.serve_types(match, serve_type)
        self.type_shot(match, point_event)

        # 2. simpan history
        if player == match.p1:
            match.last_points.append("p1")
        else:
            match.last_points.append("p2")

        match.last_points = match.last_points[-15:]

        # 3. kalau match selesai
        if match.finish:
            return

        # 4. tiebreak mode
        if match.is_tiebreak:
            self.tiebreak_scoring(match, player, opponent)
            return

        # 5. normal scoring
        player.total_point += 1

        if player == match.current_server:
            self.serve_win(player, serve_type)
        else:
            player.return_point_win += 1

        self.update_point(match,player, opponent)

        self.break_point_check(match)
    
    def update_point(self, match, player, opponent):
        player.game_point +=1
        if player == match.p1:
            match.last_winner_point= "p1"
        else:
            match.last_winner_point= "p2"
            
        self.duration(match)
        match.is_changing_game = False
        
        if player.game_point >= 4 and (player.game_point - opponent.game_point) >= 2:
            self.win_game(match, player, opponent)
            player.game_point = 0
            opponent.game_point = 0
            
        self.update_display_score(match.p1,match.p2)
    
    def update_display_score(self, p1, p2):
        mapping = [0, 15, 30, 40]

        if p1.game_point >= 3 and p2.game_point >= 3:
            if p1.game_point == p2.game_point:
                p1.point = 40
                p2.point = 40
            elif p1.game_point > p2.game_point:
                p1.point = "AD"
                p2.point = "-"
            else:
                p1.point = "-"
                p2.point = "AD"
        else:
            p1.point = mapping[p1.game_point]
            p2.point = mapping[p2.game_point]
    
    def win_game(self, match, player, opponent):
        self.increment_break_point_win(match, player)
        player.sets[match.current_set] += 1
        self.change_server(match)
        match.is_changing_game = True

        player.point = 0
        opponent.point = 0
        
        self.check_last_set(match)
        self.check_set_finished(match, player, opponent)
        self.check_match_finish(match, player, opponent)

        match.status = f"*Game {player}"
        
    def check_last_set(self, match):
        match.is_last_set = (match.current_set == 2)

        if match.is_last_set :
            print("MASUK LAST SET")
            self.check_super_tiebreak_only(match)
        else:
            match.is_tiebreak = False
            
            
    def check_super_tiebreak_only(self,match):
        if match.final_set == "super_tiebreak_only" :
            print("Masuk SUPER TIE BREAK")
            match.is_tiebreak = True
        else:
            match.is_tiebreak = False
            
    def check_set_finished(self, match, player, opponent):
        if player.sets[match.current_set] == 6 and opponent.sets[match.current_set] == 6:
            self.check_tiebreak(match, player, opponent)
            return

        if player.sets[match.current_set] >= 2 and (player.sets[match.current_set] - opponent.sets[match.current_set] >= 1):
            match.is_changing_game = True
            match.current_set += 1
            self.check_last_set(match)
            match.start_time = datetime.now()
            self.get_set_snapshot(match)
            player.point = 0
            opponent.point = 0
            self.reset_atribut_after_set(match.p1)
            self.reset_atribut_after_set(match.p2)

            player.set_win += 1

            if player == match.p1:
                match.set_winner.append("p1")
            else:
                match.set_winner.append("p2")
    
    def tiebreak_scoring(self, match, player, opponent):
        match.current_tiebreak += 1
        self.get_first_server_tiebreak(match)
        self.change_server_tiebreak(match)
        
        player.tiebreak_point_win += 1
        player.tiebreak_display_score[match.current_set] += 1
        player.total_point += 1
        
        tie_break_point_min_won = 7 
        if match.is_last_set:
            if match.final_set in ["super_tiebreak", "super_tiebreak_only"]:
                tie_break_point_min_won = 10
            elif match.final_set == "normal":
                tie_break_point_min_won = 7
        
        if player.tiebreak_point_win >= tie_break_point_min_won and (player.tiebreak_point_win - opponent.tiebreak_point_win) >= 2:
            player.sets[match.current_set] = 7
            opponent.sets[match.current_set] = 6
           
            match.current_set += 1
            self.check_last_set(match)
            match.start_time = datetime.now()
            self.get_set_snapshot(match)
            self.get_current_server_after_tiebreak(match)
            self.reset_atribut_after_set(match.p1)
            self.reset_atribut_after_set(match.p2)

            player.set_win += 1

            player.tiebreak_point_win = 0
            opponent.tiebreak_point_win = 0

            self.check_match_finish(match, player, opponent)

    def get_first_server_tiebreak(self, match):
        if match.current_tiebreak == 1:
            if match.current_server == match.p1:
                match.first_server_tiebreak = "p1"
            else:
                match.first_server_tiebreak = "p2"
                
    def get_current_server_after_tiebreak(self, match):
        if match.first_server_tiebreak == "p1":
            match.current_server = match.p2
        else:
            match.current_server = match.p1
            
    def check_match_finish(self, match, player, opponent):
        if player.set_win == 2 or opponent.set_win == 2:
            match.finish = True

            if player.set_win > opponent.set_win:
                match.match_winner = player
                match.match_loser = opponent
            else:
                match.match_winner = opponent
                match.match_loser = player

            self.get_scoring_display(match)
        
            self.get_aggregate_snapshot(match)
            
    def serve_types(self, match, serve_type):
        if match.current_server == match.p1:
            match.p1.total_service += 1
            match.p2.return_point += 1
        else:
            match.p2.total_service += 1
            match.p1.return_point += 1

        if serve_type == "first":
            match.current_server.first_serve_total += 1
        else:
            match.current_server.second_serve_total += 1


    def serve_win(self, player, serve_type):
        if serve_type == "first":
            player.first_serve_win += 1
        else:
            player.second_serve_win += 1


    def type_shot(self, match, point_event):
        player_id, shot = point_event.split("_")

        player = match.p1 if player_id == "p1" else match.p2

        if shot == "ace":
            player.ace += 1
            match.status = f"*Ace from {player}"
        elif shot == "winner":
            player.winner += 1
            match.status = f"*Winner from {player}"
        elif shot == "df":
            player.double_fault += 1
            match.status = f"*Double Fault from {player}"
        elif shot == "fe":
            player.forced_error += 1
            match.status = f"*Forced Error from {player}"
        elif shot == "ue":
            player.unforced_error += 1
            match.status = f"*Unforced Error from {player}"


    def break_point_check(self, match):
        server = match.current_server
        returner = match.p1 if server == match.p2 else match.p2

        if (returner.point == 40 and server.point != 40) or returner.point == "AD":
            returner.break_point += 1


    def increment_break_point_win(self, match, player):
        if player != match.current_server:
            player.break_point_win += 1


    def change_server(self,match):
        if match.current_server == match.p1:
            match.current_server = match.p2
        else:
            match.current_server = match.p1

    def change_server_tiebreak(self, match):
        if match.current_tiebreak % 2 == 1:
            match.current_server = match.p2 if match.current_server == match.p1 else match.p1
  
    def check_tiebreak(self, match, player, opponent):
        match.is_tiebreak = True
        player.point = 0
        opponent.point = 0


    def get_scoring_display(self, match):
        match.score = []
        match_winner = match.match_winner
        match_loser = match.match_loser

        for i in range(match.current_set):
            # Ambil nilai set winner dan loser
            winner_set = match_winner.sets[i]
            loser_set = match_loser.sets[i]

            if i == match.current_set  and match.final_set == "super_tiebreak_only":
                match.score.append(f"[{match_winner.tiebreak_display_score[i]}-{match_loser.tiebreak_display_score[i]}]")
            elif max(winner_set, loser_set) == 7 and min(winner_set, loser_set) == 6:
                match.score.append(f"{winner_set}-{loser_set}<sup>({match_winner.tiebreak_display_score[i]}-{match_loser.tiebreak_display_score[i]})</sup>")
            else:
                match.score.append(f"{winner_set}-{loser_set}")       
            
        match.score = "  ".join(match.score)
        
    def duration(self, match):
        # Hitung durasi set sekarang
            
        duration = datetime.now() - match.start_time
        minutes = int(duration.total_seconds() // 60)
        
        match.duration[match.current_set] = minutes
        
    
    def reset_atribut_after_set(self,player):
        resettable_attrs = [
            "ace", "double_fault", "winner", "unforced_error",
            "forced_error", "total_point", "total_service",
            "first_serve_total", "first_serve_win",
            "second_serve_total", "second_serve_win",
            "return_point", "return_point_win",
            "break_point", "break_point_win",
            "game_point", "tiebreak_point_win" ]  
                     
        for attr in resettable_attrs:
            setattr(player, attr, 0)
        
    def get_set_snapshot(self, match):
         # Ambil stats player
        p1_data_snapshot = build_player_stats(match.p1, match.p2)
        p2_data_snapshot = build_player_stats(match.p2, match.p1)

        snapshot = {
            "p1": p1_data_snapshot,
            "p2": p2_data_snapshot,
            "match": {
                "current_set": match.current_set,
                "current_server": "p1" if match.current_server == match.p1 else "p2",
                "is_tiebreak": match.is_tiebreak,
                "current_tiebreak": match.current_tiebreak,
                "status": match.status,
                "set_winner": match.set_winner.copy(),
                "duration": match.duration.copy(),
                "start_time": match.start_time.isoformat()
            },
        }
        match.set_snapshot.append(snapshot)     
        
    def get_aggregate_snapshot(self,match):
        from .score import player_attrs

        result_all_set = {
            "p1": {},
            "p2": {},
            "match": {}
        }

        # ambil semua key numerik dari player_attrs
        for player in ["p1", "p2"]:
            for attr in player_attrs:
                result_all_set[player][attr] = sum(
                    snap[player].get(attr, 0) for snap in match.set_snapshot
                )
        p1_data_all_snapshot = build_player_stats(result_all_set['p1'], result_all_set['p2'])
        p2_data_all_snapshot = build_player_stats(result_all_set['p2'], result_all_set['p1'])
        all_snapshot={
            "p1" : p1_data_all_snapshot,
            "p2" : p2_data_all_snapshot        }
        
        
        match.all_set_snapshot = all_snapshot
       
class MatchSerializer:
    def __init__(self, match):
        self.match = match
    

    def match_info(self):
        match_stat = {}
        
        for group, attrs in match_attrs.items():
            for attr in attrs:
                match_stat[attr] = getattr(self.match, attr, None)
        
        match_stat.update({
        "current_server": "p1" if self.match.current_server == self.match.p1 else "p2",
        "match_winner": self.match.match_winner.name if self.match.match_winner else None,
        "match_loser": self.match.match_loser.name if self.match.match_loser else None,
        "start_time": self.match.start_time.isoformat(),
        "duration": self.match.duration,
        "final_set": self.match.final_set
        })
        
        return match_stat

    def to_dict(self):
        # Kembalikan dictionary final skor + info match + totals
        return {
            "p1": build_player_stats(self.match.p1, self.match.p2),
            "p2": build_player_stats(self.match.p2, self.match.p1),
            **self.match_info()
        }
