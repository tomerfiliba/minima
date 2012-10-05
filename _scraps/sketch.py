def schedule_meeting_page():
    with Page(title = "Touchbase - Scheduling Assistant") as doc:
        with Section(title = "What") as sect_what:
            business = Button(img = "/img/type-business.jpg", title = "Business Meeting")),
            friends = Button(img = "/img/type-friends.jpg", title = "Friends Gathering")),
            phone = Button(img = "/img/type-phonecall.jpg", title = "Phone Call")),
            other = Button(img = "/img/type-other.jpg", title = "Other", )),
            sect_what.ready_on(meeting_type)
        
        with Section(title = "Who") as sect_who:
            current_contact = AutocompleteTextbox(api_url = "/api/get-contacts")
            RecentList(api_url = "/api/get-recent-contants", params = {"limit" : 5})
            contacts = ContactList(source = current_contact)
            btn_who_next = Button("Next")
            sect_who.ready_on(btn_who_next)

        with Section(title = "Where") as sect_where:
            location = AutocompleteTextbox(api_url = "/api/get-location")
            RecentList(api_url = "/api/get-recent-locations", params = {"contacts" : contacts, 
                "type" : meeting_type, "limit" : 5})
            sect_who.ready_on(location)

        with Section(title = "When") as sect_when:
            CalendarBox(api_url = "/api/get-meeting-times", params = {"contacts" : contacts, 
                "type" : meeting_type, "location" : location})
            btn_when_next = Button("Next")
            sect_when.ready_on(btn_when_next)

        with Section(title = "Review"):
            
            btn_send = Button("Send Invitations", )


    return doc
