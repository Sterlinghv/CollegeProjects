def solve_tsp(G):
    #define
    target_city = 0
    city_count = len(G)
    cities_traveled_to = [0]

    #go through until we have visited every city
    while len(cities_traveled_to) < city_count:
        #large holder... in this case a billion!
        minimum_distance_holder = 1e9
        #go through every city
        for city in range(city_count):
            if G[target_city][city] != 0:
                if G[target_city][city] < minimum_distance_holder:
                    #if we havent visited the city yet...
                    if city not in cities_traveled_to:
                        minimum_distance_holder = G[target_city][city]
                        city_closest_to = city

        #nearest city to visited city
        cities_traveled_to.append(city_closest_to)
        target_city = city_closest_to

    #add starting city to the end of the visited cities list
    cities_traveled_to.append(0)
    return cities_traveled_to