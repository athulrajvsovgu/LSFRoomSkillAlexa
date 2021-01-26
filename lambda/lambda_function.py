# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
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

        # if the interaction models uses synonyms  the following logic will return the ID for the value
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
        
        commons = SearchIntent()   
        speech = commons.search_execution(handler_input, data, user_id, date, time, building, duration, seats, movable_seats, projector, chalkboard)
        return handler_input.response_builder.speak(speech).response    

        
class RoomSearchNowIntentHandler(AbstractRequestHandler):
    """
    Handler for Searching Room
    """
    #round off time to nearest hour
    def round_time(self, time_now):
        if time_now.minute >= 1:
            return time_now.replace(second=0, microsecond=0, minute=0, hour=time_now.hour+2)
        else:
            return time_now.replace(second=0, microsecond=0, minute=0, hour=time_now.hour+1)

    def date_format_convert(self, data):
        date_converted = data.strftime("%Y-%m-%d %H:%M:%S.%f")
        date_converted = datetime.strptime(date_converted,'%Y-%m-%d %H:%M:%S.%f')
        return date_converted

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

        # if the interaction models uses synonyms  the following logic will return the ID for the value
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

        date = datetime.now()
        time = self.round_time(date)
        date = datetime.strftime(date,'%Y-%m-%d')
        time = datetime.strftime(time,'%H:%M')
        
        commons = SearchIntent()   
        speech = commons.search_execution(handler_input, data, user_id, date, time, building, duration, seats, movable_seats, projector, chalkboard)
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
        data = handler_input.attributes_manager.request_attributes["_"]
        slots = handler_input.request_envelope.request.intent.slots
        skill_locale = handler_input.request_envelope.request.locale
        user_id = handler_input.request_envelope.context.system.user.user_id   
        user_id = str(user_id)        
        # if the interaction models uses synonyms the following logic will return the ID for the value
        try:
            confirm_cancellation = slots["confirmCancellation"].resolutions.resolutions_per_authority[0].values[0].value.id
        except:
        # if the above fails, it means that there are no synonyms being used, so retrieve the value for the month in the regular way
            pass
        
        if confirm_cancellation == 'TRUE':
            db = ReserveRooms()
            confirmation = db.remove_reservation(user_id)
            if not confirmation:
                speech = data["NO_RESERVATION"]
            elif confirmation == 'error':
                speech = data["ERROR_RESERVATION_CANCEL"]
            else:
                speech = data["CANCEL_RESERVATION"]
        else:
            speech = data["GOODBYE_MSG"]
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
        
        if session_attr["intent"] == "SearchIntent":
            handler_input.response_builder.set_should_end_session(False)
            return handler_input.response_builder.add_directive(
                DelegateDirective(updated_intent="ReserveRoom")).response
        else:
            speak_output = data["GOODBYE_MSG"]
            handler_input.response_builder.speak(speak_output)
            handler_input.response_builder.set_should_end_session(True)
            return handler_input.response_builder.response
            

class NoHandler(AbstractRequestHandler):
    """
    Handler for No intent when audio is not playing.
    """
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        data = handler_input.attributes_manager.request_attributes["_"]
        speak_output = data["GOODBYE_MSG"]
        handler_input.response_builder.set_should_end_session(True)
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        

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
        return handler_input.response_builder.response


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