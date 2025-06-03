

def parse_m3u_from_file(fn):
    with open(fn) as f:
        lines = f.read().split('\n')
    return parse_m3u(lines)


def parse_m3u(lines):
    lst = []
    i = 0
    playlist_started = False
    while i < len(lines)-1:
        line: str = lines[i]
        if not playlist_started:
            if line == '#EXTM3U':
                playlist_started = True
        else:
            if line.startswith('#EXTINF:-1,'):
                s = 11
            elif line.startswith('#EXTINF:0,'):
                s = 10
            elif line.startswith('#EXTINF:-1 ,'):
                s = 12
            elif line.startswith('#EXTINF:0 ,'):
                s = 11
            else:
                i += 1
                continue

            title = line[s:].strip()
            if len(title) > 0:
                j = i+1
                while lines[j].startswith("#") and j < len(lines) - 1: j += 1
                url = lines[j].strip()
                if len(url) > 0:
                    lst.append((title, url))
                i = j
        i += 1
    return lst

