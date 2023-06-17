# Author: Sterling Violette
# GitHub username: Sterlinghv
# Date: 10/7/2022
# Description: A program that mimics a library and the logic of operating a library.
#              Has an overarching Library class that completes many functions on top of other
#              classes such as checking out a library item. LibraryItem class is the parent
#              class of Book, Album, and Movie classes which hold logic for different
#              LibraryItems essentially. And a Patron class that defines a customer and said logic.
#              Allows checking in items, checking out, requesting items, paying fines, adding fines and more.

class Library:
    """
    A class that represents a library
    """
    def __init__(self, current_date = 0):
        """creates a library object"""
        if current_date == 0:
            self._current_date = 0
        self._holdings = []
        self._members = []

    def get_current_date(self):
        """gets the current date"""
        return self._current_date

    def set_current_date(self, date):
        """sets the current date"""
        self._current_date = date

    def add_library_item(self, library_item):
        """adds a LibraryItem object to the holdings collection"""
        self._holdings.append(library_item)

    def add_patron(self, patron):
        """adds a Patron object to the members collection"""
        self._members.append(patron)

    def lookup_library_item_from_id(self, id):
        """takes a id and returns a LibraryItem object if its in the holdings collection"""
        for item in self._holdings:
            if item.get_library_item_id() == id:
                return item
            else:
                return None

    def lookup_patron_from_id(self, id):
        """takes an id and returns a Patron object if its in the members collection """
        for patron in self._members:
            if patron.get_patron_id() == id:
                return patron
            else:
                return None


    def check_out_library_item(self, patron_id, item_id):
        """checks a library item out"""
        for patron in self._members:
            if patron.get_patron_id() == patron_id:
                for item in self._holdings:
                    if item.get_library_item_id() == item_id:
                        if item.get_location() == 'CHECKED_OUT':
                            return 'item already checked out'
                        elif item.get_location() == 'ON_HOLD_SHELF':
                            return 'item on hold by other patron'
                        else:
                            item.set_location('CHECKED_OUT')
                            item.set_checked_out_by(patron)
                            item.set_date_checked_out(self._current_date)
                            if item.get_requested_by() == patron:
                                item.set_requested_by(None)
                            patron.add_library_item(item)
                            return 'check out successful'
                    continue
                return "item not found"
            continue
        return "person not found"

    def return_library_item(self, item_id):
        """retuns a library item"""
        for item in self._holdings:
            if item.get_library_item_id() == item_id:
                if item.get_location() == 'CHECKED_OUT':
                    patron = item.get_checked_out_by()
                    patron.remove_library_item(item)
                    if item.get_requested_by() != None:
                        item.set_location('ON_HOLD_SHELF')
                    else:
                        item.set_location('ON_SHELF')
                    item.set_checked_out_by(None)
                    return "return successful"
                else:
                    return 'item already in library'
            continue
        return "item not found"

    def request_library_item(self, patron_id, item_id):
        """requests for a library item"""
        for patron in self._members:
            if patron.get_patron_id() == patron_id:
                for item in self._holdings:
                    if item.get_library_item_id() == item_id:
                        if item.get_requested_by() is not None:
                            return 'item already on hold'
                        else:
                            item.set_requested_by(patron)
                        if item.get_location == 'ON_SHELF':
                            item.set_location = 'ON_HOLD_SHELF'
                        return 'request successful'
                    continue
                return "item not found"
            continue
        return "patron not found"

    def pay_fine(self, id, amount):
        for patron in self._members:
            if patron.get_patron_id() == id:
                patron.amend_fine(-amount)
                return "payment successful"
        return "patron not found"

    def increment_current_date(self):
        """changes the current date"""
        self._current_date += 1
        for patron in self._members:
            for item in patron.get_checked_out_items():
                if (self._current_date - item.get_date_checked_out()) > item.get_check_out_length():
                    patron.amend_fine(0.10)


class LibraryItem:
    """a class that represents a LibraryItem"""

    def __init__(self, library_item_id, title, checked_out_by = None, requested_by = None, location = 'ON_SHELF' ):
        """creates a LibraryItem object"""
        self._library_item_id = library_item_id
        self._title = title
        if checked_out_by is None:
            self._checked_out_by = None
        if requested_by is None:
            self._requested_by = None
        if location == 'ON_SHELF':
            self._location = 'ON_SHELF'
        self._date_checked_out = 0

    def get_library_item_id(self):
        """gets a LibraryItem based upon id"""
        return self._library_item_id

    def get_title(self):
        """gets a title of current object"""
        return self._title

    def get_location(self):
        """gets the location of current object"""
        return self._location

    def set_location(self, location):
        """sets the location of current object"""
        self._location = location

    def get_checked_out_by(self):
        """gets who has the object (LibraryItem) checked out"""
        return self._checked_out_by

    def set_checked_out_by(self, patron):
        """sets who has the object (LibraryItem) checked out"""
        self._checked_out_by = patron

    def get_requested_by(self):
        """gets who the item is requested by"""
        return self._requested_by

    def set_requested_by(self, patron):
        """sets who the item is requested by"""
        self._requested_by = patron

    def get_date_checked_out(self):
        """gets the date when the item was checked out"""
        return self._date_checked_out

    def set_date_checked_out(self, date):
        """sets the date when the item was checked out"""
        self._date_checked_out = date


class Book(LibraryItem):
    """a class that represents a Book that inherits a LibraryItem"""

    def __init__(self, library_item_id, title, author):
        """creates a new Book object"""
        self._author = author
        self._library_item_id = library_item_id
        self._title = title
        self._checked_out_by = None
        self._requested_by = None
        self._location = 'ON_SHELF'

    def get_author(self):
        """gets the author"""
        return self._author

    def get_check_out_length(self):
        """gets the max checkout length duration"""
        return 21


class Album(LibraryItem):
    """a class that represents an Album object that inherits a LibraryItem"""

    def __init__(self, library_item_id, title, artist):
        """creates a new album object"""
        self._artist = artist
        self._library_item_id = library_item_id
        self._title = title
        self._checked_out_by = None
        self._requested_by = None
        self._location = 'ON_SHELF'

    def get_artist(self):
        """gets the artist"""
        return self._artist

    def get_check_out_length(self):
        """gets the max check out length duration"""
        return 14


class Movie(LibraryItem):
    """a class that represents a Movie that inherits a LibraryItem"""

    def __init__(self, library_item_id, title, director):
        """creates a new Movie object"""
        self._director = director
        self._library_item_id = library_item_id
        self._title = title
        self._checked_out_by = None
        self._requested_by = None
        self._location = 'ON_SHELF'

    def get_director(self):
        """gets the director"""
        return self._director

    def get_check_out_length(self):
        """gets the max checkout length duration"""
        return 7


class Patron:
    """a class that represents a patron"""

    def __init__(self, patron_id, name):
        """creates a new Patron object"""
        self._patron_id = patron_id
        self._name = name
        self._checked_out_items = []
        self._fine_amount = 0

    def get_patron_id(self):
        """gets the patron id"""
        return self._patron_id

    def get_name(self):
        """gets a name"""
        return self._name

    def get_fine_amount(self):
        """gets the fine amount"""
        return self._fine_amount

    def get_checked_out_items(self):
        """gets what LibraryItems the patron has checked out"""
        return self._checked_out_items

    def add_library_item(self, library_item):
        """adds a LibraryItem to a Patrons check out collection"""
        self._checked_out_items.append(library_item)

    def remove_library_item(self, library_item):
        """removes a LibraryItem from a Patrons checked out collection"""
        self._checked_out_items.remove(library_item)

    def get_fine_amount(self):
        """gets a Patrons fine amount"""
        return self._fine_amount

    def amend_fine(self, fine):
        """changes a Patrons fine amount"""
        self._fine_amount += fine