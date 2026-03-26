from django.shortcuts import render
from django.views.generic import View
from . import score, list_wta_players, utils

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
    "set1_p1": new_value["p1"]["sets"][0],
    "set1_p2": new_value["p2"]["sets"][0],
    "set2_p1": new_value["p1"]["sets"][1],
    "set2_p2": new_value["p2"]["sets"][1],
    "set3_p1": new_value["p1"]["sets"][2],
    "set3_p2": new_value["p2"]["sets"][2],
        })
    return render(request, 'index.html', context)
    