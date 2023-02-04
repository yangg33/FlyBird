def save_history(point):
    with open("misc/history.txt", "a") as f:
        f.write(f"{point}\n")


def get_max_points():
    with open("misc/history.txt", "r") as f:
        data = f.readlines()
        max_p = 0
        for p in data:
            p = int(p.strip())
            if p > max_p:
                max_p = p
        return max_p
