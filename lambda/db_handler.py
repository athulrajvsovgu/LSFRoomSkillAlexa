import pymongo
import pandas as pd


class ReserveRooms:

    def __init__(self):
        self.username = 'athulrajvs'
        self.password = 'vUni#2018'
        self.url = 'mongodb+srv://'+self.username+':'+self.password+'@cluster0.pbsks.mongodb.net/mydbs?retryWrites=true&w=majority'
        self.client = pymongo.MongoClient(self.url)
        self.database = self.client.mydbs
        self.collection = self.database.RoomReserve
    
    def check_user(self, user):
        flag = False
        try:
            for dict in self.collection.find():
                if dict['user'] == user:
                    flag = True
                    break
            self.client.close()    
            return flag
        except:
            return 'error'
        
    def return_user_info(self, user):
        return_user = 'empty'
        try:
            for dict in self.collection.find():
                if dict['user'] == user:
                    return_user = dict
                    break
            self.client.close()    
            return return_user
        except:
            return 'error'
        
    def remove_reservation(self, user):
        flag = False
        try:
            for dict in self.collection.find():
                if dict['user'] == user:
                    self.collection.remove(dict)
                    flag = True
                    break
            self.client.close()    
            return flag
        except:
            return 'error'

    def check_data(self, rooms):
        common = []
        temp = pd.DataFrame(columns=["user", "room", "start_at", "expire_at"])
        final_result = pd.DataFrame(columns=["user", "room", "start_at", "expire_at"])
        try:
            for dict in self.collection.find():
                if dict['room'] in rooms['room'].values:
                    common.append(dict['room'])
    
            temp = rooms.loc[~rooms['room'].isin(common)]
            final_result = final_result.append(temp, ignore_index=True)
    
            for dict in self.collection.find():
                for i in range(len(rooms['room'])):
                    if rooms['room'][i] == dict['room']:
                        condition1 = rooms['start_at'][i] >= dict['start_at']
                        condition2 = rooms['start_at'][i] <= dict['expire_at']
                        condition3 = rooms['expire_at'][i] >= dict['start_at']
                        condition4 = rooms['expire_at'][i] <= dict['expire_at']
                        condition5 = condition1 and condition2
                        condition6 = condition3 and condition4
                        condition7 = condition5 or condition6
                        if not condition7:
                            final_result = final_result.append({'user': rooms['user'][i], 'room': rooms['room'][i], 'start_at': rooms['start_at'][i],
                                                'expire_at': rooms['expire_at'][i]}, ignore_index=True)
    
            self.client.close()
            return final_result
        except:
            return 'error'

    def insert_data(self, records):
        try:
            self.collection.create_index("expire_at", expireAfterSeconds=0)
            self.collection.insert_one(records)
            self.client.close()
            return True
        except:
            return False