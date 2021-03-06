
import time

from bcreg.bcregistries import BCRegistries, system_type
from bcreg.tests.bcregistries_baseline import BCRegistriesBaseline
from bcreg.eventprocessor import EventProcessor
from bcreg.tests.eventprocessor_baseline import EventProcessorBaseline


def test_connect_bcreg():
    with BCRegistries() as bc_registries:
	    assert True

def test_connect_bcreg_baseline():
    with BCRegistriesBaseline() as bc_registries:
	    assert True

def test_compare_corp_events():
    specific_corps = [
                    '0641655',
                    #'0820416',
                    '0700450',
                    '0803224',
                    'LLC0000192',
                    'C0277609',
                    'A0072972',
                    'A0051862',
                    'C0874156',
                    '0874244',
                    '0593707',
                    'A0068919',
                    'A0064760',
                    'LLC0000234',
                    'A0077118',
                    'A0062459',
                    '0708325',
                    '0679026',
                    '0707774',
                    'C0874057',
                    'A0028374',
                    'A0053381',
                    'A0051632',
                    '0578221',
                    'A0032100',
                    '0874088',
                    '0803207',
                    #'0873646',
                    ]
    
    with BCRegistriesBaseline() as bc_registries:
        prev_event_id = 0
        max_event_id = bc_registries.get_max_event()
        baseline_corps = bc_registries.get_specific_corps(specific_corps)
        baseline_corps = bc_registries.get_unprocessed_corp_events(prev_event_id, max_event_id, baseline_corps)

    with BCRegistries() as bc_registries:
        prev_event_id = 0
        max_event_id = bc_registries.get_max_event()
        corps = bc_registries.get_specific_corps(specific_corps)
        corps = bc_registries.get_unprocessed_corp_events(prev_event_id, max_event_id, corps)
    
    assert len(baseline_corps) == len(corps)
    assert baseline_corps == corps

def test_compare_corp_infos():
    specific_corps = [
                    '0641655',
                    #'0820416',
                    '0700450',
                    '0803224',
                    'LLC0000192',
                    'C0277609',
                    'A0072972',
                    'A0051862',
                    'C0874156',
                    '0874244',
                    '0593707',
                    'A0068919',
                    'A0064760',
                    'LLC0000234',
                    'A0077118',
                    'A0062459',
                    '0708325',
                    '0679026',
                    '0707774',
                    'C0874057',
                    'A0028374',
                    'A0053381',
                    'A0051632',
                    '0578221',
                    'A0032100',
                    '0874088',
                    '0803207',
                    #'0873646',
                    ]
    
    with BCRegistries() as bc_registries:
        prev_event_id = 0
        max_event_id = bc_registries.get_max_event()
        corps = bc_registries.get_specific_corps(specific_corps)
        corps = bc_registries.get_unprocessed_corp_events(prev_event_id, max_event_id, corps)
    
    with BCRegistriesBaseline() as bc_registries:
        prev_event_id = 0
        max_event_id = bc_registries.get_max_event()
        baseline_corps = bc_registries.get_specific_corps(specific_corps)
        baseline_corps = bc_registries.get_unprocessed_corp_events(prev_event_id, max_event_id, baseline_corps)

    assert len(baseline_corps) == len(corps)
    assert baseline_corps == corps

    bcreg_loading_time = 0
    bcreg_loading_time_baseline = 0

    corp_info = {}
    with BCRegistries(True) as bc_registries:
        print('Load cached corp info')
        start_time = time.perf_counter()
        bc_registries.cache_bcreg_corps(specific_corps)
        for corp in corps:
            print(corp)
            corp_info[corp['CORP_NUM']] = bc_registries.get_bc_reg_corp_info(corp['CORP_NUM'], corp['LAST_EVENT_ID'])
        bcreg_loading_time = bcreg_loading_time + (time.perf_counter() - start_time)

    print('new load:', bcreg_loading_time)

    corp_info_baseline = {}
    with BCRegistriesBaseline() as bc_registries:
        print('Run baseline')
        start_time = time.perf_counter()
        for corp in corps:
            print(corp)
            corp_info_baseline[corp['CORP_NUM']] = bc_registries.get_bc_reg_corp_info(corp['CORP_NUM'], corp['LAST_EVENT_ID'])
        bcreg_loading_time_baseline = bcreg_loading_time_baseline + (time.perf_counter() - start_time)

    print('baseline:', bcreg_loading_time_baseline, 'new load:', bcreg_loading_time)

    #for corp in corps:
    #    assert corp_info[corp['CORP_NUM']] == corp_info_baseline[corp['CORP_NUM']]

    corp_creds = {}
    with EventProcessor() as event_processor:
        for corp in corps:
            corp_creds[corp['CORP_NUM']] = event_processor.generate_credentials(system_type, corp['PREV_EVENT_ID'], corp['LAST_EVENT_ID'], 
    										corp['CORP_NUM'], corp_info[corp['CORP_NUM']])

    corp_creds_baseline = {}
    with EventProcessorBaseline() as event_processor:
        for corp in corps:
            corp_creds_baseline[corp['CORP_NUM']] = event_processor.generate_credentials(system_type, corp['PREV_EVENT_ID'], corp['LAST_EVENT_ID'], 
    										corp['CORP_NUM'], corp_info_baseline[corp['CORP_NUM']])

    diffs = []
    for corp in corps:
        if corp_creds[corp['CORP_NUM']] != corp_creds_baseline[corp['CORP_NUM']]:
            diffs.append(corp['CORP_NUM'])
    print(diffs)

    assert 0 == len(diffs)


