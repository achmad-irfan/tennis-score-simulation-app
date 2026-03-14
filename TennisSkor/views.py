from django.shortcuts import render
from django.views.generic import View
from . import score

def Skor(request):
    
    # Ambil data user
    p1 = request.GET.get("p1") or request.session.get("p1_name")
    p2 = request.GET.get("p2") or request.session.get("p2_name")
   
    
    # Pick first server
    firstserver = request.GET.get("firstserve")
    
    
    # Cek session sebelumnya
    match = request.session.get('match')
    
    #Buat Objek
    m = score.Match(p1, p2, firstserver or "p1")
    
    
    
    if match and p1 == match.get("p1_name") and p2 == match.get("p2_name"):
        m.p1.pt = match["pt1"]
        m.p2.pt = match["pt2"]
        m.p1.set  = match["g1"]
        m.p2.set  = match["g2"]
        m.p1.tb = match["tb1"]
        m.p2.tb = match["tb2"]
        m.p1.ace= match['ace1']
        m.p2.ace= match['ace2']
        m.p1.df= match['df1']
        m.p2.df= match['df2']
        m.p1.winner= match['winner1']
        m.p2.winner= match['winner2']
        m.p1.ue= match['ue1']
        m.p2.ue= match['ue2']
        m.p1.totalpoint = match["tp1"]
        m.p2.totalpoint = match["tp2"]
        m.current_set = match["current_set"]
        m.p1.set_won = match["set1_won"]
        m.p2.set_won = match["set2_won"]
        m.tiebreak = match.get("tiebreak", False)
        m.finish= match['finish']
        m.winner = match.get('winner')
        m.loser = match.get('loser')
        m.current_server = m.p1 if match['current_server'] == "p1" else m.p2
            
    
    # Cek Pemenang Poin
    pointWinner = request.POST.get("point")
    
    if pointWinner in("p1_ace" , "p1_winner" , "p2_df" , "p2_ue"):
        m.win_point("p1","p2",pointWinner)
    elif pointWinner in("p1_df" , "p2_ace" , "p1_ue" , "p2_winner"):
        m.win_point("p2","p1",pointWinner)
    
    scores = m.get_score() 
    
    request.session["match"] = {
        "p1_name": p1,
        "p2_name": p2,
        "pt1": scores["p1"]['pt'],
        "pt2": scores["p2"]['pt'],
        "g1": scores["p1"]['set'],
        "g2": scores["p2"]['set'],
        "tb1": scores["p1"]['tb'],
        "tb2": scores["p2"]['tb'],
        "tp1": scores["p1"]['tp'],
        "tp2": scores["p2"]['tp'],
        "ace1": scores["p1"]['ace'],
        "ace2": scores["p2"]['ace'],
        "df1": scores["p1"]['df'],
        "df2": scores["p2"]['df'],
        "winner1" : scores['p1']['winner'],
        "winner2" : scores['p2']['winner'],
        "ue1" : scores['p1']['ue'],
        "ue2" : scores['p2']['ue'],
        "current_set": m.current_set,
        "set1_won": scores["p1"]["set_won"],
        "set2_won": scores["p2"]["set_won"],
        "tiebreak": m.tiebreak,
        "winner": scores['result']['winner'].name if scores['result']['winner'] else None,
        "loser": scores['result']['loser'].name if scores['result']['loser'] else None,
        "finish": scores['finish'],
        "score": scores['score'],
        "current_server":scores['current_server']
    }
    
    labels= ["Ace", "DF", "Winner", "Unforced Error"]
    context = {
        "p1": p1,
        "p2": p2,
        "pt1": scores["p1"]['pt'],
        "pt2": scores["p2"]['pt'],
        "set1_p1": scores["p1"]["set"][0],
        "set1_p2": scores["p2"]["set"][0],
        "set2_p1": scores["p1"]["set"][1],
        "set2_p2": scores["p2"]["set"][1],
        "set3_p1": scores["p1"]["set"][2],
        "set3_p2": scores["p2"]["set"][2],
        "ace1": scores["p1"]['ace'],
        "ace2": scores["p2"]['ace'],
        "tb1": scores["p1"]["tb"],
        "tb2": scores["p2"]["tb"],
        "tp1": scores["p1"]["tp"],
        "tp2": scores["p2"]["tp"],
        "df1": scores["p1"]['df'],
        "df2": scores["p2"]['df'],
        "ue1" : scores['p1']['ue'],
        "ue2" : scores['p2']['ue'],
        "winner1" : scores['p1']['winner'],
        "winner2" : scores['p2']['winner'],
        "current_set": m.current_set,
        "set1_won": scores["p1"]["set_won"],
        "set2_won": scores["p2"]["set_won"],
        "tiebreak": m.tiebreak,
        "finish": scores['finish'],
        "winner": scores['result']['winner'].name if scores['result']['winner'] else None,
        "loser": scores['result']['loser'].name if scores['result']['loser'] else None,
        "score": scores['score'],
        "current_server":scores['current_server'],
        "labels":labels
    }
    
    
    
    
    return render(request,'index.html', context)
            
    
    
    