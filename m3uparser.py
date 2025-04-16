

def parse_m3u_from_file(fn):
    with open(fn) as f:
        lines = f.read().split('\n')
    return parse_m3u(lines)


def parse_m3u(lines):
    lst = []
    i = 0
    player_started = False
    while i < len(lines)-1:
        line: str = lines[i]
        if not player_started:
            if line == '#EXTM3U':
                player_started = True
        elif line.startswith('#EXTINF:-1,'):
            title = line[11:].strip()
            if len(title) > 0:
                url = lines[i+1].strip()
                if len(url) > 0 and not url.startswith('#'):
                    lst.append((title, url))
                    i += 1
        i += 1
    return lst

