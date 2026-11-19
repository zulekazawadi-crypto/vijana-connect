from datetime import date
from home.models import Opportunity, Training

# Only fill the database if it is empty
if not Opportunity.objects.exists():
    data = [
        ("Software Developer", "TechHub Kenya", "job", "Nairobi", "Full-time", "Build and maintain web applications with a young, growing team.", date(2026, 12, 30)),
        ("Sales Assistant", "Savanna Supermarkets", "vacancy", "Eldoret", "Contract", "Assist customers, manage stock and support daily store operations.", date(2026, 12, 20)),
        ("ICT Attachment", "BrightPath Media", "attachment", "Nakuru", "3 Months", "Gain hands-on experience in IT support, networking and web design.", date(2027, 1, 10)),
        ("Accounts Clerk", "GreenFarm Ltd", "job", "Kisumu", "Full-time", "Handle invoices, payments and monthly financial records.", date(2027, 1, 15)),
        ("Customer Care Officer", "Nairobi Health Clinic", "vacancy", "Nairobi", "Full-time", "Welcome patients, answer calls and manage appointments.", date(2027, 1, 5)),
        ("Business Attachment", "Rift Valley Traders", "attachment", "Mombasa", "2 Months", "Learn marketing, record keeping and customer service on the job.", date(2026, 12, 28)),
        ("Graphic Designer", "Creative Minds Studio", "job", "Nairobi", "Full-time", "Design logos, posters and social media content for clients.", date(2027, 1, 18)),
        ("Delivery Rider", "QuickMove Logistics", "job", "Nakuru", "Full-time", "Deliver parcels within town. Own motorbike and licence required.", date(2026, 12, 22)),
        ("Farm Supervisor", "Highland Agro Ltd", "vacancy", "Kericho", "Contract", "Oversee daily farm activities and manage a small team of workers.", date(2027, 1, 12)),
        ("Front Office Receptionist", "Lakeview Hotel", "vacancy", "Kisumu", "Full-time", "Welcome guests, handle bookings and answer enquiries.", date(2027, 1, 8)),
        ("Engineering Attachment", "PowerGrid Solutions", "attachment", "Nairobi", "3 Months", "Work with electrical engineers on installations and maintenance.", date(2027, 1, 20)),
        ("Journalism Attachment", "Daily Voice Media", "attachment", "Eldoret", "2 Months", "Learn news writing, photography and radio production.", date(2026, 12, 30)),
    ]
    for title, company, category, location, job_type, description, deadline in data:
        Opportunity.objects.create(title=title, company=company, category=category,
                                   location=location, job_type=job_type,
                                   description=description, deadline=deadline)

if not Training.objects.exists():
    courses = [
        ("Computer Skills", "Learn Microsoft Office, internet use and basic IT skills.", "4 weeks"),
        ("Web Development", "Build websites with HTML, CSS, JavaScript and Django.", "12 weeks"),
        ("Entrepreneurship", "Start and grow your own small business.", "6 weeks"),
        ("CV and Interview Skills", "Write a strong CV and perform well in interviews.", "2 weeks"),
        ("Digital Marketing", "Learn social media marketing, content and online sales.", "8 weeks"),
        ("Customer Service", "Communication and service skills for any workplace.", "3 weeks"),
    ]
    for title, description, duration in courses:
        Training.objects.create(title=title, description=description, duration=duration)

print("Sample data loaded.")