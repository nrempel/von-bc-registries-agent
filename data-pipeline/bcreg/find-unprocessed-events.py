#!/usr/bin/python
import psycopg2
import datetime
from bcreg.config import config
from bcreg.eventprocessor import EventProcessor
from bcreg.bcregistries import BCRegistries, system_type


with BCRegistries() as bc_registries:
    with EventProcessor() as event_processor:
        print("Get last processed event")
        prev_event_id = event_processor.get_last_processed_event(system_type)
        
        print("Get last max event")
        max_event_id = bc_registries.get_max_event()
        
        # get unprocessed corps (there are about 2700)
        print("Get unprocessed corps")
        corps = bc_registries.get_unprocessed_corps(prev_event_id, max_event_id)
        
        print("Find unprocessed events for each corp")
        corps = bc_registries.get_unprocessed_corp_events(prev_event_id, max_event_id, corps)
        
        print("Update our queue")
        event_processor.update_corp_event_queue(system_type, corps, max_event_id)


