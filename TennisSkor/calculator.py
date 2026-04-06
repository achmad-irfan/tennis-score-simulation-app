def calc_pct(win, total):
    return round((win / total) * 100) if total else 0

def build_service_pct(player):
    return {
        "first_serve_total_pct": calc_pct(player.first_serve_total, player.total_service),
        "second_serve_win_pct": calc_pct(player.second_serve_win, player.second_serve_total),
        "first_serve_win_pct": calc_pct(player.first_serve_win, player.first_serve_total),
        "return_point_win_pct": calc_pct(player.return_point_win, player.return_point),
        "break_point_win_pct": calc_pct(player.break_point_win, player.break_point),
    }
    
    
def build_player_stats(player):
    from .score import player_attrs 
    data = {}

    # ambil raw stats
    for attr in player_attrs:
        data[attr] = getattr(player, attr)

    data["sets"] = player.sets
    data["tiebreak_display_score"] = player.tiebreak_display_score
    data['name']=  player.name

    # service pct
    data.update(build_service_pct(player))

    return data

def build_total_pct( p1, p2):
    from .score import total_stats
    totals = {}

    for stat in total_stats:
        total = getattr(p1, stat) + getattr(p2, stat)

        totals[f"total_{stat}_pct1"] = calc_pct(getattr(p1, stat), total)
        totals[f"total_{stat}_pct2"] = calc_pct(getattr(p2, stat), total)

    return totals