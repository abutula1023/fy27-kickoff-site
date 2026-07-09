# data.py

EVENT_META = {
    "title": "FY27 Kickoff: Innovation & Collaboration",
    "date": "September 18, 2026",
    "venue": "Discovery World (Exclusive Pavilion Use)",
    "hours": "7:45 AM – 3:00 PM",
    "dress_code": "Business Casual",
    "parking": "On-site underground museum garage (100 spaces max). Street parking is available if capacity is hit.",
    "catering": "Bartolotta Catering"
}

AGENDA = [
    {"time": "07:30 AM – 08:00 AM", "title": "Breakfast & Networking", "desc": "Breakfast Buffet: Breakfast Sandwiches, Potatoes, Assorted granola bars, muffins, fresh fruit, and yogurt parfaits."},
    {"time": "08:00 AM – 08:20 AM", "title": "Welcome & FY27 Theme", "desc": "Opening remarks introducing our core pillars: Collaboration, Innovation, and Growth."},
    {"time": "08:30 AM – 10:00 AM", "title": "Executive Panel", "desc": "SVP & VP led panel featuring Anna Bell (SVP Pet Consumer Marketing) and more."},
    {"time": "10:00 AM – 12:00 PM", "title": "Team Competition: Watson Adventures", "desc": "The Celebrate Milwaukee Scavenger Hunt around Discovery World (Rain plan: Indoor Trivia Slam)."},
    {"time": "12:00 PM – 01:00 PM", "title": "Lunch: Little Italy Buffet", "desc": "Chicken Marsala, Rigatoni with eggplant & mozzarella, Parmesan Green Bean salad, Rosemary potatoes, Focaccia, and dessert."},
    {"time": "01:30 PM – 02:30 PM", "title": "Networking, Wander & Swag Giveaway", "desc": "Explore the pavilion, grab custom swag, and join the Team Winner Award Ceremony."},
    {"time": "02:30 PM – 03:00 PM", "title": "Wrap Up Talk", "desc": "Final strategy takeaways. Strict guest egress from the Pavilion by 3:00 PM due to an evening event."},
    {"time": "03:00 PM – 05:00 PM", "title": "After Event Gathering (Optional)", "desc": "An informal, optional post-event social hour for team tracking and decompression."}
]

FAQS = [
    {
        "question": "What is the parking situation?",
        "answer": "Parking is available in the underground museum garage. Note that there are only 100 guaranteed spaces, so carpooling is recommended. Street parking is available nearby if the garage fills up. A parking attendant will be on-site to help guide drivers."
    },
    {
        "question": "Is the whole museum open?",
        "answer": "No. The main museum is closed to the public for annual maintenance. Our team has completely exclusive use of the lakefront West Pavilion, promenade, and patio areas."
    },
    {
        "question": "Are dietary restrictions accommodated?",
        "answer": "Yes. Our lunch buffet options include vegetarian-friendly dishes (like our baked rigatoni) and gluten-free choices. You can specify severe allergies using the confirmation form on this site."
    }
]

DUE_DATES = [
    {"date": "July 10, 2026", "task": "Sign contract and submit $3,500 deposit to secure venue.", "owner": "Chuck"},
    {"date": "August 10, 2026", "task": "Submit final timeline, initial menu selections, and room setups to DW.", "owner": "Planning Team"},
    {"date": "September 4, 2026", "task": "Finalize and communicate technical AV/microphone requirements.", "owner": "AV Lead"},
    {"date": "September 8, 2026", "task": "Final guest counts, seating charts, and floor plans due (No decreases allowed).", "owner": "Planning Team"},
    {"date": "September 11, 2026", "task": "Final venue invoice payment due.", "owner": "Finance / Chuck"}
]