# data.py

EVENT_META = {
    "title": "CSP 2027 Fiscal Year Kick-Off",
    "date": "September 18, 2026",
    "venue": "Discovery World, 500 North Harbor Drive, Milwaukee, WI 53202",
    "hours": "8:00 AM – 3:00 PM",
    "dress_code": "Business Casual — Please wear comfortable shoes for the group activity (no high heels)",
    "parking": (
        "On-site underground museum garage with limited capacity. "
        "Street parking is available if the garage fills up."
    ),
    "catering": "Bartolotta Catering",
}

PRESENTATION_DESC = (
    "A series of short presentations from CSP team members focused on Growth, Innovation, "
    "Collaboration, and other key FY27 priorities."
)

PANEL_DESC = (
    "Panel moderated by Melissa McCance – Director – Corporate HR.\n\n"
    "Panelists:\n"
    "- Ernie – VP Innovation - Pet\n"
    "- Alex Thompson – VP of Pet eComm\n"
    "- Anna Bell – Sr VP Pet Marketing\n"
    "- Chris Walter – SVP and CIO Central Garden and Pet\n"
    "- Lonnie Hobbs Jr. – Professor at Kansas State University\n\n"
    "The panel will answer questions submitted by attendees, with a strong focus "
    "on Growth, Innovation, Collaboration, and the future of CSP."
)

AGENDA = [
    {
        "time": "07:30 AM – 08:00 AM",
        "title": "Breakfast & Networking (Optional)",
        "desc": (
            "Optional breakfast and networking before the formal program begins at 8:00 AM. "
            "Breakfast buffet with breakfast sandwiches, potatoes, assorted granola bars, "
            "muffins, fresh fruit, and yogurt parfaits."
        ),
    },
    {
        "time": "08:00 AM – 08:15 AM",
        "title": "Opening Welcome",
        "desc": "Opening remarks to welcome attendees to the CSP 2027 Fiscal Year Kick-Off.",
    },
    {
        "time": "08:15 AM – 08:30 AM",
        "title": "FY 2027 Themes",
        "desc": (
            "Introduction to the FY27 theme and our core pillars: Collaboration, Innovation, "
            "and Growth."
        ),
    },
    {
        "time": "08:30 AM – 09:50 AM",
        "title": "AM Presentations",
        "desc": PRESENTATION_DESC,
    },
    {
        "time": "09:50 AM – 10:00 AM",
        "title": "Group Picture",
        "desc": "We will all head out back by the Amphitheatre for a group picture.",
    },
    {
        "time": "10:00 AM – 12:00 PM",
        "title": "Group Competition!",
        "desc": "Event hosted by Watson Adventures.",
    },
    {
        "time": "12:00 PM – 01:00 PM",
        "title": "Lunch",
        "desc": (
            "Chicken Marsala, rigatoni with eggplant and mozzarella, Parmesan green bean "
            "salad, rosemary potatoes, focaccia, and dessert."
        ),
    },
    {
        "time": "01:00 PM – 01:10 PM",
        "title": "Segue to Panel",
        "desc": "Transition to the panel discussion.",
    },
    {
        "time": "01:10 PM – 02:15 PM",
        "title": "Panel Discussion",
        "desc": PANEL_DESC,
    },
    {
        "time": "02:15 PM – 02:30 PM",
        "title": "Team Award Ceremony!",
        "desc": "Recognition of the team competition winner.",
    },
    {
        "time": "02:30 PM – 02:45 PM",
        "title": "Closing Comments",
        "desc": "Final takeaways and closing remarks.",
    },
    {
        "time": "02:45 PM – 03:00 PM",
        "title": "Depart",
        "desc": "Guests must leave the Pavilion by 3:00 PM.",
    },
    {
        "time": "03:00 PM – 05:00 PM",
        "title": "After-Event Gathering (Optional)",
        "desc": (
            "An informal, optional post-event gathering for networking, "
            "conversation, and decompression."
        ),
    },
]

FAQS = [
    {
        "question": "What is the parking situation?",
        "answer": (
            "Parking is available in the underground museum garage, but capacity is "
            "limited, so carpooling is recommended. Street parking is available nearby "
            "if the garage fills up. A parking attendant will be on-site to help guide drivers."
        ),
    },
    {
        "question": "Is the whole museum open?",
        "answer": (
            "No. The main museum is closed to the public for annual maintenance. "
            "Our team has exclusive use of the lakefront West Pavilion, promenade, "
            "and patio areas."
        ),
    },
    {
        "question": "Are dietary restrictions accommodated?",
        "answer": (
            "Yes. The lunch buffet includes vegetarian-friendly and gluten-free choices. "
            "Please identify severe allergies or other dietary needs on the confirmation form."
        ),
    },
]
