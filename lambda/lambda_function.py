# -*- coding: utf-8 -*-

"""
This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
session persistence, api calls, and more.
This sample is built using the handler classes approach in skill builder.
"""

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
import ask_sdk_model.services
import pandas as pd
import ask_sdk_core.utils as ask_utils
from alexa import data
from common import SearchIntent, ReserveIntent
from db_handler import ReserveRooms
from datetime import date, datetime, timedelta, timezone
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.dialog import (ElicitSlotDirective, DelegateDirective)
from ask_sdk_core.dispatch_components import (AbstractRequestHandler, AbstractExceptionHandler,
    AbstractResponseInterceptor, AbstractRequestInterceptor)
from ask_sdk_model import (Intent, Response, IntentRequest, DialogState, 
    IntentConfirmationStatus, Slot, SlotConfirmationStatus)
from ask_sdk_model.slu.entityresolution import (
    Resolutions,Resolution, ValueWrapper, Value, Status, StatusCode)    
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])
from pytz import timezone as tz
    
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """
    Handler for Skill Launch
    """
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        user_id = handler_input.request_envelope.context.system.user.user_id
        user_id = str(user_id)
        db = ReserveRooms()
        check_user_expiry = db.return_user_info(user_id)
        handler_input.attributes_manager.session_attributes["check_user_expiry"] = check_user_expiry
        if (check_user_expiry == 'empty') or (check_user_expiry == 'error'):
            speech = data["WELCOME_MSG"]
        else:
            room = check_user_expiry['room']
            start_at = check_user_expiry['start_at']
            expire_at = check_user_expiry['expire_at']
            speech = data['WELCOME_BACK_MSG'].format(room, start_at, expire_at)
        reprompt = data["WELCOME_REPROMPT_MSG"]
        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response
        

class RoomSearchIntentHandler(AbstractRequestHandler):
    """
    Handler for Searching Room
    """
        #round off time to nearest hour
    def round_time(self, time_now):
        if time_now.minute >= 1:
            return time_now.replace(second=0, microsecond=0, minute=0, hour=time_now.hour+1)
        else:
            return time_now.replace(second=0, microsecond=0, minute=0, hour=time_now.hour)
            
    def can_handle(self, handler_input):
        return is_intent_name("FindRoomWithDate")(handler_input)

    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        slots = handler_input.request_envelope.request.intent.slots
        skill_locale = handler_input.request_envelope.request.locale
        user_id = handler_input.request_envelope.context.system.user.user_id
        user_id = str(user_id)
            
        # extract slot values
        date = slots["date"].value
        time = slots["time"].value
        duration = slots["duration"].value
        seats = slots["seats"].value

        # if the interaction models uses synonyms the following logic will return the ID for the value
        try:
            movable_seats = slots["movableSeats"].resolutions.resolutions_per_authority[0].values[0].value.id
            projector = slots["projector"].resolutions.resolutions_per_authority[0].values[0].value.id
            chalkboard = slots["chalkboard"].resolutions.resolutions_per_authority[0].values[0].value.id
        except:
        # if the above fails, it means that there are no synonyms being used, so retrieve the value for the month in the regular way
            pass

        if slots["buildingNumber"].value:
            building = slots["buildingNumber"].value
            building = int(building)   
        
        check_date = datetime.strptime(date,'%Y-%m-%d')
        if(check_date.isoweekday() == 7):
            check_date = check_date + timedelta(days=1)
            add_speech = "Since its not possible to reserve room on Sunday, the search was done for Monday same time."
            date = datetime.strftime(check_date,'%Y-%m-%d')
        else:
            add_speech = "default"
        
        commons = SearchIntent()   
        speech = commons.search_execution(handler_input, data, user_id, date, time, building, duration, seats, movable_seats, projector, chalkboard, add_speech)
        return handler_input.response_builder.speak(speech).response
        

class RoomSearchNowIntentHandler(AbstractRequestHandler):
    """
    Handler for Searching Room
    """
    #round off time to nearest hour
    def round_time(self, time_now):
        if time_now.minute >= 1:
            return time_now.replace(second=0, microsecond=0, minute=0, hour=time_now.hour+1)
        else:
            return time_now.replace(second=0, microsecond=0, minute=0, hour=time_now.hour)

    def return_date_time(self, check):
        start_low = datetime(1900, 1, 1, 0, 0).time()
        start_high = datetime(1900, 1, 1, 8, 0).time()
        end_low = datetime(1900, 1, 1, 20, 0).time()
        end_high = datetime(1900, 1, 1, 23, 59).time()
        
        if start_low < check.time() < start_high:
            if(check.isoweekday() == 7):
                date = check + timedelta(days=1)
                add_speech = "Since its not possible to reserve room on Sunday, the search was done for Monday 8:00 a.m."
            else: 
                date = check
                add_speech = "Since its not possible to reserve room now, the search was done for 8:00 a.m."
            time = "08:00"
            
        elif end_low < check.time() < end_high:
            date = check + timedelta(days=1)
            if(date.isoweekday() == 7):
                date = check + timedelta(days=1)
                add_speech = "Since its not possible to reserve room now and Sunday, the search was done for next day 8:00 a.m."
            else:
                add_speech = "Since its not possible to reserve room now, the search was done for next day 8:00 a.m."
            time = "08:00"
            
        elif start_high < check.time() < end_low:
            if(check.isoweekday() == 7):
                date = check + timedelta(days=1)
                add_speech = "Since its not possible to reserve room on Sunday, the search was done for Monday same time."
            else:
                date = check
                add_speech = "default"
            time = datetime.strftime(self.round_time(date),'%H:%M')
    
        date = datetime.strftime(date,'%Y-%m-%d')
        return date, time, add_speech

    def can_handle(self, handler_input):
            return is_intent_name("FindRoomImmediately")(handler_input)
        
    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        slots = handler_input.request_envelope.request.intent.slots
        skill_locale = handler_input.request_envelope.request.locale
        user_id = handler_input.request_envelope.context.system.user.user_id   
        user_id = str(user_id)
        
        # extract slot values
        duration = slots["duration"].value
        seats = slots["seats"].value

        # if the interaction models uses synonyms the following logic will return the ID for the value
        try: 
            movable_seats = slots["movableSeats"].resolutions.resolutions_per_authority[0].values[0].value.id
            projector = slots["projector"].resolutions.resolutions_per_authority[0].values[0].value.id
            chalkboard = slots["chalkboard"].resolutions.resolutions_per_authority[0].values[0].value.id
        except:
        # if the above fails, it means that there are no synonyms being used, so retrieve the value for the month in the regular way
            pass
        
        if slots["buildingNumber"].value:
            building = slots["buildingNumber"].value
            building = int(building)        

        date, time, add_speech = self.return_date_time(datetime.now())
        
        commons = SearchIntent()
        speech = commons.search_execution(handler_input, data, user_id, date, time, building, duration, seats, movable_seats, projector, chalkboard, add_speech)
        return handler_input.response_builder.speak(speech).response 
        

class ReserveRoomIntentHandler(AbstractRequestHandler):
    """
    Handler for Searching Room
    """
    def can_handle(self, handler_input):
        return is_intent_name("ReserveRoom")(handler_input)
    
    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        slots = handler_input.request_envelope.request.intent.slots
        skill_locale = handler_input.request_envelope.request.locale
        session_attr = handler_input.attributes_manager.session_attributes
        # if the interaction models uses synonyms the following logic will return the ID for the value
        try:
            room_option = slots["roomOption"].resolutions.resolutions_per_authority[0].values[0].value.id
            reserve_room = slots["roomReserve"].resolutions.resolutions_per_authority[0].values[0].value.id
        except:
        # if the above fails, it means that there are no synonyms being used, so retrieve the value for the month in the regular way
            pass
        
        commons = ReserveIntent()
        speech = commons.reserve_execution(handler_input, data, session_attr, room_option, reserve_room)
        return handler_input.response_builder.speak(speech).response
        
        
class RemoveReservationIntentHandler(AbstractRequestHandler):
    """
    Handler for Searching Room
    """
    def can_handle(self, handler_input):
        return is_intent_name("RemoveReservation")(handler_input)
    
    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        data = handler_input.attributes_manager.request_attributes["_"]
        skill_locale = handler_input.request_envelope.request.locale
        slots = handler_input.request_envelope.request.intent.slots
        user_id = handler_input.request_envelope.context.system.user.user_id   
        user_id = str(user_id)
        
        try:
            check_user_expiry = session_attr["check_user_expiry"]
        except:
            db = ReserveRooms()
            check_user_expiry = db.return_user_info(user_id)
        
        if (check_user_expiry == 'empty') or (check_user_expiry == 'error'):
            logger.info("speech")
            speech = data["NO_RESERVATION"]
            logger.info(speech)
            handler_input.response_builder.set_should_end_session(True)
            return handler_input.response_builder.speak(speech).response
        else:
            speech = data["CONFIRM_CANCELLATION"]
            handler_input.attributes_manager.session_attributes["intent"] = "RemoveReservation"
            handler_input.response_builder.set_should_end_session(False)
            return handler_input.response_builder.speak(speech).response        


class YesHandler(AbstractRequestHandler):
    """
    Handler for Yes intent when audio is not playing.
    """
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        data = handler_input.attributes_manager.request_attributes["_"]
        session_attr = handler_input.attributes_manager.session_attributes
        skill_locale = handler_input.request_envelope.request.locale
        user_id = handler_input.request_envelope.context.system.user.user_id
        commons = SearchIntent()
        
        user_id = str(user_id)
        try:
            intent = session_attr["intent"]
        except:
            intent = ""
                    
        if (intent == "SearchIntent") or (intent == "Alternate_1_reserve") or (intent == "Alternate_2_reserve") or (intent == "Alternate_3_reserve"):
            logger.info("Yes intent reserve")
            logger.info(intent)
            handler_input.response_builder.set_should_end_session(False)
            return handler_input.response_builder.add_directive(
                DelegateDirective(updated_intent="ReserveRoom")).response
        
        elif intent == "Alternate_1_search":
            try:
                response_2 = session_attr["response_2"]
                result_2 = session_attr["result_2"]
                response_2 = response_2 + ' ' + commons.reserve_alternate(data, handler_input, result_2, user_id, "Alternate_2")
                handler_input.response_builder.set_should_end_session(False)
                logger.info("Alternate_1_search_response_2")
                return handler_input.response_builder.speak(response_2).response
            except:
                try:
                    response_3 = session_attr["response_3"]
                    result_3 = session_attr["result_3"]
                    response_3 = response_3 + ' ' + commons.reserve_alternate(data, handler_input, result_3, user_id, "Alternate_3")
                    handler_input.response_builder.set_should_end_session(False)
                    logger.info("Alternate_1_search_response_3")
                    return handler_input.response_builder.speak(response_3).response
                except:
                    speech = data['NO_MORE_ALTERNATE_MSG'] + ' ' + data['NEW_SEARCH']
                    handler_input.response_builder.set_should_end_session(True)
                    logger.info("Alternate_1_search_exception")
                    return handler_input.response_builder.speak(speech).response
        
        elif intent == "Alternate_2_search":
            try:
                response_3 = session_attr["response_3"]
                result_3 = session_attr["result_3"]
                response_3 = response_3 + ' ' + commons.reserve_alternate(data, handler_input, result_3, user_id, "Alternate_3")
                handler_input.response_builder.set_should_end_session(False)
                logger.info("Alternate_2_search_response_3")
                return handler_input.response_builder.speak(response_3).response
            except:
                speech = data["NO_MORE_ALTERNATE_MSG"] + ' ' + data['NEW_SEARCH']
                handler_input.response_builder.set_should_end_session(True)
                logger.info("Alternate_2_search_exception")
                return handler_input.response_builder.speak(speech).response
        
        elif intent == "Alternate_3_search":
            speech = data["NO_MORE_ALTERNATE_MSG"] + ' ' + data['NEW_SEARCH']
            handler_input.response_builder.set_should_end_session(True)
            logger.info("Alternate_3_search_exception")
            return handler_input.response_builder.speak(speech).response
            
        elif intent == "FindRoomWithDate":
            handler_input.response_builder.set_should_end_session(False)
            return handler_input.response_builder.add_directive(
                DelegateDirective(updated_intent="FindRoomWithDate")).response
            
        elif intent == "SearchIntentAlternative":
            try:
                response_1 = session_attr["response_1"]
                result_1 = session_attr["result_1"]
                response_1 = response_1 + ' ' + commons.reserve_alternate(data, handler_input, result_1, user_id, "Alternate_1")
                handler_input.response_builder.set_should_end_session(False)
                logger.info("SearchIntentAlternative_response_1")
                return handler_input.response_builder.speak(response_1).response                
            except:
                try:
                    response_2 = session_attr["response_2"]
                    result_2 = session_attr["result_2"]
                    response_2 = response_2 + ' ' + commons.reserve_alternate(data, handler_input, result_2, user_id, "Alternate_2")
                    handler_input.response_builder.set_should_end_session(False)
                    logger.info("SearchIntentAlternative_response_2")
                    return handler_input.response_builder.speak(response_2).response
                except:
                    try:
                        response_3 = session_attr["response_3"]
                        result_3 = session_attr["result_3"]
                        response_3 = response_3 + ' ' + commons.reserve_alternate(data, handler_input, result_3, user_id, "Alternate_3")
                        handler_input.response_builder.set_should_end_session(False)
                        logger.info("SearchIntentAlternative_response_3")
                        return handler_input.response_builder.speak(response_3).response
                    except:
                        speech = data["NO_MORE_ALTERNATE_MSG"]
                        handler_input.response_builder.set_should_end_session(True)
                        logger.info("SearchIntentAlternative_exception")
                        return handler_input.response_builder.speak(speech).response
                
        elif intent == "RemoveReservation":
            db = ReserveRooms()
            confirmation = db.remove_reservation(user_id)
            if not confirmation:
                speech = data["NO_RESERVATION"]
            elif confirmation == 'error':
                speech = data["ERROR_RESERVATION_CANCEL"]
            else:
                speech = data["CANCEL_RESERVATION"]
            handler_input.response_builder.set_should_end_session(True)
            return handler_input.response_builder.speak(speech).response
            
        else:
            logger.info("Yes intent goodbye")
            logger.info(intent)
            speech = data["GOODBYE_MSG"]
            handler_input.response_builder.set_should_end_session(True)
            return handler_input.response_builder.speak(speech).response
            

class NoHandler(AbstractRequestHandler):
    """
    Handler for No intent when audio is not playing.
    """
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        data = handler_input.attributes_manager.request_attributes["_"]
        session_attr = handler_input.attributes_manager.session_attributes
        skill_locale = handler_input.request_envelope.request.locale
        user_id = handler_input.request_envelope.context.system.user.user_id
        commons = SearchIntent()
        
        user_id = str(user_id)
        try:
            intent = session_attr["intent"]
        except:
            intent = ""
        
        if intent == "Alternate_1_reserve":
            logger.info("Alternate_1_reserve")
            try:
                response_2 = session_attr["response_2"]
                result_2 = session_attr["result_2"]
                response_2 = response_2 + ' ' + commons.reserve_alternate(data, handler_input, result_2, user_id, "Alternate_2")
                handler_input.response_builder.set_should_end_session(False)
                logger.info("Alternate_1_reserve_response_2")
                return handler_input.response_builder.speak(response_2).response                
            except:
                try:
                    response_3 = session_attr["response_3"]
                    result_3 = session_attr["result_3"]
                    response_3 = response_3 + ' ' + commons.reserve_alternate(data, handler_input, result_3, user_id, "Alternate_3")
                    handler_input.response_builder.set_should_end_session(False)
                    logger.info("Alternate_1_reserve_response_3")
                    return handler_input.response_builder.speak(response_3).response
                except:
                    speech = data['NO_MORE_ALTERNATE_MSG'] + ' ' + data['NEW_SEARCH']
                    handler_input.response_builder.set_should_end_session(True)
                    logger.info("Alternate_1_reserve_exception")
                    return handler_input.response_builder.speak(speech).response
        
        elif intent == "Alternate_2_reserve":
            try:
                logger.info("Alternate_2_reserve")
                response_3 = session_attr["response_3"]
                result_3 = session_attr["result_3"]
                response_3 = response_3 + ' ' + commons.check_reserve_possible(data, handler_input, result_3, user_id, "Alternate_3")
                handler_input.response_builder.set_should_end_session(False)
                logger.info("Alternate_1_reserve_response_3")
                return handler_input.response_builder.speak(response_3).response
            except:
                speech = data["NO_MORE_ALTERNATE_MSG"] + ' ' + data['NEW_SEARCH']
                handler_input.response_builder.set_should_end_session(True)
                logger.info("Alternate_2_reserve_exception")
                return handler_input.response_builder.speak(speech).response
        
        elif intent == "Alternate_3_reserve":
            speech = data["NO_MORE_ALTERNATE_MSG"] + ' ' + data['NEW_SEARCH']
            handler_input.response_builder.set_should_end_session(True)
            logger.info("Alternate_3_reserve")
            return handler_input.response_builder.speak(speech).response
        
        else:
            logger.info("No intent goodbye")
            logger.info(intent)
            speech = data["GOODBYE_MSG"]
            handler_input.response_builder.set_should_end_session(True)
            return handler_input.response_builder.speak(speech).response
        

class HelpIntentHandler(AbstractRequestHandler):
    """
    Handler for Help Intent.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        data = handler_input.attributes_manager.request_attributes["_"]
        speak_output = data["HELP_MSG"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """
    Single handler for Cancel and Stop Intent.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        data = handler_input.attributes_manager.request_attributes["_"]
        session_attr = handler_input.attributes_manager.session_attributes
        
        try:
            intent = session_attr["intent"]
        except:
            intent = ""
            
        if intent == "FindRoomImmediately":
            speak_output = data["TIME_ISSUE"] + " " + data["GOODBYE_MSG"]
        else:    
            speak_output = data["GOODBYE_MSG"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """
    Handler for Session End.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # Any cleanup logic goes here.
        data = handler_input.attributes_manager.request_attributes["_"]
        speak_output = data["TIMEOUT_MSG"] + ' ' + data["NEW_SEARCH"]
        return handler_input.response_builder.speak(speak_output).response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        data = handler_input.attributes_manager.request_attributes["_"]
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = data["REFLECTOR_MSG"].format(intent_name)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        data = handler_input.attributes_manager.request_attributes["_"]
        speak_output = data["ERROR_MSG"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


class LocalizationInterceptor(AbstractRequestInterceptor):
    """
    Add function to request attributes, that can load locale specific data.
    """

    def process(self, handler_input):
        skill_locale = handler_input.request_envelope.request.locale

        # localized strings stored in language_strings.json
        with open("language_strings.json") as language_prompts:
            language_data = json.load(language_prompts)
        # set default translation data to broader translation
        data = language_data[skill_locale[:2]]
        # if a more specialized translation exists, then select it instead
        # example: "fr-CA" will pick "fr" translations first, but if "fr-CA" translation exists,
        #          then pick that instead
        if skill_locale in language_data:
            data.update(language_data[skill_locale])
        handler_input.attributes_manager.request_attributes["_"] = data

        # configure the runtime to treat time according to the skill locale
        skill_locale = skill_locale.replace('-','_')
        locale.setlocale(locale.LC_TIME, skill_locale)
        
        
sb = CustomSkillBuilder(persistence_adapter=s3_adapter)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(RoomSearchIntentHandler())
sb.add_request_handler(RoomSearchNowIntentHandler())
sb.add_request_handler(ReserveRoomIntentHandler())
sb.add_request_handler(RemoveReservationIntentHandler())
sb.add_request_handler(YesHandler())
sb.add_request_handler(NoHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn’t override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())

lambda_handler = sb.lambda_handler()