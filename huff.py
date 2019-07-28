def huff(A, B):
    def d(x_1,x_2,y_1,y_2):
        return math.hypot(x_1-x_2, y_1-y_2)
    
    for a in A:
        a['volume'] = 0

    while B:
        b = B.pop()
        D = [d(a['lat'], b['lat'], a['lng'], b['lng']) for a in A]
        A[D.index(min(D))]['volume'] += b['volume']
    
    points = [(a['lat'], a['lng'], a['volume']) for a in A]
    
    lat_min = min(points, key=lambda x: x[0])[0]
    lng_min = min(points, key=lambda x: x[1])[1]
    lat_d = max(points, key=lambda x: x[0])[0] - lat_min
    lng_d = max(points, key=lambda x: x[1])[1] - lng_min

    points = [((p[0]-lat_min)/lat_d,(p[1]-lng_min)/lng_d, p[2])  for p in points]
    
    data = []
    for _ in points:
        data.append({})
    

    for (i, (x_t, y_t, s_t)) in enumerate(points):
        for y in np.arange(-0.2, 1.2, 0.05):
            for x in np.arange(-0.2, 1.2, 0.05):
                data[i][x, y] = (s_t/d(x_t, x, y_t, y))/sum(s1/d(x, x1, y, y1) for (y1,x1,s1) in points)
    ret = []
    for e in data:
        ret.append(sum(e.values()))
    return ret