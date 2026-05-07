from .score import Match, Player, MatchSerializer
from .list_wta_players import players
from .score import player_attrs, total_stats, match_attrs, service_stats
from datetime import datetime

def get_players_from_request(request):

    match_type = request.GET.get("match")
    if match_type == "single":
        p1= [request.GET.get('p1', '')]
        p2= [request.GET.get('p2', '')]
    elif match_type == "double":
        p1_team1 = request.GET.get('p1_team1','')
        p2_team1 = request.GET.get('p2_team1','')
        p1_team2 = request.GET.get('p1_team2','')
        p2_team2 = request.GET.get('p2_team2','')
        p1 = [p1_team1, p2_team1]
        p2 = [p1_team2, p2_team2]
    else:
        p1,p2= [], []
    
    first_server = request.GET.get("first_server")
    final_set_scoring= request.GET.get("final_set_scoring")
    
    return p1,p2,first_server, final_set_scoring, match_type


    
def profile(player_list, name):
    for player in player_list:
        if player['name'] == name:
            return player
    return None


        
def player_validation(request, p1,p2):
    if request.GET.get("submit"):
            if not p1 or not p2:
                return "Pilih kedua pemain dulu!"
    return None
                
def restore_match(request,p1,p2,first_serve, final_set_scoring, match_type):
    # Cek sesi sebelumnya
    match = request.session.get('match')
    
    # Buat objek pertandingan
    m = Match(p1, p2, first_serve, final_set_scoring, match_type)
    
    if match and p1 == match.get("p1_name") and p2 == match.get("p2_name"):
        p1_data = match.get("p1") or {}
        p2_data = match.get("p2") or {}
        
        for attr in player_attrs:
            setattr(m.p1, attr, p1_data.get(attr, 0))
            setattr(m.p2, attr, p2_data.get(attr, 0))
            
        for group, attrs in match_attrs.items():
            for attr in attrs:
                setattr(m, attr, match.get(attr ))
            
        m.is_tiebreak = match.get("is_tiebreak", False)
        m.current_server = m.p1 if match.get("current_server") == "p1" else m.p2
        m.p1.sets = p1_data.get("sets", [0,0,0])
        m.p2.sets = p2_data.get("sets", [0,0,0])
        m.p1.tiebreak_display_score = p1_data.get("tiebreak_display_score", [0,0,0])
        m.p2.tiebreak_display_score = p2_data.get("tiebreak_display_score", [0,0,0])
        m.start_time = datetime.fromisoformat(match.get("start_time"))
        m.duration = match.get("duration", 0)
        m.p1.total_statictics_all_set = p1_data.get("total_statictics_all_set", [])
        m.p2.total_statictics_all_set = p2_data.get("total_statictics_all_set", [])
        m.final_set_scoring = match.get("final_set_scoring")
        m.first_server = match.get("first_server")
        m.match_type = match.get("match_type")
        
    return m

def post_winner(request, m):
    point_event = request.POST.get("point")
    serve_type = request.POST.get("serve_type")
    
    if point_event:
        m.play_point(point_event, serve_type)
    return point_event,serve_type

def save_session(request, match: Match):
    data = MatchSerializer(match).to_dict()
    
    data.update({
        "p1_name": match.p1.name,
        "p2_name": match.p2.name
    })
    
    request.session['match'] = data
    
def show_live_tb(match):
    return (
        match["is_tiebreak"] and
        not match["finish"] and
        not (match["final_set_scoring"] == "super_tiebreak_only" and match["current_set"] >= 3)
    )

def show_final_tb(match):
    return (
        match["final_set_scoring"] == "super_tiebreak_only" and
        match["finish"] and match["current_set"] == 2
    )
    

def format_name(names):
    if not names:
        return ""
    
    players =[]
    for name in names:
        part = name.split()
        inisial = part[0][0].upper()
        last_name = " ".join(part[1:]).title()
        players.append(f"{inisial}. {last_name}")
        
    return players
                
  
def get_flash(match, player, set_index):
    flash_set = None
    if match['is_changing_game']:
        if match['is_set_finished']:
            flash_set = match['last_finished_set']
        else:
            flash_set = match['current_set']
            
    return (
        match['last_winner_point'] == player and match['is_changing_game'] and
        not match['is_tiebreak']and
        flash_set == set_index
            )
  
    

    

    
   