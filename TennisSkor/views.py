from django.shortcuts import render
from django.views.generic import View
from . import score, list_wta_players, utils
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from .calculator import build_player_stats
from . import calculator

def Skor(request):
    # Reset Session
    if request.GET.get("reset"):
        request.session.pop("match", None)
    
    # Ambil data user
    p1,p2,first_server, final_set_scoring, match_type = utils.get_players_from_request(request)
    
    if settings.DEBUG:
        rules = utils.get_debug_data(request)
    else:
        rules = settings.MATCH_RULES
    
    # Membuat profile pemain 
    p1_profile = [utils.profile(list_wta_players.players, player) for player in p1]
    p2_profile = [utils.profile(list_wta_players.players, player) for player in p2]
    
    
    # Restrore session jika ada session sebelumnya
    restore_match = utils.restore_match(request, p1,p2,first_server, final_set_scoring, match_type, rules)            
    
    
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
    live_stats = utils.get_live_stats(restore_match)
    
    # Cek apakah ada cancel point
    if "cancel_point" in request.POST:
        restore_match = restore_match.cancel_point()  
        new_value = score.MatchSerializer(restore_match).to_dict()
    
    # Menyimpan dalam session
    utils.save_session(request,restore_match)
    
    active_tab = request.GET.get("active_tab", "pick")
    if request.POST.get("submit_shot") or "cancel_point" in request.POST:
        active_tab = "score"
        
    # Context
    context= new_value.copy()
    context.update({
    "DEBUG" : settings.DEBUG,
    "p1_name" : new_value["p1"]['name'],
    "p2_name":  new_value["p2"]['name'], 
    "p1_name_format" : utils.format_name(new_value["p1"]['name']),
    "p2_name_format":  utils.format_name(new_value["p2"]['name']),
    "players": list_wta_players.players,
    "p1_profile": p1_profile,
    "p2_profile": p2_profile,   
    "start_time": new_value["start_time"] , 
    "duration_set1": f"{new_value['duration'][0]}'",
    "duration_set2": f"{new_value['duration'][1]}'",
    "duration_set3": f"{new_value['duration'][2]}'",
    "total_duration": f"{sum(new_value['duration'])}'",
    "table_match_stats": score.table_match_stats,
    "show_live_tb": utils.show_live_tb(new_value),
    "show_final_tb": utils.show_final_tb(new_value),
    "active_tab" : active_tab,
    "first_server" : new_value['first_server'],
    "match_type" : new_value['match_type'],
    "game_range": range(1, 7),
    "live_stats": live_stats
    })
    
    for attr in score.player_attr_list:
        for i in range(3):
            y= i+1 
            context[f"{attr}{y}_p1"] = new_value["p1"][attr][i]
            context[f"{attr}{y}_p2"] = new_value["p2"][attr][i]
            
    flash= {}   
    for player in ["p1", "p2"]:
        flash[player] = {}
        for i in range(3):
           flash[player][i] = utils.get_flash(new_value, player, i)
    context.update({
        "flash" : flash
    })  
    print(context['p1']['win_probability'])
    print(context['p2']['win_probability'])
    return render(request, 'index.html', context)
    