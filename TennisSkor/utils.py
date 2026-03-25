from .score import Match, Player, MatchSerializer
from .list_wta_players import players
from .score import player_attrs, total_stats, match_attrs, service_stats

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
                
def restore(request,p1,p2,firstserver):
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
        
        
    return m

def post_winner(request, m):
    pointWinner = request.POST.get("point")
    serve_type= request.POST.get("serve_type")
    
    if pointWinner in("p1_ace" , "p1_winner" , "p2_df" , "p2_ue", "p1_fe"):
        m.win_point("p1","p2", pointWinner, serve_type)
    elif pointWinner in("p1_df" , "p2_ace" , "p1_ue" , "p2_winner","p2_fe"):
        m.win_point("p2","p1", pointWinner, serve_type)
    
    return pointWinner,serve_type

def save_session(request, match: Match):
    data = MatchSerializer(match).to_dict()
    
    data.update({
        "p1_name": match.p1.name,
        "p2_name": match.p2.name
    })
    
    request.session['match'] = data
    