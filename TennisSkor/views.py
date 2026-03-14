from django.shortcuts import render
from django.views.generic import View
from . import score

def Skor(request):
    
    # Ambil data user
    p1 = request.GET.get("p1") or request.session.get("p1_name")
    p2 = request.GET.get("p2") or request.session.get("p2_name")
    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    
    
    # Pick first server
    firstserver = request.GET.get("firstserve")
    print(f"firstserver : {firstserver}")
    print(f"Apakah firstserver None?  {firstserver==None}")
    
    
    
    # Cek session sebelumnya
    match = request.session.get('match')
    
    #Buat Objek
    m = score.Match(p1, p2, firstserver or "p1")
    
    print(f"servise pertama = {m.current_server}")
    
    if match and p1 == match.get("p1_name") and p2 == match.get("p2_name"):
        m.p1.pt = match["pt1"]
        m.p2.pt = match["pt2"]
        m.p1.set  = match["g1"]
        m.p2.set  = match["g2"]
        m.p1.tb = match["tb1"]
        m.p2.tb = match["tb2"]
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
    pointWinner = request.POST.get("player")
    if pointWinner == "p1":
        m.win_point("p1","p2")
    elif pointWinner == "p2":
        m.win_point("p2","p1")
    
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
        "tb1": scores["p1"]["tb"],
        "tb2": scores["p2"]["tb"],
        "tp1": scores["p1"]["tp"],
        "tp2": scores["p2"]["tp"],
        "current_set": m.current_set,
        "set1_won": scores["p1"]["set_won"],
        "set2_won": scores["p2"]["set_won"],
        "tiebreak": m.tiebreak,
        "finish": scores['finish'],
        "winner": scores['result']['winner'].name if scores['result']['winner'] else None,
        "loser": scores['result']['loser'].name if scores['result']['loser'] else None,
        "score": scores['score'],
        "current_server":scores['current_server']
    }
    
    
    print(context)
    
    return render(request,'index.html', context)
            
    
    

    