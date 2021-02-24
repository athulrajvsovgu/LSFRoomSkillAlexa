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

    def date_format_convert(self, data):
        date_converted = data.strftime("%Y-%m-%d %H:%M:%S.%f")
        date_converted = datetime.strptime(date_converted,'%Y-%m-%d %H:%M:%S.%f')
        return date_converted         
        
    def search_execution(self, handler_input, data, user_id, date, time, building, duration, seats, movable_seats, projector, chalkboard):
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
                x = 1
                for room in final_result['room']:
                    if x < len(final_result['room']):
                        speech = speech + room + ", "
                    else:
                        speech = speech + room
                    x = x + 1
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
            speech = data['NO_RESULT_MSG']
            handler_input.response_builder.set_should_end_session(True)
            
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