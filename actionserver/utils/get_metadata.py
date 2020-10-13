from rasa.core.trackers import DialogueStateTracker

def get_latest_metadata(tracker:DialogueStateTracker):
    events = tracker.current_state()['events']
    # user_events = []
    # for e in events:
    #     if e['event'] == 'user':
    #         user_events.append(e)

    # return user_events[-1]['metadata']


    #===================================    
    #   Using List Comprihension       
    #===================================

    li =  [ e for e in events if e['event'] == 'user' ][-1]['metadata']
    return li
