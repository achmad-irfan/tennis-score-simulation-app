from .score import Match, Player
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
    
    if match and p1 == match.get("p1") and p2 == match.get("p2"):
        for attr in player_attrs:
            setattr(m.p1,attr, match[f"{attr}1"])
            setattr(m.p2,attr, match[f"{attr}2"])
            
        for group, attrs in match_attrs.items():
            for attr in attrs:
                setattr(m, attr, match[attr])
            
        m.tiebreak = match.get("tiebreak", False)
        m.winner = match.get('winner')
        m.loser = match.get('loser')
        m.current_server = m.p1 if match['current_server'] == "p1" else m.p2
        
    return m

def post_winner(request, m):
    pointWinner = request.POST.get("point")
    serve_type= request.POST.get("serve_type")
    
    if pointWinner in("p1_ace" , "p1_winner" , "p2_df" , "p2_ue", "p1_fe"):
        m.win_point("p1","p2", pointWinner, serve_type)
    elif pointWinner in("p1_df" , "p2_ace" , "p1_ue" , "p2_winner","p2_fe"):
        m.win_point("p2","p1", pointWinner, serve_type)
    
    return pointWinner,serve_type

def save_session(request, p1, p2, scores):
    session_data = {}

    for attr in player_attrs:
        session_data[f"{attr}1"] = scores['p1'][attr]
        session_data[f"{attr}2"] = scores['p2'][attr]
        
    for group, attrs in match_attrs.items():
            for attr in attrs:
                session_data[attr]= scores[attr]

    session_data.update({
        "p1": p1,
        "p2": p2,
        "is_tiebreak": scores['is_tiebreak'],
        "match_winner": scores['match_winner'],
        "match_loser": scores['match_loser'],
        "score": scores['score'],
        "current_server": scores['current_server']
    })

    request.session["match"] = session_data
    

def get_context(scores,p1,p2,p1_profile, p2_profile):
    context={}
    for attr in player_attrs:
        if attr != "set":
            context[f"{attr}1"]= scores['p1'][attr]
            context[f"{attr}2"]= scores['p2'][attr]
            
    for group, attrs in match_attrs.items():
        for attr in attrs:
            context[f"{attr}"]= scores[attr]
        
    for attr in total_stats:
        context[f"total_{attr}1"]= scores['p1'][f"total_{attr}"]
        context[f"total_{attr}2"]= scores['p2'][f"total_{attr}"]
        
    for attr in service_stats:
        context[f"{attr}1"]= scores['p1'][f"{attr}_pct"]
        context[f"{attr}2"]= scores['p2'][f"{attr}_pct"]
        
    
    context.update( {
        "p1": p1,
        "p2": p2,
        "p1_profile": p1_profile,
        "p2_profile": p2_profile,
        "set1_p1": scores["p1"]["set"][0],
        "set1_p2": scores["p2"]["set"][0],
        "set2_p1": scores["p1"]["set"][1],
        "set2_p2": scores["p2"]["set"][1],
        "set3_p1": scores["p1"]["set"][2],
        "set3_p2": scores["p2"]["set"][2],
        "match_winner": scores['match_winner'],
        "match_loser": scores['match_loser'],
        "players":players,
        "current_server" : scores["current_server"],
        "return_pct1": scores["p1"]["return_pct"],
        "return_pct2": scores["p2"]["return_pct"]
        })
    
    return context
