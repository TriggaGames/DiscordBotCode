class NotesHandler: 
    
    '''
    Handles notes for discord bot
    Gets called for appending notes
    '''
    
    def __init__(self) -> None: 
        # Notes storage
        self.notes: dict[str, dict[str, dict[str, list[str]]]] = {}
        
    def append_notes(self, user_name: str, notes: list[str]) -> None:
        '''Adds date and note of user notes'''
        from datetime import datetime
        now = datetime.now()
        date = now.strftime("%Y-%m-%d") # Day format
        time = now.strftime("%H:%M:%S") # Time format
        if user_name not in self.notes: self.notes[user_name] = {}
        if date not in self.notes[user_name]: self.notes[user_name][date] = {}
        if time not in self.notes[user_name][date]: self.notes[user_name][date][time] = []
        for note in notes: 
            self.notes[user_name][date][time].append(str(note))
    
    def grab_notes_d(self, user: str, date: str) -> dict: 
        '''Grab the notes from that day'''
        return self.notes[user].get(date)
        
    def grab_note_dt(self, user_name: str, date: str, time: str) -> str: 
        '''Request note at a specific day and time time'''
        return self.notes[user_name][date].get(time)
    
    def clear(self) -> None: 
        '''Clear notes'''
        self.notes = {}
        
    def load_user_notes(self, user_name: str) -> dict:
        '''Return the stored notes for a specified user'''
        return self.notes.get(user_name)
    
    def edit_note(self, user_name: str, date: str, time: str, *new_notes: tuple[str]) -> bool: 
        '''Edit any stored note, returns false if not found'''    
        if user_name in self.notes and date in self.notes[user_name] and time in self.notes[user_name][date]: 
            self.notes[user_name][date][time] = []
            for note in new_notes: 
                self.notes[user_name][date][time].append(note)
            return True
        
        return False
    
    def delete_note(self, user_name: str, date: str, time: str) -> None: 
        '''Delete note at date and time'''
        if user_name in self.notes and date in self.notes[user_name] and time in self.notes[user_name][date]:
            del self.notes[user_name][date][time]
            if not self.notes[user_name][date]: # If empty, delete
                del self.notes[user_name][date]
            
            return True
        return False
    
    def list_notes(self, user_name: str) -> list: 
        '''Return a list version of the notes'''
        return list(self.notes[user_name].keys())
    
    def list_notes_for_date(self, user_name: str, date: str) -> dict:
        '''List the notes a specified date'''
        return dict(sorted(self.notes[user_name].get(date, {}).items()))
    
    def search(self, user_name: str, keyword: str):
        '''Search given a specified keyword'''
        results = []
        user_notes = self.notes.get(user_name)
        for date, times in user_notes.items(): 
            for time, note in times.items(): 
                if keyword.lower() in note.lower():
                    results.append((date, time, note))
                    
        return results
    
if __name__ == "__main__":
    import time
    import json 
    
    nh = NotesHandler()
    
    p1_name = "Javier"
    p2_name = "Lorelie"
    
    nh.append_notes(p1_name, "Buy groceries", "Get propellant stuff")
    time.sleep(2)
    nh.append_notes(p1_name, "Find something to do on valentines day")
    
    nh.append_notes(p2_name, "Get some money")
    time.sleep(2)
    nh.append_notes(p2_name, "Get bread")
    
    p1_notes = nh.load_user_notes(p1_name)
    p2_notes = nh.load_user_notes(p2_name)
    
    with open("p1_notes.json", "w") as J: 
        json.dump(p1_notes, J, indent=4)
    with open("p2_notes.json", "w") as J: 
        json.dump(p2_notes, J, indent=4)