# -*- coding: utf-8 -*-
import requests


def get_routes_list():

    routes_list = []
    csv_raw_routes = requests.get('http://www.minsktrans.by/city/minsk/routes.txt').content.decode("utf-8-sig").encode("utf-8").split("\r\n")
    del csv_raw_routes[-1]

    for route in csv_raw_routes:
        route_item = route.split(';')
        route_dict = {}
        route_dict['RouteNum'] = route_item[0]
        route_dict['Authority'] = route_item[1]
        route_dict['City'] = route_item[2]
        route_dict['Transport'] = route_item[3]
        route_dict['Operator'] = route_item[4]
        route_dict['ValidityPeriods'] = route_item[5]
        route_dict['SpecialDates'] = route_item[6]
        route_dict['RouteTag'] = route_item[7]
        route_dict['RouteType'] = route_item[8]
        route_dict['Commercial'] = route_item[9]
        route_dict['RouteName'] = route_item[10]
        route_dict['Weekdays'] = route_item[11]
        route_dict['RouteID'] = route_item[12]
        route_dict['Entry'] = route_item[13]
        route_dict['RouteStops'] = route_item[14]
        route_dict['Pikas2012.11.19'] = route_item[15]
        route_dict['Datestart'] = route_item[16]
        routes_list.append(route_dict)

    return routes_list


def get_stops_list():

    routes_list = []
    csv_raw_routes = requests.get('http://www.minsktrans.by/city/minsk/routes.txt').content.decode("utf-8-sig").encode("utf-8").split("\r\n")
    del csv_raw_routes[-1]
    headlines = csv_raw_routes[0].split(';')

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

    return routes_list

get_stops_list()
test
