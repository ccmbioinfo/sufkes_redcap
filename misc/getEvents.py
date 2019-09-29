from getEventIDs import getEventIDs # REDCAP API APPARENTLY DOESN'T EXPORT event_id; THIS FUNCTION IS A MAPPING BETWEEN EVENT NAMES AND event_id's

def getEvents(project, project_info, project_longitudinal): # project_info ONLY NEED FOR event_id MAPPER
    if project_longitudinal:
        events = {} # dict with unique_event_name as keys. Items include the 'pretty' event name.

        pycap_events = project.events # Inlcudes days_offset, custom_event_label etc. So far only want unique_event_name
        for pycap_event_index in range(len(pycap_events)):
            pycap_event = pycap_events[pycap_event_index]
#            pycap_events[pycap_event_index] = pycap_event["unique_event_name"]
            events[pycap_event["unique_event_name"]] = {}
            events[pycap_event["unique_event_name"]]["day_offset"] = pycap_event["day_offset"]
            events[pycap_event["unique_event_name"]]["custom_event_label"] = pycap_event["custom_event_label"]
            events[pycap_event["unique_event_name"]]["event_name"] = pycap_event["event_name"]
            events[pycap_event["unique_event_name"]]["arm_num"] = pycap_event["arm_num"]
            events[pycap_event["unique_event_name"]]["offset_min"] = pycap_event["offset_min"]
            events[pycap_event["unique_event_name"]]["offset_max"] = pycap_event["offset_max"]

            events[pycap_event["unique_event_name"]]["event_id"] = getEventIDs(pycap_event["unique_event_name"] ,project_info) # NOT SURE HOW TO GET THIS INFORMATION AUTOMATICALLY.
    else:
        events = None
    return events
