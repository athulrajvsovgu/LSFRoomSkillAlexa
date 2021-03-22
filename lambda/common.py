import logging
import os
import json
import locale
import requests
import calendar
import gettext
import yaml 
import codecs
import pymongo
import urllib
import pandas as pd
from alexa import data
from lsf_service import LsfService
from db_handler import ReserveRooms
from datetime import date, datetime, timedelta, timezone
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from pytz import timezone as tz
from random import randrange
    
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SearchIntent:
    
    def __init__(self):
        self.file = codecs.open('parameters.yml', 'r', 'utf-8')
        try:
            self.params = yaml.safe_load(self.file)
        except yaml.YAMLError as ex:
            print(ex)
            self.params = None
        self.file.close()
        self.ls = LsfService(self.params)
        self.db = ReserveRooms()
        self.time_list = []
        self.equipments_list = [{'free seating': 0, 'lcd projector': 1},
                    {'free seating': 0, 'blackboard': 1},
                    {'seats': 0, 'lcd projector': 1},
                    {'seats': 0, 'blackboard': 1}]

    def date_format_convert(self, data):
        date_converted = data.strftime("%Y-%m-%d %H:%M:%S.%f")
        date_converted = datetime.strptime(date_converted,'%Y-%m-%d %H:%M:%S.%f')
        return date_converted         
    
    def create_time_list(self, time, duration):
        end_time = time + timedelta(hours=duration)
        time_list = []
        time_check = time
        time_list.append(time)
        iterator = 0
        while iterator <= duration:
            if not((str(time_check) == '1900-01-01 07:00:00') or (str(time_check) == '1900-01-01 21:00:00')):
                time_list.append(time_check - timedelta(hours=1))
                time_list.append(time_check + timedelta(hours=1))
                time_list.append(time_check - timedelta(hours=1 + duration))
                time_list.append(time_check + timedelta(hours=1 + duration))
    
            iterator += 1
    
        time_list = pd.unique(time_list).tolist()
    
        iterator = 0
        time_list_return = []
        while iterator < len(time_list):
            if not((time_list[iterator] == time) or (time_list[iterator] == end_time)):
                if not ((time_list[iterator] == datetime(1900, 1, 1, 7, 0)) or (time_list[iterator] == datetime(1900, 1, 1, 21, 0))):
                    time_list_return.append(time_list[iterator])
    
            iterator += 1
    
        if len(time_list_return) > 4: time_list_return = time_list_return[:4]
        return pd.unique(time_list_return).tolist()

    def get_alternative_by_rank(self, check_rank):
        if (check_rank == 1):
            alternative = "without any movable seats, lcd projector or chalkboard"
    
        if (check_rank == 2):
            alternative = "with just chalkboard available"
    
        if (check_rank == 3):
            alternative = "with just lcd projector available"
    
        if (check_rank == 4):
            alternative = "with both lcd projector and chalkboard available"
    
        if (check_rank == 5):
            alternative = "with just movable seats available"
    
        if (check_rank == 6):
            alternative = "with both movable seats and chalkboard available"
    
        if (check_rank == 7):
            alternative = "with both movable seats and lcd projector available"
    
        if (check_rank == 8):
            alternative = "with all movable seats, lcd projector or chalkboard available"
    
        return alternative
        
    def rank_room(self, result_rooms, user_id, start_datetime, expire_datetime):
        try:
            rooms_ranked = pd.DataFrame(columns=["user", "room", "start_at", "expire_at"])
            rooms_ranked['room'] = result_rooms['Room']
            rooms_ranked['user'] = rooms_ranked['user'].fillna(user_id)
            rooms_ranked['start_at'] = rooms_ranked['start_at'].fillna(self.date_format_convert(start_datetime))
            rooms_ranked['expire_at'] = rooms_ranked['expire_at'].fillna(self.date_format_convert(expire_datetime))
            result_ranked = (self.db).check_data(rooms_ranked)
            return result_ranked
        except:
            return pd.DataFrame(columns=["user", "room", "start_at", "expire_at"])
    
    def check_alternatives_diff_equip(self, handler_input, data, building, time, duration, date, user_id, start_datetime, expire_datetime):
        iterator = 0
        rank = len(self.equipments_list)
        alternate_results = pd.DataFrame(columns=["user", "room", "start_at", "expire_at"])
        
        while iterator < len(self.equipments_list):
            alternate_results_ranked = (self.ls).search_room(building=building, equipments=self.equipments_list[iterator], start_time=time, duration=duration, date_needed=date)
            handler_input.response_builder.set_should_end_session(False)
            try:    
                if len(alternate_results_ranked.index) > 0:
                    alternate_results = self.rank_room(alternate_results_ranked, user_id, start_datetime, expire_datetime)
                    break
            except:
                pass
            
            rank -= 1
            iterator += 1
            
        try:
            if len(alternate_results.index) > 0:
                if len(alternate_results.index) == 1:
                    return_speech = data['ALTERNATE_EQUIP_MSG_SINGLE'].format(len(alternate_results.index), self.get_alternative_by_rank(rank))
                if len(alternate_results.index) > 1:
                    if len(alternate_results.index) > 4:
                        alternate_results = alternate_results[:4]
                    return_speech = data['ALTERNATE_EQUIP_MSG'].format(len(alternate_results.index), self.get_alternative_by_rank(rank))
                return 1, alternate_results.to_dict('list'), return_speech
        except:
            return 0, pd.DataFrame(columns=["user", "room", "start_at", "expire_at"]).to_dict('list'), data['NO_ALTERNATE_EQUIP_MSG']
    
        return 0, pd.DataFrame(columns=["user", "room", "start_at", "expire_at"]).to_dict('list'), data['NO_ALTERNATE_EQUIP_MSG']
    
    def check_alternatives_diff_build(self, handler_input, data, equipments, time, duration, date, user_id, start_datetime, expire_datetime):
        alternate_results = pd.DataFrame(columns=["user", "room", "start_at", "expire_at"])
        alternate_results_temp = (self.ls).search_room(equipments=equipments, start_time=time, duration=duration, date_needed=date)
            
        try:
            if len(alternate_results_temp.index) > 0:
                if len(alternate_results_temp.index) > 4:
                    alternate_results_temp = alternate_results_temp[:4]
                alternate_results = self.rank_room(alternate_results_temp, user_id, start_datetime, expire_datetime)
        except:
            pass
        
        handler_input.response_builder.set_should_end_session(False)
        
        try:
            if len(alternate_results.index) > 0:
                if len(alternate_results.index) == 1:
                    return_speech = data['ALTERNATE_BUILD_MSG_SINGLE'].format(len(alternate_results.index))
                else:
                    return_speech = data['ALTERNATE_BUILD_MSG'].format(len(alternate_results.index))
                return 1, alternate_results.to_dict('list'), return_speech
        except:
            return 0, pd.DataFrame(columns=["user", "room", "start_at", "expire_at"]).to_dict('list'), data['NO_ALTERNATE_BUILD_MSG']
    
        return 0, pd.DataFrame(columns=["user", "room", "start_at", "expire_at"]).to_dict('list'), data['NO_ALTERNATE_BUILD_MSG']
    
    def check_alternatives_diff_time(self, handler_input, data, equipments, building, time, duration, date, user_id):
        iterator = 1
        alternate_results = pd.DataFrame(columns=["user", "room", "start_at", "expire_at"])
        
        while iterator < duration:
            alternate_results_temp = (self.ls).search_room(building=building, equipments=equipments, start_time=time, duration=iterator, date_needed=date)
            check_start_datetime = datetime.combine(date, (time + timedelta(hours=0)).time())
            check_expire_datetime = datetime.combine(date, (time + timedelta(hours=iterator)).time())
            handler_input.response_builder.set_should_end_session(False)
            
            try:
                if len(alternate_results_temp.index) > 0:
                    alternate_results = self.rank_room(alternate_results_temp, user_id, check_start_datetime, check_expire_datetime)                    
                    break
            except:
                pass    
            iterator += 1
        
        try:
            if len(alternate_results.index) > 0:
                if (len(alternate_results.index) == 1) and (duration > 1):
                    return_speech = data['ALTERNATE_TIME_MSG_SINGLE'].format(len(alternate_results.index), str(duration))
                elif (len(alternate_results.index) > 1) and (duration == 1):
                    return_speech = data['ALTERNATE_TIME_MSG_DUR'].format(len(alternate_results.index), str(duration))
                elif (len(alternate_results.index) == 1) and (duration == 1):
                    return_speech = data['ALTERNATE_TIME_MSG_DUR_SINGLE'].format(len(alternate_results.index), str(duration))
                else:
                    return_speech = data['ALTERNATE_TIME_MSG'].format(len(alternate_results.index), str(duration))
                return 1, alternate_results.to_dict('list'), return_speech
        except:
            return 0, pd.DataFrame(columns=["user", "room", "start_at", "expire_at"]).to_dict('list'), data['NO_ALTERNATE_TIME_MSG']
        
        return 0, pd.DataFrame(columns=["user", "room", "start_at", "expire_at"]).to_dict('list'), data['NO_ALTERNATE_TIME_MSG']
        
    def reserve_alternate(self, data, handler_input, results_dict, user_id, intent):
        final_result = pd.DataFrame.from_dict(results_dict)
        if len(final_result['room']) == 1:
            speech = data['ALT_RESULT_MSG']
        else:
            speech = data['ALT_RESULTS_MSG']
            
        iterator = 1
        for room in final_result['room']:
            if iterator < len(final_result['room']):
                speech = speech + room + ", "
            else:
                speech = speech + room
            iterator = iterator + 1
        speech = speech + "."
        speech = str(speech)[:-1]
        
        check_user_existence = (self.db).check_user(user_id)
        if not check_user_existence:
            handler_input.attributes_manager.session_attributes["intent"] = intent + "_reserve"
            handler_input.attributes_manager.session_attributes["results"] = results_dict
            ask_reserve = data['RESERVE_MSG']
            speech = speech + "." + "\n" + ask_reserve
            handler_input.response_builder.set_should_end_session(False)
            
        else:
            check_user_expiry = (self.db).return_user_info(user_id)
            handler_input.attributes_manager.session_attributes["intent"] = intent + "_search"
            say_reserve = data['USER_CANNOT_BOOK'].format(check_user_expiry['expire_at'])
            speech = speech + "." + "\n" + say_reserve + ' ' + data['CONTINUE_MSG']
            handler_input.response_builder.set_should_end_session(False)    
        return speech
        
    def search_execution(self, handler_input, data, user_id, date, time, building, duration, seats, movable_seats, projector, chalkboard, add_speech="default"):
        date = datetime.strptime(date,'%Y-%m-%d')
        time = datetime.strptime(time,'%H:%M')
        duration = int(duration)
        seats = int(seats)
                
        equipments = {}
        if movable_seats == 'TRUE':
            equipments['free seating'] = seats
        else:
            equipments['seats'] = seats
        
        if projector == 'TRUE':
            equipments['lcd projector'] = 1
            
        if chalkboard == 'TRUE':
            equipments['blackboard'] = 1
            
        try:
            self.equipments_list.remove(equipments)
        except:
            pass
        
        start_datetime = datetime.combine(date, (time + timedelta(hours=0)).time())
        expire_datetime = datetime.combine(date, (time + timedelta(hours=duration)).time())
        
        result = (self.ls).search_room(building = building, equipments = equipments, start_time = time, duration = duration, date_needed = date)
        rooms = pd.DataFrame(columns=["user", "room", "start_at", "expire_at"])
        try:
            rooms['room'] = result['Room']
            rooms['user'] = rooms['user'].fillna(user_id)
            rooms['start_at'] = rooms['start_at'].fillna(self.date_format_convert(start_datetime))
            rooms['expire_at'] = rooms['expire_at'].fillna(self.date_format_convert(expire_datetime))
                
            final_result = (self.db).check_data(rooms)
            results_dict = (final_result).to_dict('list')
            
            if len(final_result['room']) == 0:
                speech = speech = data['NO_RESULT_MSG']
                handler_input.response_builder.set_should_end_session(True)
            else:
                if len(final_result['room']) == 1:
                    speech = data['RESULT_MSG'].format(len(final_result['room']))
                else:
                    speech = data['RESULTS_MSG'].format(len(final_result['room']))
                iterator = 1
                for room in final_result['room']:
                    if iterator < len(final_result['room']):
                        speech = speech + room + ", "
                    else:
                        speech = speech + room
                    iterator = iterator + 1
                speech = speech + "."
                speech = str(speech)[:-1]
                
                check_user_existence = (self.db).check_user(user_id)
                if not check_user_existence:
                    handler_input.attributes_manager.session_attributes["intent"] = "SearchIntent"
                    handler_input.attributes_manager.session_attributes["results"] = results_dict
                    ask_reserve = data['RESERVE_MSG']
                    speech = speech + "." + "\n" + ask_reserve
                    handler_input.response_builder.set_should_end_session(False)
                else:
                    check_user_expiry = (self.db).return_user_info(user_id)
                    say_reserve = data['USER_CANNOT_BOOK'].format(check_user_expiry['expire_at'])
                    speech = speech + "." + "\n" + say_reserve + ' ' + data['GOODBYE_MSG']
                    handler_input.response_builder.set_should_end_session(True)
                    
        except:
            try:
                check_alternate_results = (self.ls).search_room(building=building, equipments={}, start_time=time, duration=duration, date_needed=date)
                if len(check_alternate_results.index) > 0:
                    rank_1 = rank_2 = rank_3 = 0
                    
                    rank_1, result_1, response_1 = self.check_alternatives_diff_equip(handler_input, data, building, time, duration, date, user_id, start_datetime, expire_datetime)
                    handler_input.response_builder.set_should_end_session(False)
                    
                    rank_2, result_2, response_2 = self.check_alternatives_diff_build(handler_input, data, equipments, time, duration, date, user_id, start_datetime, expire_datetime)
                    handler_input.response_builder.set_should_end_session(False)
                    
                    rank_3, result_3, response_3 = self.check_alternatives_diff_time(handler_input, data, equipments, building, time, duration, date, user_id)
                    handler_input.response_builder.set_should_end_session(False)
                    
                    total_rank = rank_1 + rank_2 + rank_3
                    
                    if rank_1 == 1:
                        handler_input.attributes_manager.session_attributes["response_1"] = response_1
                        handler_input.attributes_manager.session_attributes["result_1"] = result_1
                        
                    if rank_2 == 1:
                        handler_input.attributes_manager.session_attributes["response_2"] = response_2
                        handler_input.attributes_manager.session_attributes["result_2"] = result_2
                    
                    if rank_3 == 1:
                        handler_input.attributes_manager.session_attributes["response_3"] = response_3
                        handler_input.attributes_manager.session_attributes["result_3"] = result_3
                        
                else:
                    rank_2, result_2, response_2 = self.check_alternatives_diff_build(handler_input, data, equipments, time, duration, date, user_id, start_datetime, expire_datetime)
                    handler_input.response_builder.set_should_end_session(False)
                    
                    rank_3, result_3, response_3 = self.check_alternatives_diff_time(handler_input, data, equipments, building, time, duration, date, user_id)
                    handler_input.response_builder.set_should_end_session(False)
                    
                    total_rank = rank_2 + rank_3
                    
                    if rank_2 == 1:
                        handler_input.attributes_manager.session_attributes["response_2"] = response_2
                        handler_input.attributes_manager.session_attributes["result_2"] = result_2
                    
                    if rank_3 == 1:
                        handler_input.attributes_manager.session_attributes["response_3"] = response_3
                        handler_input.attributes_manager.session_attributes["result_3"] = result_3
                    
            except:
                rank_2, result_2, response_2 = self.check_alternatives_diff_build(handler_input, data, equipments, time, duration, date, user_id, start_datetime, expire_datetime)
                handler_input.response_builder.set_should_end_session(False)
                
                rank_3, result_3, response_3 = self.check_alternatives_diff_time(handler_input, data, equipments, building, time, duration, date, user_id)
                handler_input.response_builder.set_should_end_session(False)
                
                total_rank = rank_2 + rank_3
                
                if rank_2 == 1:
                    handler_input.attributes_manager.session_attributes["response_2"] = response_2
                    handler_input.attributes_manager.session_attributes["result_2"] = result_2
                
                if rank_3 == 1:
                    handler_input.attributes_manager.session_attributes["response_3"] = response_3
                    handler_input.attributes_manager.session_attributes["result_3"] = result_3
            
            if total_rank == 0:
                speech = data['NO_RESULT_MSG'] + ' ' + data['NO_ALTERNATE_MSG'] + ' ' + data['NEW_SEARCH']
                handler_input.response_builder.set_should_end_session(True)
            elif total_rank == 1:
                speech = data['NO_RESULT_MSG'] + ' ' + data['TOTAL_ALTERNATE_MSG'].format(total_rank)
                handler_input.attributes_manager.session_attributes["intent"] = "SearchIntentAlternative"
                handler_input.response_builder.set_should_end_session(False)
            else:
                speech = data['NO_RESULT_MSG'] + ' ' + data['TOTAL_ALTERNATES_MSG'].format(total_rank)
                handler_input.attributes_manager.session_attributes["intent"] = "SearchIntentAlternative"
                handler_input.response_builder.set_should_end_session(False)

        if not(add_speech == "default"):
            speech = add_speech + " " + speech
        return speech
        

class ReserveIntent:
    
    def __init__(self):
        self.db = ReserveRooms()
        
    def date_format_convert(self, data):
        date_converted = datetime.fromisoformat(data)
        date_converted = date_converted.strftime("%Y-%m-%d %H:%M:%S")
        date_converted = datetime.strptime(date_converted,'%Y-%m-%d %H:%M:%S')
        date_converted = date_converted.strftime("%Y-%m-%d %H:%M:%S.%f")
        date_converted = datetime.strptime(date_converted,'%Y-%m-%d %H:%M:%S.%f')
        #date_format_converted = date_converted.astimezone(tz('Europe/Berlin'))
        #date_format_converted = date_format_converted.astimezone(tz('UTC'))        
        return date_converted
    
    def reserve_execution(self, handler_input, data, session_attr, room_option, reserve_room):
        room_option = int(room_option)
        session_values = session_attr["results"]
        total_records = len(session_values['room'])
        if ('room' in session_attr["results"]) and (reserve_room == 'TRUE'):
            if total_records >= room_option:
                update_dict = session_values['room'][room_option - 1]
                records_dict = dict({"room": update_dict})
                update_dict = session_values['user'][room_option - 1]
                records_dict_update = dict({"user": update_dict})
                records_dict.update(records_dict_update)
                update_dict = session_values['start_at'][room_option - 1]
                records_dict_update = dict({"start_at": self.date_format_convert(update_dict)})
                records_dict.update(records_dict_update)
                update_dict = session_values['expire_at'][room_option - 1]
                records_dict_update = dict({"expire_at": self.date_format_convert(update_dict)})
                records_dict.update(records_dict_update)
                (self.db).insert_data(records_dict)
                speak_output = data["YES_RESERVED_MSG"].format(session_values['room'][room_option - 1])
                handler_input.response_builder.set_should_end_session(True)
            else:
                speak_output = data["INVALID_OPTION"].format(total_records)
                speak_output = speak_output + ' ' + data["TRY_AGAIN"]
                handler_input.response_builder.set_should_end_session(False)
        elif ('room' in session_attr["results"]) and (reserve_room == 'FALSE'):
            speak_output = data["GOODBYE_MSG"]
            handler_input.response_builder.set_should_end_session(True)
        else:
            speak_output = data["ERROR_MSG"]
            handler_input.response_builder.set_should_end_session(True)
        return speak_output