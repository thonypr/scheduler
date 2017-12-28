# -*- coding: utf-8 -*-
import requests


def get_routes_list():

    routes_list = []
    csv_raw_routes = requests.get('http://www.minsktrans.by/city/minsk/routes.txt').content.decode("utf-8-sig").encode("utf-8").split("\r\n")
    print csv_raw_routes[-1]
    del csv_raw_routes[-1]
    headlines = csv_raw_routes[0].split(';')
    del csv_raw_routes[0]

    for route in csv_raw_routes:
        route_item = route.split(';')
        route_dict = {}
        route_dict['{}'.format(headlines[0])] = route_item[0]
        route_dict['{}'.format(headlines[1])] = route_item[1]
        route_dict['{}'.format(headlines[2])] = route_item[2]
        route_dict['{}'.format(headlines[3])] = route_item[3]
        route_dict['{}'.format(headlines[4])] = route_item[4]
        route_dict['{}'.format(headlines[5])] = route_item[5]
        route_dict['{}'.format(headlines[6])] = route_item[6]
        route_dict['{}'.format(headlines[7])] = route_item[7]
        route_dict['{}'.format(headlines[8])] = route_item[8]
        route_dict['{}'.format(headlines[9])] = route_item[9]
        route_dict['{}'.format(headlines[10])] = route_item[10]
        route_dict['{}'.format(headlines[11])] = route_item[11]
        route_dict['{}'.format(headlines[12])] = route_item[12]
        route_dict['{}'.format(headlines[13])] = route_item[13]
        route_dict['{}'.format(headlines[14])] = route_item[14]
        route_dict['{}'.format(headlines[15])] = route_item[15]
        route_dict['{}'.format(headlines[16])] = route_item[16]

        routes_list.append(route_dict)

    filtered_routes = []
    print routes_list[0]['RouteNum']

    i = 0
    print routes_list.__len__()

    while i < routes_list.__len__():
        print "entered"
        print u'i = {}'.format(i)
        # если указан RouteNum ок, берём элемент
        if routes_list[i]['RouteNum']:
            # print "found init"
            filtered_routes.append(routes_list[i])
            i += 1
            # проверить, есть ли реверс
            if not routes_list[i]['RouteNum'] and routes_list[i]['RouteName'].split(" - ").sort() == routes_list[i-1]['RouteName'].split(" - ").sort():
                # print "found reverse"
                routes_list[i]['RouteNum'] = routes_list[i-1]['RouteNum']
                filtered_routes.append(routes_list[i])
                i += 1
        else:
            i += 1
        # if i > routes_list.__len__():
        #     break
    # print u'i = {}'.format(i)

    # for x in filtered_routes:
    #     print "{}".format(x['RouteNum'])

    return filtered_routes


def get_stops_list():

    stops_list = []
    csv_raw_stops = requests.get('http://www.minsktrans.by/city/minsk/stops.txt').content.decode("utf-8-sig").encode("utf-8").split("\n")
    print csv_raw_stops[-1]
    del csv_raw_stops[-1]
    headlines = csv_raw_stops[0].split(';')
    del csv_raw_stops[0]

    for stop in csv_raw_stops:
        stop_item = stop.split(';')
        stop_dict = {}
        stop_dict['{}'.format(headlines[0])] = stop_item[0]
        stop_dict['{}'.format(headlines[1])] = stop_item[1]
        stop_dict['{}'.format(headlines[2])] = stop_item[2]
        stop_dict['{}'.format(headlines[3])] = stop_item[3]
        stop_dict['{}'.format(headlines[4])] = stop_item[4]
        stop_dict['{}'.format(headlines[5])] = stop_item[5]
        stop_dict['{}'.format(headlines[6])] = stop_item[6]
        stop_dict['{}'.format(headlines[7])] = stop_item[7]
        stop_dict['{}'.format(headlines[8])] = stop_item[8]
        stop_dict['{}'.format(headlines[9])] = stop_item[9]
        # stop_dict['{}'.format(headlines[10])] = stop_item[10]

        stops_list.append(stop_dict)

    filtered_stops = []
#    print stops_list[0]['RouteNum']

    i = 0
    print stops_list.__len__()

    # while i < stops_list.__len__():
    #     print "entered"
    #     print u'i = {}'.format(i)
    #     если указан RouteNum ок, берём элемент
        # if stops_list[i]['RouteNum']:
        #     print "found init"
            # filtered_stops.append(stops_list[i])
            # i += 1
            # проверить, есть ли реверс
            # if not stops_list[i]['RouteNum'] and stops_list[i]['RouteName'].split(" - ").sort() == stops_list[i-1]['RouteName'].split(" - ").sort():
            #     print "found reverse"
                # stops_list[i]['RouteNum'] = stops_list[i-1]['RouteNum']
                # filtered_stops.append(stops_list[i])
                # i += 1
        # else:
        #     i += 1
        # if i > stops_list.__len__():
        #     break
    # print u'i = {}'.format(i)
    #
    # for x in filtered_stops:
    #     print "{}".format(x['RouteNum'])

    # return filtered_stops
    return stops_list

# get_routes_list()
x = get_stops_list()
print x[456]['Name']
