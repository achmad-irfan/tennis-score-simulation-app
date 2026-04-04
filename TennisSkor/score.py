from datetime import datetime

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
                "data_bool": ["is_tiebreak", "finish"],
                "data_none": ['match_winner', "match_loser","status", "first_server_tiebreak"],
                "data_list" :["score", "set_winner", "last_points", "history", "set_snapshot"],
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

# Stat untuk total pada tabel
for stat in table_match_stats:
    if "key" in stat and stat["key"]:  
        stat["pct_key_p1"] = f"total_{stat['key']}_pct1"
        stat["pct_key_p2"] = f"total_{stat['key']}_pct2"
    
for stat in table_match_stats:
    key = stat.get("key")
    
    if key in service_stats:
        stat["category"] = "service"
    else:
        stat["category"] = "general"

for stat in table_match_stats:
    if stat["category"] == "service":
        stat['pct']= f"{stat['key']}_pct"
        
        
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
    def __init__(self,p1,p2,first_server):
        self.p1=Player(p1)
        self.p2=Player(p2)
        self.first_server=first_server
        self.current_server = self.p1
        self.start_time = datetime.now() 
        self.duration = [0,0,0]

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
        new_match = Match(self.p1.name, self.p2.name, self.first_server)
        
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
        self.duration(match)
        
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

        

        player.point = 0
        opponent.point = 0

        self.check_set_finished(match, player, opponent)
        self.check_match_finish(match, player, opponent)

        match.status = f"*Game {player}"
        
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
            
    def tiebreak_scoring(self, match, player, opponent):
        match.current_tiebreak += 1
        self.get_first_server_tiebreak(match)
        self.change_server_tiebreak(match)
        

        player.tiebreak_point_win += 1
        player.tiebreak_display_score[match.current_set] += 1
        player.total_point += 1

        if player.tiebreak_point_win >= 7 and (player.tiebreak_point_win - opponent.tiebreak_point_win) >= 2:
            player.sets[match.current_set] = 7
            opponent.sets[match.current_set] = 6
           
            match.current_set += 1
            match.start_time = datetime.now()
            match.is_tiebreak = False
            self.get_set_snapshot(match)
            self.get_current_server_after_tiebreak(match)
            self.reset_atribut_after_set(match.p1)
            self.reset_atribut_after_set(match.p2)

            player.set_win += 1

            player.tiebreak_point_win = 0
            opponent.tiebreak_point_win = 0

            self.check_match_finish(match, player, opponent)
    
    def check_set_finished(self, match, player, opponent):
        if player.sets[match.current_set] == 1 and opponent.sets[match.current_set] == 1:
            self.check_tiebreak(match, player, opponent)
            return

        if player.sets[match.current_set] >= 2 and (player.sets[match.current_set] - opponent.sets[match.current_set] >= 1):
            match.current_set += 1
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
        
        
    def check_match_finish(self, match, player, opponent):
        if player.set_win == 2 or opponent.set_win == 2:
            match.finish = True

            if player.set_win > opponent.set_win:
                match.match_winner = player
                match.match_loser = opponent
            else:
                match.match_winner = opponent
                match.match_loser = player

            self.scoring(match)
            match.p1.total_statistics_all_set = self.agregat_all_stat(match.set_snapshot, "p1")
            match.p2.total_statistics_all_set = self.agregat_all_stat(match.set_snapshot, "p2")
            
            
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


    def scoring(self, match):
        match.score = []
        match_winner = match.match_winner
        match_loser = match.match_loser

        for i in range(match.current_set):
            # Ambil nilai set winner dan loser
            winner_set = match_winner.sets[i]
            loser_set = match_loser.sets[i]

            # Tentukan apakah set ini tiebreak
            tiebreak_score = ""
            if max(winner_set, loser_set) == 7 and min(winner_set, loser_set) == 6:
                # Tampilkan skor tiebreak kalah saja
                if winner_set > loser_set:
                    tiebreak_score = f"({match_loser.tiebreak_display_score[i]})"
                    match.score.append(f"7-{loser_set}{tiebreak_score}")
                else:
                    tiebreak_score = f"({match_winner.tiebreak_display_score[i]})"
                    match.score.append(f"{tiebreak_score}{winner_set}-7")
             
            else:
                match.score.append(f"{winner_set}-{loser_set}")       
            
        match.score = "  ".join(match.score)
        
    def duration(self, match):
        # Hitung durasi set sekarang
            
        duration = datetime.now() - match.start_time
        minutes = int(duration.total_seconds() // 60)
        
        match.duration[match.current_set] = minutes
        
    def calc_pct(self, win, total):
        return round((win / total) * 100) if total else 0

    def build_service_pct(self, player):
        service_pct_map = {
        "first_serve_total_pct": ("first_serve_total", "total_service"),
        "first_serve_win_pct": ("first_serve_win", "first_serve_total"),
        "second_serve_win_pct": ("second_serve_win", "second_serve_total"),
        "return_point_win_pct": ("return_point_win", "return_point"),
        "break_point_win_pct": ("break_point_win", "break_point"),
    }

        result = {}

        for key, (win_attr, total_attr) in service_pct_map.items():
            win = getattr(player, win_attr)
            total = getattr(player, total_attr)
            result[key] = self.calc_pct(win, total)

        return result
    
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
        totals = {}

        for stat in total_stats:
            total = getattr(match.p1, stat) + getattr(match.p2, stat)
            totals[f"total_{stat}_pct1"] = self.calc_pct(getattr(match.p1, stat), total)
            totals[f"total_{stat}_pct2"] = self.calc_pct(getattr(match.p2, stat), total)

        p1_data = {
            attr: getattr(match.p1, attr)
            for attr in player_attrs + ["sets", "tiebreak_display_score"]
        }

        p2_data = {
            attr: getattr(match.p2, attr)
            for attr in player_attrs + ["sets", "tiebreak_display_score"]
        }

        for attr in service_stats:
            p1_data[attr] = getattr(match.p1, attr)
            p2_data[attr] = getattr(match.p2, attr)

        # === percentage stats ===
        p1_data.update(self.build_service_pct(match.p1))
        p2_data.update(self.build_service_pct(match.p2))

        snapshot = {
            "p1": p1_data,
            "p2": p2_data,
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
            "totals": totals
        }
        match.set_snapshot.append(snapshot)
    
    def agregat_all_stat(self, data, player):
        result = {}
        
        for stat in table_match_stats:
            if "key" not in stat:
                continue
            
            key = stat["key"]
            result[key] = sum(item[player].get(key, 0) for item in data)
        
            if "pair" in stat:
                pair = stat["pair"]
                if pair not in result:
                    result[pair] = sum(item[player].get(pair, 0) for item in data)

        return result
    
    
    
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
        player_data['tiebreak_display_score']= player.tiebreak_display_score
        player_data['total_statistics_all_set'] = player.total_statistics_all_set

        # Persentase service & points
        player_data.update({
            "first_serve_total_pct": self.calc_pct(player.first_serve_total, player.total_service),
            "second_serve_win_pct": self.calc_pct(player.second_serve_win, player.second_serve_total),
            "first_serve_win_pct": self.calc_pct(player.first_serve_win, player.first_serve_total),
            "return_point_win_pct": self.calc_pct(player.return_point_win, player.return_point),
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
        "start_time": self.match.start_time.isoformat(),
        "duration": self.match.duration
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
        
        
    