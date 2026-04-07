def get_value(source, key):
    if isinstance(source, dict):
        return source.get(key, 0)
    return getattr(source, key, 0)


def calc_pct(win, total):
    return round((win / total) * 100) if total else 0




def build_player_stats(player, opponent):
    from .score import player_attrs, total_stats

    data = {}

    # ambil raw stats (bisa dari object / dict)
    for attr in player_attrs:
        data[attr] = get_value(player, attr)

    # optional fields (kalau ada)
    data["sets"] = get_value(player, "sets")
    data["tiebreak_display_score"] = get_value(player, "tiebreak_display_score")
    data["name"] = get_value(player, "name")

    # service pct
    data.update({
        "first_serve_total_pct": calc_pct(
            get_value(player, "first_serve_total"),
            get_value(player, "total_service")
        ),
        "second_serve_win_pct": calc_pct(
            get_value(player, "second_serve_win"),
            get_value(player, "second_serve_total")
        ),
        "first_serve_win_pct": calc_pct(
            get_value(player, "first_serve_win"),
            get_value(player, "first_serve_total")
        ),
        "return_point_win_pct": calc_pct(
            get_value(player, "return_point_win"),
            get_value(player, "return_point")
        ),
        "break_point_win_pct": calc_pct(
            get_value(player, "break_point_win"),
            get_value(player, "break_point")
        ),
    })

    # 🔥 total pct antar pemain
    for stat in total_stats:
        total = get_value(player, stat) + get_value(opponent, stat)

        data[f"{stat}_pct"] = calc_pct(
            get_value(player, stat),
            total
        )
        
    return data
