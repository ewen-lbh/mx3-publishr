from consts import *

class userdata:
    @staticmethod
    def ask():
        data = {}
        # --- TRACK TYPE ---
        userdata['kind'] = ask.choices('Please enter the kind of track you want to publish',AVAIL_KINDS)
        
        # --- GETTING ARTIST ---
        if not AUTO_DETECT_OC:
            # Ask if the artist != SELF_NAME (dont ask if its a remix, obviously)
            if userdata['kind'] != 'remix':
                is_oc = ask.yesno('Did you ('+SELF_NAME+') created this from scratch ?')
            else:
                is_oc = False
        else:
            if userdata['kind'] == 'remix': is_oc = False 
            else                          : is_oc = True

        # If the artist isn't SELF_NAME, ask for it:
        if is_oc:
            userdata['artist'] = SELF_NAME
        else:
            userdata['artist'] = ask.anything('Who did the original track ?')
        
        
        # --- TRACK NAME ---
        if not userdata['kind'] in COLLECTION_KINDS:
            userdata['track'] = ask.anything('What\'s the track name ?')

            if AUTO_ADD_REMIX_SUFFIX and (REMIX_TRACK_SUFFIX not in userdata['track']) and (userdata['kind'] == 'remix'):
                    userdata['track'] += REMIX_TRACK_SUFFIX
            
        # --- COLLECTION NAME ---
        if userdata['kind'] != 'single':
            userdata['collection'] = ask.anything('Please enter the '+userdata['kind']+' name')
        else:
            userdata['collection'] = userdata['track']+SINGLE_COLLECTION_SUFFIX
        
        return data