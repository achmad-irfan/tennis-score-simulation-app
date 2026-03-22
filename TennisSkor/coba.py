players = ["p1", "p2"]
stats = ["ace", "df", "winner", "ue", "fe", "totalpoint"]
new_stats=[]
for stat in stats:
    new_stats.append("total_"+stat)
    
print(new_stats)