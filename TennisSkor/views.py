from django.shortcuts import render
from django.views.generic import View
from . import score



def Skor(request):
    
    # Ambil data user
    p1 = request.GET.get("p1")
    p2 = request.GET.get("p2")
    
    # Cek session sebelumnya
    match = request.session.get('match')
    
    #Buat Objek
    m = score.Match(p1,p2)
    if match and p1 == match.get("p1_name") and p2 == match.get("p2_name"):
        m.p1.pt = match["pt1"]
        m.p2.pt = match["pt2"]
        m.p1.set  = match["g1"]
        m.p2.set  = match["g2"]
        m.p1.tb = match["tb1"]
        m.p2.tb = match["tb2"]
        m.current_set = match["current_set"]
        m.tiebreak = match.get("tiebreak", False)
 
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
        "current_set": m.current_set,
        "tiebreak": m.tiebreak,
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
        "current_set": m.current_set,
        "tiebreak": m.tiebreak,
    }
    
    
    return render(request,'index.html', context)
            
    
    

    