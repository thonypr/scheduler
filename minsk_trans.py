# -*- coding: utf-8 -*-
import requests
import html5lib
import bs4
import urllib2

bus_page_name = u"autobus"
trolley_page_name = u"trolleybus"
tram_page_name = u"tram"


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


# def get_stops_list():
#
#     routes_list = []
#     csv_raw_routes = requests.get('http://www.minsktrans.by/city/minsk/routes.txt').content.decode("utf-8-sig").encode("utf-8").split("\r\n")
#     print csv_raw_routes[-1]
#     del csv_raw_routes[-1]
#     headlines = csv_raw_routes[0].split(';')
#     del csv_raw_routes[0]
#
#     for route in csv_raw_routes:
#         route_item = route.split(';')
#         route_dict = {}
#         route_dict['{}'.format(headlines[0])] = route_item[0]
#         route_dict['{}'.format(headlines[1])] = route_item[1]
#         route_dict['{}'.format(headlines[2])] = route_item[2]
#         route_dict['{}'.format(headlines[3])] = route_item[3]
#         route_dict['{}'.format(headlines[4])] = route_item[4]
#         route_dict['{}'.format(headlines[5])] = route_item[5]
#         route_dict['{}'.format(headlines[6])] = route_item[6]
#         route_dict['{}'.format(headlines[7])] = route_item[7]
#         route_dict['{}'.format(headlines[8])] = route_item[8]
#         route_dict['{}'.format(headlines[9])] = route_item[9]
#         route_dict['{}'.format(headlines[10])] = route_item[10]
#         route_dict['{}'.format(headlines[11])] = route_item[11]
#         route_dict['{}'.format(headlines[12])] = route_item[12]
#         route_dict['{}'.format(headlines[13])] = route_item[13]
#         route_dict['{}'.format(headlines[14])] = route_item[14]
#         route_dict['{}'.format(headlines[15])] = route_item[15]
#         route_dict['{}'.format(headlines[16])] = route_item[16]
#
#         routes_list.append(route_dict)
#
#     filtered_routes = []
#     print routes_list[0]['RouteNum']
#
#     i = 0
#     print routes_list.__len__()
#
#     while i < routes_list.__len__():
#         print "entered"
#         print u'i = {}'.format(i)
#         # если указан RouteNum ок, берём элемент
#         if routes_list[i]['RouteNum']:
#             # print "found init"
#             filtered_routes.append(routes_list[i])
#             i += 1
#             # проверить, есть ли реверс
#             if not routes_list[i]['RouteNum'] and routes_list[i]['RouteName'].split(" - ").sort() == routes_list[i-1]['RouteName'].split(" - ").sort():
#                 # print "found reverse"
#                 routes_list[i]['RouteNum'] = routes_list[i-1]['RouteNum']
#                 filtered_routes.append(routes_list[i])
#                 i += 1
#         else:
#             i += 1
#         # if i > routes_list.__len__():
#         #     break
#     print u'i = {}'.format(i)
#     return routes_list


def get_routes_html(transport):
    page = requests.get(u"https://kogda.by/routes/minsk/{}".format(transport)).content

    # try:
    #     from BeautifulSoup import BeautifulSoup
    # except ImportError:
    #     from bs4 import BeautifulSoup
    #
    # try:
    #     from urllib2 import urlopen
    # except ImportError:
    #     from urllib.request import urlopen  # py3k
    #
    # url = "https://kogda.by/routes/minsk/autobus"
    # soup = BeautifulSoup(urlopen(url), "html5lib")
    # print(soup.prettify())

    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        from bs4 import BeautifulSoup
    html = page
    parsed_html = BeautifulSoup(page, "html5lib")
    routes = []
    final = []
    text = 0
    i = 0

    while text is not None:
        text = parsed_html.body.find('div', attrs={'id': 'routes-block-{}'.format(i)})
        if text is not None:
            raw_routes = text.text.split("\n\n")
            for raw_route in raw_routes:
                try:
                    value = raw_route.split("\n", 1)[1]
                except BaseException:
                    value = None
                if value is not u'':
                    routes.append(value)
            i += 1
        else:
            print "All routes were found"
    for item in routes:
        if item == u'                                    ':
            del item
        else:
            trim = item.split('                                            ')[1]
            final.append(trim)
    return final


def get_direction_index_by_route(transport, route_number, direction):
    page = requests.get(u"https://kogda.by/routes/minsk/{0}/{1}".format(transport, route_number)).content
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        from bs4 import BeautifulSoup
    parsed_html = BeautifulSoup(page, "html5lib")
    text = 0
    i = 0

    while text is not None:
        text = parsed_html.body.find('div', attrs={'id': 'direction-{}-heading'.format(i)})
        # x = u'{}'.format(text.text)
        # a = x.__contains__(u"{}".format(direction))
        if text is not None:
            if direction in text.text:
                return i
            else:
                i = i+1
        else:
            print "All directions were checked"
    return 666


def get_stops_in_route(transport, route_number, direction):
    page = requests.get(u"https://kogda.by/routes/minsk/{0}/{1}".format(transport, route_number)).content
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        from bs4 import BeautifulSoup
    parsed_html = BeautifulSoup(page, "html5lib")
    result = []

    try:
        direction_index = get_direction_index_by_route(transport, route_number, direction)
        stops = parsed_html.body.find('div', attrs={'id': 'direction-{}'.format(direction_index)}).text
        stops = stops.split("\n\n\n                                            ")[0].split('\n')
        for stop in stops:
            stop = stop.strip()
            if stop is not u'':
                result.append(stop)
        del result[0]
        return result
    except BaseException:
        return u"Error in getting stops for route {}".format(route_number)


def get_directions_in_route(transport, route_number):
    page = requests.get(u"https://kogda.by/routes/minsk/{0}/{1}".format(transport, route_number)).content
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        from bs4 import BeautifulSoup
    parsed_html = BeautifulSoup(page, "html5lib")
    text = 0
    i = 0
    result = []

    while text is not None:
        text = parsed_html.body.find('div', attrs={'id': 'direction-{}-heading'.format(i)})
        if text is not None:
            raw_direction = text.text.split("\n                                ")[1].split("\n")[0]
            result.append(raw_direction)
            i += 1
        else:
            print "All directions were found"
    return result


# def get_stops_by_transport_and_number(transport, route_number):
#     page = requests.get(u"https://kogda.by/routes/minsk/{0}/{1}".format(transport, route_number)).content
#     try:
#         from BeautifulSoup import BeautifulSoup
#     except ImportError:
#         from bs4 import BeautifulSoup
#     html = page
#     parsed_html = BeautifulSoup(html)
#     original_name = parsed_html.body.find('div', attrs={'id': 'direction-0-heading'}).text.split("\n\n\n                                ")[1].split("\n")[0]
#     reversed_name = parsed_html.body.find('div', attrs={'id': 'direction-1-heading'}).text.split("\n\n\n                                ")[1].split("\n")[0]
#     original_stops = get_stops_in_route(0, parsed_html, original_name)
#     reversed_stops = get_stops_in_route(1, parsed_html, reversed_name)
#     routes = []
    # text = 0
    # i = 0
    # while text is not None:
    #     text = parsed_html.body.find('div', attrs={'id': 'routes-block-{}'.format(i)})
    #     if text is not None:
    #         raw_routes = text.text.split("\n\n")
    #         for raw_route in raw_routes:
    #             try:
    #                 value = raw_route.split("\n", 1)[1]
    #             except BaseException:
    #                 value = None
    #             if value is not u'':
    #                 routes.append(value)
    #         i += 1
    #     else:
    #         print "All routes were found"
    # if reversed_name is not u'':
    #     TODO: think about getting route without reverse
        # return original_name, original_stops, reversed_name, reversed_stops
    # else:
    #     return original_name, original_stops


def get_around_times_at_stop(transport, route_number, route, stop):
    result = []
    page = requests.get(u"https://kogda.by/routes/minsk/{0}/{1}/{2}/{3}".format(transport, route_number, route, stop)).content
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        from bs4 import BeautifulSoup
    html = page
    parsed_html = BeautifulSoup(html)
    try:
        times = parsed_html.body.find('div', attrs={'class': 'timetable'}).text.split("\n\n                    ")
        for time in times:
            x = time.split('\n')
            for v in x:
                if v.strip() is not u'':
                    result.append(v.strip())
        # del result[0]
        return result
    except BaseException:
        return u'Error in getting times for {0} # {1} at {2}'.format(transport, route_number, stop)

# dirs = get_directions_in_route("autobus", u"30-с")
# stops = get_stops_in_route("autobus", u"30-с", dirs[0])
# print get_around_times_at_stop("autobus", u"30-с", dirs[0], stops[0])
# ix = 0
# get_stops_by_transport_and_number(u'trolleybus', u'35')
# get_around_times_at_stop(u'autobus', u'30-с', u'Корженевского - Красный Бор', u'пл. Казинца')
#
# x = requests.get(u"https://kogda.by/routes/minsk/autobus/30-с/Корженевского - Красный Бор/пл. Казинца").content

# transport = raw_input(u"Enter transport...\n")
# print transport
# routes = get_routes_html(transport)
# print u"List of routes for {}:".format(transport)
# for x in routes:
#     print x
# selected_route_number = raw_input(u"Enter route number...\n")
# print u"List of stops for {0} number {1}:".format(transport, selected_route_number)
# route_name, original_stops, reversed_name, reversed_stops = get_stops_by_transport_and_number(transport, selected_route_number)
# print u"Available stops for {}:".format(route_name)
# for y in original_stops:
#     print y
#
# print u"Available stops for {}:".format(reversed_name)
# for y in reversed_stops:
#     print y
# # route_name = raw_input(u"Enter route name...\n")
# # stop = raw_input(u"Enter stop name...\n")
# times = get_around_times_at_stop(transport, selected_route_number, route_name, original_stops[0])
# print u"Passed was at: {0}\n Next will be at: {1}\n Future will be at: {2}".format(times[0], times[1], times[2])
# i = 0
# # trolley_routes = get_routes_html(trolley_page_name)
# # tran_routes = get_routes_html(tram_page_name)
# i = 9



