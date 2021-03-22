import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import date, datetime, timedelta


class LsfService:

    def __init__(self, params):
        #self.url = 'https://lsf.ovgu.de/qislsf/rds?state=extendedRoomSearch&type=1&next=extendedRoomSearch.vm&nextdir=ressourcenManager&searchCategory=detailedRoomSearch&asi='
        #self._room_search_url = 'https://lsf.ovgu.de/qislsf/rds?state=extendedRoomSearch&type=1&next=extendedRoomSearch.vm&nextdir=ressourcenManager&searchCategory=detailedRoomSearch&asi='
        #self.payload = 'searchCategory=detailedRoomSearch&P_anzahl=10&P_start=0&WochentagID=6&Beginn=10%3A00&Ende=11%3A00&RhythmusID=2&AnfangDat=20.03.2020&EndeDat=20.03.2020&kindOfRoom=5%7C39%7C10&building=14&campus=2&RoomSearch_Search=Suchen'
        #self.header = {'Content-Type':'application/x-www-form-urlencoded'}
        self.params = params
        self.form_data = {
            'searchCategory': 'detailedRoomSearch',
            'P_anzahl': 5,
            'P_start': 0,
            'WochentagID': 6,
            'Beginn': '10:00',
            'Ende': '11:00',
            'RhythmusID': 2,
            'AnfangDat': '20.03.2020',
            'EndeDat': '20.03.2020',
            'equipment': '8:99|22:10',
            'kindOfRoom': '5|39|81|10|57',
            'building': '',
            'campus': 2,
            'RoomSearch_Search': 'Search'
        }

    def search_room(self, building=None, start_time=datetime.now(),
                    duration=2, equipments={}, date_needed=date.today()):
        query_data = self.form_data.copy()
        
        if building in self.params['buildings_num']:
            building = self.params['buildings_num'][building]
            query_data['building'] = building
        elif building is None:
            query_data['building'] = ''
        else:
            return None

        eq_str = ''
        for key, value in equipments.items():
            if key in self.params['equipments']:
                eq_str += str(self.params['equipments']
                              [key]) + ':' + str(value) + '|'
        query_data['equipment'] = eq_str
        query_data['WochentagID'] = (date_needed.isoweekday() % 7)+1

        date_needed = date_needed.strftime("%d.%m.%Y")
        query_data['AnfangDat'] = date_needed
        query_data['EndeDat'] = date_needed
        end_time = start_time + timedelta(hours=duration)
        start_time = start_time.strftime('%H:%M')
        end_time = end_time.strftime('%H:%M')
        query_data['Beginn'] = start_time
        query_data['Ende'] = end_time
        return self._room_search_query(query_data)

    def _extract_roomid(self, roomid):
        pattern = '(?<=_)[a-zA-Z0-9]+'
        result = re.findall(pattern, roomid)[0]
        return result

    def _extract_roomno(self, roomno):
        result = roomno.split()[1]
        return result

    def _room_search_query(self, data):
        try:
            page = requests.post(url=self.params['urls']['rooms_search'], data=data, headers=self.params['urls']['rooms_search_header'])
            soup = BeautifulSoup(page.content, 'html.parser')
            #print("soup: "+soup)
            table = soup.find('table')
            table_rows = table.find_all('tr')
            res = []
            for tr in table_rows:
                td = tr.find_all('td')
                #row = [tr.text.strip() for tr in td if tr.text.strip()]
                row = []
                for tr in td:
                    if tr.text.strip():
                        lb = tr.find('label', attrs={'for': True})
                        if lb:
                            roomid = str(lb.attrs.get('for'))
                            roomno = str(tr.text.strip())
                            row.append(self._extract_roomno(roomno))
                            row.append(self._extract_roomid(roomid))
                        else:
                            row.append(tr.text.strip())
                if row:
                    res.append(row)
            rooms = pd.DataFrame(res, columns=["Room", "Room ID", "Roomtype", "Institute"])
            return rooms
        except:
            return None

    def get_room_details(self, roomid):
        url = self.params['urls']['room_details']
        url += str(roomid)
        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        table = soup.find('table',{'summary':"Übersicht über die Ausstattung des Raumes"})
        table_rows = table.find_all('tr')
        room_details = {}
        res=[]
        #print(self.params['translations']['equipments'])
        for tr in table_rows:
            td = tr.find_all('td')
            if td: 
                row = []
                for cl in td:
                    if cl:
                        if cl.text.strip() in self.params['translations']['equipments']:
                            row.append(self.params['translations']['equipments'][cl.text.strip()])                        
                        else:
                            row.append(cl.text.strip())
                if row:
                    res.append(row)

        equipments = pd.DataFrame(res, columns=["Equipment","Quantity","Remarks"])
        return equipments

    def setPrinter(self, name):
        return name

    def getPrinter(self, name):
        val = self.setPrinter(name)
        print(val)