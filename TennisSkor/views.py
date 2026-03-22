from django.shortcuts import render
from django.views.generic import View
from . import score, list_wta_players

def Skor(request):
    
    # Ambil data user
    p1 = request.GET.get("p1") 
    p2 = request.GET.get("p2") 
    
    if request.GET.get("reset"):
        request.session.pop("match", None)
    
    if not p1 or not p2:
        return render(request, 'index.html', {
        "players": list_wta_players.players,
        "error": "Pilih kedua pemain dulu!"
    })
        
    # Profile
    p1_profile= next((p for p in list_wta_players.players if p["name"] == p1), None)
    p2_profile= next((p for p in list_wta_players.players if p["name"] == p2), None)
    
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
        m.p1.firstservetotal= match["firstservetotal1"]
        m.p2.firstservetotal= match["firstservetotal2"]
        m.p1.secondservetotal = match['secondservetotal1']
        m.p2.secondservetotal = match['secondservetotal2']
        m.p1.totalservice= match["totalservice1"]
        m.p2.totalservice= match["totalservice2"]
        m.p1.firstservewin= match['firstservewin1']
        m.p2.firstservewin= match['firstservewin2']
        m.p1.secondservewin= match['secondservewin1']
        m.p2.secondservewin= match['secondservewin2']
        m.p1.breakpoint= match['breakpoint1']
        m.p2.breakpoint= match['breakpoint2']
        m.p1.breakpointwon=match['breakpointwon1']
        m.p2.breakpointwon=match['breakpointwon2']
        m.p1.returnpoint= match['returnpoint1']
        m.p2.returnpoint= match['returnpoint2']
        m.p1.returnpointwon= match['returnpointwon1']
        m.p2.returnpointwon= match['returnpointwon2']
        m.p1.totalpoint = match["tp1"]
        m.p2.totalpoint = match["tp2"]
        m.p1.fe = match['fe1']
        m.p2.fe = match['fe2']
        m.current_set = match["current_set"]
        m.p1.set_won = match["set1_won"]
        m.p2.set_won = match["set2_won"]
        m.lastpoints= match['lastpoints']
        m.tiebreak = match.get("tiebreak", False)
        m.finish= match['finish']
        m.winner = match.get('winner')
        m.loser = match.get('loser')
        m.current_server = m.p1 if match['current_server'] == "p1" else m.p2
        m.status=match["status"]
        m.set_winner= match['set_winner']
            
    
    # Cek Pemenang Poin
    pointWinner = request.POST.get("point")
    serve_type= request.POST.get("serve_type")
    
    if pointWinner in("p1_ace" , "p1_winner" , "p2_df" , "p2_ue", "p1_fe"):
        m.win_point("p1","p2", pointWinner, serve_type)
    elif pointWinner in("p1_df" , "p2_ace" , "p1_ue" , "p2_winner","p2_fe"):
        m.win_point("p2","p1", pointWinner, serve_type)
    
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
        "firstservetotal1" : scores['p1']["firstservetotal"],
        "firstservetotal2" : scores['p2']["firstservetotal"],
        "secondservetotal1" : scores['p1']["secondservetotal"],
        "secondservetotal2" : scores['p2']["secondservetotal"],
        "totalservice1": scores['p1']['totalservice'],
        "totalservice2": scores['p2']['totalservice'],
        "firstservewin1": scores['p1']['firstservewin'],
        "firstservewin2": scores['p2']['firstservewin'],
        "secondservewin1": scores['p1']['secondservewin'],
        "secondservewin2": scores['p2']['secondservewin'],
        "breakpoint1": scores['p1']['breakpoint'],
        "breakpoint2": scores['p2']['breakpoint'],
        "breakpointwon1": scores['p1']['breakpointwon'],
        "breakpointwon2": scores['p2']['breakpointwon'],
        "returnpoint1" : scores['p1']['returnpoint'],
        "returnpoint2" : scores['p2']['returnpoint'],
        "returnpointwon1" : scores['p1']['returnpointwon'],
        "returnpointwon2" : scores['p2']['returnpointwon'],
        "fe1": scores['p1']['fe'],
        "fe2": scores['p2']['fe'],
        "lastpoints": scores['lastpoints'],
        "current_set": m.current_set,
        "set1_won": scores["p1"]["set_won"],
        "set2_won": scores["p2"]["set_won"],
        "tiebreak": m.tiebreak,
        "winner": scores['result']['winner'].name if scores['result']['winner'] else None,
        "loser": scores['result']['loser'].name if scores['result']['loser'] else None,
        "finish": scores['finish'],
        "score": scores['score'],
        "current_server":scores['current_server'],
        "status": scores['status'],
        "set_winner": scores['set_winner']
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
        "fe1": scores['p1']['fe'],
        "fe2": scores['p2']['fe'],
        "lastpoints": scores['lastpoints'],
        "firstservetotal1" : scores['p1']["firstservetotal"],
        "firstservetotal2" : scores['p2']["firstservetotal"],
        "secondservetotal1" : scores['p1']["secondservetotal"],
        "secondservetotal2" : scores['p2']["secondservetotal"],
        "totalservice1": scores['p1']['totalservice'],
        "totalservice2": scores['p2']['totalservice'],
        "firstservewin1": scores['p1']['firstservewin'],
        "firstservewin2": scores['p2']['firstservewin'],
        "secondservewin1": scores['p1']['secondservewin'],
        "secondservewin2": scores['p2']['secondservewin'],
        "firstservewin_pct1": scores['p1']['firstservewin_pct'],
        "firstservewin_pct2": scores['p2']['firstservewin_pct'],
        "secondservewin_pct1": scores['p1']['secondservewin_pct'],
        "secondservewin_pct2": scores['p2']['secondservewin_pct'],
        "breakpoint1": scores['p1']['breakpoint'],
        "breakpoint2": scores['p2']['breakpoint'],
        "breakpointwon1": scores['p1']['breakpointwon'],
        "breakpointwon2": scores['p2']['breakpointwon'],
        "returnpoint1" : scores['p1']['returnpoint'],
        "returnpoint2" : scores['p2']['returnpoint'],
        "returnpointwon1" : scores['p1']['returnpointwon'],
        "returnpointwon2" : scores['p2']['returnpointwon'],
        "return_pct1" : scores['p1']['return_pct'],
        "return_pct2" : scores['p2']['return_pct'],
        "bpwin1" : scores['p1']['bpwin'],
        "bpwin2" : scores['p2']['bpwin'],
        "ace_pct1": scores['p1']['total_ace'],
        "ace_pct2": scores['p2']['total_ace'],
        "df_pct1" : scores['p1']['total_df'],
        "df_pct2" : scores['p2']['total_df'],
        "fe_pct1": scores['p1']['total_fe'],
        "fe_pct2": scores['p2']['total_fe'],
        "winner_pct1": scores['p1']['total_winner'],
        "winner_pct2": scores['p2']['total_winner'],
        "ue_pct1": scores['p1']['total_ue'],
        "ue_pct2": scores['p2']['total_ue'],
        "totalpoint_pct1": scores['p1']['total_totalpoint'],
        "totalpoint_pct2": scores['p2']['total_totalpoint'], 
        "first_serve_pct1": (
        f"{scores['p1']['firstservetotal'] / scores['p1']['totalservice'] * 100:.0f}%"
        if scores['p1']['totalservice'] else "0%"),
        "first_serve_pct2": (
        f"{scores['p2']['firstservetotal'] / scores['p2']['totalservice'] * 100:.0f}%"
        if scores['p2']['totalservice'] else "0%"),
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
        "status": scores['status'],
        "players":list_wta_players.players,
        "p1_profile" : p1_profile,
        "p2_profile" : p2_profile,
        "set_winner": scores['set_winner']
        }
    print(context['current_server'])
    print(f"Total Service p1 : {context['totalservice1']}")
    print(f"Total 1st Service  p1 : {context['firstservetotal1']}")
    print(f"Total 1st Service win p1 : {context['firstservewin1']}")
    print(f"Total 1st Service win p1 % : {context['firstservewin_pct1']}")
    print(f"return_pct1 = {context['return_pct1']}")
    print(f"Total Service p2 : {context['totalservice2']}")
    print(f"Total 1st Service  p2 : {context['firstservetotal2']}")
    print(f"Total 1st Service win p2 : {context['firstservewin2']}")
    print(f"Total 1st Service win p2 % : {context['firstservewin_pct2']}")
    print(f"Total return point p2 : {context['returnpoint2']}")
    print(f"lastpoints = {context['lastpoints']}")
    print(f"return_pct1 = {context['return_pct1']}")
    print(f"return_pct2 = {context['return_pct2']}")
    print(f"return_pct1 = {context['return_pct1']}")
    print("----")
    print(f"2nd serve total p1 : {context['secondservetotal1']}")
    print(f"2nd serve total win p1 : {context['secondservewin1']}")
    print(f"2nd serve total win_pct p1 : {context['secondservewin_pct1']}")
    print(f"2nd serve total p2 : {context['secondservetotal2']}")
    print(f"2nd serve total win p2 : {context['secondservewin2']}")
    print("----")
    print(f"total ace p1 : {context['ace1']}")
    print(f"total ace p2 : {context['ace1']}")
    print(f"total ace p1 % : {context['ace_pct1']}")
   
     
    
    return render(request,'index.html', context)
            
    
    
