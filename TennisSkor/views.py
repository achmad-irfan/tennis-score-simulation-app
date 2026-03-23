from django.shortcuts import render
from django.views.generic import View
from . import score, list_wta_players, utils

def Skor(request):
    # Reset Session
    if request.GET.get("reset"):
        request.session.pop("match", None)
    
    # Ambil data user
    p1,p2,firstserver = utils.get_players_from_request(request)
    
    # Validasi input
    if not p1 or not p2:
        return render(request, 'index.html', {
        "players": list_wta_players.players,
        "error": "Pilih kedua pemain dulu!"
    })
    
    # Membuat profile pemain 
    p1_profile= utils.profile(list_wta_players.players, p1)
    p2_profile= utils.profile(list_wta_players.players, p2)
    
    # Restrore session jika ada session sebelumnya
    m = utils.restore(request, p1,p2,firstserver)
    
    
    # Cek Pemenang Poin dan panggil method winning_point
    pointWinner,serve_type= utils.post_winner(request,m)
    
    # Memasukan nilai atribut baru 
    scores = m.get_score() 
    
    # Menyimpan dalam session
    utils.save_session(request,p1,p2,scores)
    
    # Context
    context= utils.get_context(scores,p1,p2,p1_profile, p2_profile)
    print(context['current_tie_break'])
    return render(request, 'index.html', context)
