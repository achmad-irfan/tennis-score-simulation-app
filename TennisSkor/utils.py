from .score import Match, Player, MatchSerializer
from .list_wta_players import players
from .score import player_attrs, total_stats, match_attrs, service_stats
from datetime import datetime

def get_players_from_request(request):
    p1= request.GET.get("p1")
    p2= request.GET.get("p2")
    first_server = request.GET.get("first_server", "p1")
    return p1,p2,first_server
    
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
                
def restore_match(request,p1,p2,firstserver):
    # Cek sesi sebelumnya
    match = request.session.get('match')
    
    # Buat objek pertandingan
    m = Match(p1, p2, firstserver or "p1")
    
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
    

    
