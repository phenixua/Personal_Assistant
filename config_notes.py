import json

class NoteManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.file_path, "r", encoding = "UTF-8") as file:
                notes = json.load(file)
            return notes
        except FileNotFoundError:
            return []

    def save_notes(self):
        with open(self.file_path, "w", encoding = "UTF-8") as file:
            json.dump(self.notes, file, ensure_ascii = False, indent = 4)

    def add_note(self, title, body, tags=None):
        note = {"title": title, "body": body, "tags": tags or []}
        self.notes.append(note)
        self.save_notes()

    def edit_note(self, title, new_title = "", new_body = "", new_tags = ""):
        for note in self.notes:
            if note["title"] == title:
                if new_title != "":
                    note["title"] = new_title
                if new_body != "":
                    note["body"] = new_body
                if new_tags != "":
                    note["tags"] = new_tags

        self.save_notes()

    def delete_note(self, title):
        for note in self.notes:
            if note['title'] == title:
                self.notes.remove(note)
                self.save_notes()
                break

    def search_notes(self, query):
        results = []
        for note in self.notes:
            if (
                query.lower() in note["title"].lower()
                or query.lower() in note["body"].lower()
                or any(query.lower() in tag.lower() for tag in note["tags"])
            ):
                results.append(note)
        return results

    def sort_notes_by_tags(self, tag):
        sorted_notes = [note for note in self.notes if tag.lower() in [t.lower() for t in note["tags"]]]
        return sorted_notes
    
    def show_all_notes(self):
        return self.notes

    def clear_all_notes(self):
        self.notes = []
        self.save_notes()

if __name__ == "__main__":
    manager = NoteManager("notes.json")