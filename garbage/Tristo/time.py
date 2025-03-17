def convert_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    result = []
    if hours > 0:
        result.append(f"{hours}h")
    if minutes > 0:
        result.append(f"{minutes}min")
    if secs > 0 or not result:  
        result.append(f"{secs}s")

    return " ".join(result)

print(convert_seconds(7265))
print(convert_seconds(65))
print(convert_seconds(0))