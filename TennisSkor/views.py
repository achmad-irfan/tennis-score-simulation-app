from django.shortcuts import render
from django.views.generic import View
from . import score, list_wta_players, utils
from datetime import datetime

def Skor(request):
    # Reset Session
    if request.GET.get("reset"):
        request.session.pop("match", None)
    
    # Ambil data user
    p1,p2,first_server = utils.get_players_from_request(request)
    
    # Validasi input
    if request.GET.get("submit"):
        if (not p1 or not p2) or (p1 == p2):
            error = "Pick 2 different players!!"
            return render(request, 'index.html', {
            "p1": p1,
            "p2": p2,
            "players": list_wta_players.players,
            "error": error
        })
    
    # Membuat profile pemain 
    p1_profile= utils.profile(list_wta_players.players, p1)
    p2_profile= utils.profile(list_wta_players.players, p2)
    
    # Restrore session jika ada session sebelumnya
    restore_match = utils.restore_match(request, p1,p2,first_server)            
    
    # Cek Pemenang Poin dan panggil method winning_point
    pointWinner,serve_type= utils.post_winner(request,restore_match)
    
    # Cek apakah ada cancel point
    
    # Validasi input pemenang poin
    if request.POST.get("submit_shot"):
        if not pointWinner or not serve_type:
            error = "Pilih pemenang poin"
            return render(request, 'index.html', {
            "p1": p1,
            "p2": p2,
            "error": error
        })
    
    # Memasukan nilai baru pada atribut
    new_value = score.MatchSerializer(restore_match).to_dict()
    
    # Cek apakah ada cancel point
    if "cancel_point" in request.POST:
        restore_match = restore_match.cancel_point()  
        new_value = score.MatchSerializer(restore_match).to_dict()
    
    # Menyimpan dalam session
    utils.save_session(request,restore_match)
    
    # Context
    context= new_value.copy()
    context.update({
    "p1_name" : new_value["p1"]['name'],
    "p2_name":  new_value["p2"]['name'],
    "players": list_wta_players.players,
    "p1_profile": p1_profile,
    "p2_profile": p2_profile,   
    "start_time": new_value["start_time"] , 
    "duration_set1": f"{new_value['duration'][0]}'",
    "duration_set2": f"{new_value['duration'][1]}'",
    "duration_set3": f"{new_value['duration'][2]}'",
    "total_duration": f"{sum(new_value['duration'])}'"
        })
    
    for attr in score.player_attr_list:
        for i in range(3):
            y= i+1 
            context[f"{attr}{y}_p1"] = new_value["p1"][attr][i]
            context[f"{attr}{y}_p2"] = new_value["p2"][attr][i]
    
    print(context['set_snapshot'])
    
    print(context['p1']['ace'])    
    return render(request, 'index.html', context)
    