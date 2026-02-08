"""
IT Support Questions based on "The IT Support Handbook"
Organized by chapters and categories
"""

questions_data = [
    # Part I: IT Support Fundamentals
    
    # Chapter 1: Introduction to IT Support
    {"question": "What are the fundamentals of IT support?", "category": "IT Fundamentals"},
    {"question": "What is the role of IT support in a company?", "category": "IT Fundamentals"},
    {"question": "How to avoid making assumptions in IT support?", "category": "IT Fundamentals"},
    {"question": "How to overcome the technical language barrier?", "category": "IT Fundamentals"},
    {"question": "Why is the interconnectedness of IT systems important?", "category": "IT Fundamentals"},
    
    # Chapter 2: Understanding Your IT System Better
    {"question": "What is the brief history of computers?", "category": "IT Systems"},
    {"question": "What are the different types of IT systems you might encounter?", "category": "IT Systems"},
    {"question": "What are the interface standards in computing?", "category": "IT Systems"},
    {"question": "What are the different types of devices?", "category": "IT Systems"},
    {"question": "What are the main operating systems?", "category": "IT Systems"},
    {"question": "How are IT systems interconnected?", "category": "IT Systems"},
    
    # Chapter 3: Understanding Your Users
    {"question": "How to communicate effectively with users?", "category": "User Management"},
    {"question": "How to manage IT staff training?", "category": "User Management"},
    {"question": "What is learning theory in IT?", "category": "User Management"},
    {"question": "How to structure IT training and education?", "category": "User Management"},
    {"question": "How to place information in context?", "category": "User Management"},
    {"question": "How to define training objectives?", "category": "User Management"},
    {"question": "How to assess learners' knowledge?", "category": "User Management"},
    
    # Chapter 4: Flow Logic and Troubleshooting
    {"question": "How does flow logic work in troubleshooting?", "category": "Troubleshooting & Methodology"},
    {"question": "What is the process of elimination in troubleshooting?", "category": "Troubleshooting & Methodology"},
    {"question": "Why is information essential in troubleshooting?", "category": "Troubleshooting & Methodology"},
    {"question": "How to begin at the end but not work your way backward?", "category": "Troubleshooting & Methodology"},
    {"question": "How to make the impossible possible in troubleshooting?", "category": "Troubleshooting & Methodology"},
    {"question": "How to work effectively as a team to solve problems?", "category": "Troubleshooting & Methodology"},
    
    # Chapter 5: Querying Users Effectively
    {"question": "How to query users effectively to diagnose problems?", "category": "Diagnosis & Communication"},
    {"question": "Why never make assumptions during diagnosis?", "category": "Diagnosis & Communication"},
    {"question": "How to ask yes/no questions effectively?", "category": "Diagnosis & Communication"},
    {"question": "How to take the user with you on the journey?", "category": "Diagnosis & Communication"},
    {"question": "How to use a non-technical dictionary with users?", "category": "Diagnosis & Communication"},
    {"question": "How to handle online chat for support?", "category": "Diagnosis & Communication"},
    
    # Chapter 6: Finding the Root Cause
    {"question": "How to find the root cause of an IT issue?", "category": "Problem Analysis"},
    {"question": "What is the 'beginning of the end' method in troubleshooting?", "category": "Problem Analysis"},
    {"question": "How to work backward to find the source of the problem?", "category": "Problem Analysis"},
    {"question": "What are the dots you need to join?", "category": "Problem Analysis"},
    {"question": "How to keep an open mind during diagnosis?", "category": "Problem Analysis"},
    
    # Chapter 7: How IT Systems Are Structured
    {"question": "How are IT systems structured?", "category": "System Architecture"},
    {"question": "What is the Unix-verse and its importance?", "category": "System Architecture"},
    {"question": "How does IP protocol work?", "category": "System Architecture"},
    {"question": "What are aging technologies in IT?", "category": "System Architecture"},
    {"question": "What is the evolution from Windows NT to Windows 11?", "category": "System Architecture"},
    {"question": "How to create a new Android version?", "category": "System Architecture"},
    {"question": "How to live in the Internet age?", "category": "System Architecture"},
    {"question": "What is the role of YouTube in the IT ecosystem?", "category": "System Architecture"},
    
    # Chapter 8: The Human Factor
    {"question": "How does the human factor affect IT systems?", "category": "Human Factor"},
    {"question": "Why do users cause problems to IT systems?", "category": "Human Factor"},
    {"question": "What hardware problems are caused by users?", "category": "Human Factor"},
    {"question": "What software problems are caused by users?", "category": "Human Factor"},
    {"question": "How do misconfigured settings cause problems?", "category": "Human Factor"},
    {"question": "How are IT and accessibility related?", "category": "Human Factor"},
    {"question": "Why are users not IT professionals?", "category": "Human Factor"},
    {"question": "What is the 'monkey mind' in IT support?", "category": "Human Factor"},
    {"question": "Why are people complex in IT support?", "category": "Human Factor"},
    
    # Chapter 9: The Peripheral Problem
    {"question": "What is the peripheral problem?", "category": "Hardware & Peripherals"},
    {"question": "How to add legacy devices to Windows?", "category": "Hardware & Peripherals"},
    {"question": "How to configure and troubleshoot legacy devices?", "category": "Hardware & Peripherals"},
    {"question": "How to troubleshoot device drivers?", "category": "Hardware & Peripherals"},
    {"question": "What other problems can occur with peripherals?", "category": "Hardware & Peripherals"},
    
    # Chapter 10: Building and Environmental Factors
    {"question": "How do environmental factors affect IT systems?", "category": "Infrastructure & Environment"},
    {"question": "What is the impact of weather on IT equipment?", "category": "Infrastructure & Environment"},
    {"question": "How do sand, dust, water and moisture affect hardware?", "category": "Infrastructure & Environment"},
    {"question": "What is the impact of the building environment on IT?", "category": "Infrastructure & Environment"},
    {"question": "Where to optimally place Wi-Fi equipment?", "category": "Infrastructure & Environment"},
    {"question": "What is the role of Bluetooth and cellular networks?", "category": "Infrastructure & Environment"},
    {"question": "What is the difference between city and countryside for IT?", "category": "Infrastructure & Environment"},
    
    # Chapter 11: Why Good Documentation Matters
    {"question": "Why is good documentation important?", "category": "Documentation"},
    {"question": "How does documentation save time and money?", "category": "Documentation"},
    {"question": "How to use documentation for training?", "category": "Documentation"},
    {"question": "How to dumb things down in documentation?", "category": "Documentation"},
    {"question": "How to document for troubleshooting?", "category": "Documentation"},
    {"question": "What is the role of personnel and SLAs in documentation?", "category": "Documentation"},
    {"question": "How to comply with documentation requirements?", "category": "Documentation"},
    {"question": "How to create documented engineering solutions?", "category": "Documentation"},
    {"question": "How to keep documentation clear and concise?", "category": "Documentation"},
    
    # Chapter 12: Creating Troubleshooting Guides
    {"question": "How to create effective troubleshooting guides?", "category": "Guides & Procedures"},
    {"question": "How to make guides clean, concise and easy to understand?", "category": "Guides & Procedures"},
    {"question": "How to use flow logic in guides?", "category": "Guides & Procedures"},
    {"question": "What is the Dev problem in documentation?", "category": "Guides & Procedures"},
    {"question": "How to tell a story in a troubleshooting guide?", "category": "Guides & Procedures"},
    
    # Chapter 13: Creating and Managing Paperwork
    {"question": "How to create and manage IT support paperwork?", "category": "Administrative Management"},
    {"question": "What is first-line support paperwork?", "category": "Administrative Management"},
    {"question": "What is second and third-line support paperwork?", "category": "Administrative Management"},
    {"question": "How to manage engineer paperwork?", "category": "Administrative Management"},
    {"question": "What additional forms and reports are needed?", "category": "Administrative Management"},
    
    # Chapter 14: Harnessing System Tools in Windows
    {"question": "How to harness Windows system tools?", "category": "Windows Tools"},
    {"question": "How to view Windows reliability history?", "category": "Windows Tools"},
    {"question": "How to use Windows administrative tools?", "category": "Windows Tools"},
    {"question": "How to use System Information tool?", "category": "Windows Tools"},
    {"question": "How to use Performance Monitor?", "category": "Windows Tools"},
    {"question": "How to use Event Viewer?", "category": "Windows Tools"},
    {"question": "What is the role of Task Manager?", "category": "Windows Tools"},
    
    # Chapter 15: Advanced Error and Status Information
    {"question": "How to obtain advanced error and status information?", "category": "Advanced Diagnostics"},
    {"question": "How to get detailed information about errors?", "category": "Advanced Diagnostics"},
    {"question": "How to copy and save event details?", "category": "Advanced Diagnostics"},
    {"question": "How to connect to event log on another PC?", "category": "Advanced Diagnostics"},
    {"question": "How to find other Windows error logs?", "category": "Advanced Diagnostics"},
    {"question": "How to use text log files?", "category": "Advanced Diagnostics"},
    {"question": "How to use XML and ETL log files?", "category": "Advanced Diagnostics"},
    {"question": "How to analyze Dmp files?", "category": "Advanced Diagnostics"},
    
    # Chapter 16: Remote Support Tools
    {"question": "What are remote support tools?", "category": "Remote Support"},
    {"question": "How to use Remote Desktop?", "category": "Remote Support"},
    {"question": "How to use Windows Remote Assistance?", "category": "Remote Support"},
    {"question": "How to use Quick Assist?", "category": "Remote Support"},
    {"question": "How to use TeamViewer?", "category": "Remote Support"},
    {"question": "How to use RealVNC?", "category": "Remote Support"},
    {"question": "How to use LogMeIn?", "category": "Remote Support"},
    {"question": "How to use Chrome Remote Desktop?", "category": "Remote Support"},
    
    # Chapter 17: Gathering Information Remotely
    {"question": "How to gather information remotely?", "category": "Remote Administration"},
    {"question": "How to start with the Asset Tag?", "category": "Remote Administration"},
    {"question": "How to permit remote administration of PCs?", "category": "Remote Administration"},
    {"question": "How to sign in to the Registry as another user?", "category": "Remote Administration"},
    {"question": "How to use Microsoft Management Console remotely?", "category": "Remote Administration"},
    
    # Chapter 18: Helping Users to Help You
    {"question": "How to help users to help you?", "category": "User Assistance"},
    {"question": "How to use Problem Steps Recorder?", "category": "User Assistance"},
    {"question": "What Windows tool records user actions with annotated screenshots?", "category": "User Assistance"},
    {"question": "How to save screenshots?", "category": "User Assistance"},
    {"question": "How to use screencasting?", "category": "User Assistance"},
    {"question": "How to use Xbox Game Bar to capture issues?", "category": "User Assistance"},
]

# For compatibility with clustering
questions = [q["question"] for q in questions_data]