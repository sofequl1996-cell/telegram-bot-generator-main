import random
import string
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class AccountGenerator:
    """Generate demo student email accounts"""
    
    # বাংলাদেশের বিশ্ববিদ্যালয় ডেমো
    BANGLADESH_UNIVERSITIES = [
        {
            'name': 'BUET',
            'full_name': 'Bangladesh University of Engineering and Technology',
            'domain': 'buet.ac.bd',
            'email_format': lambda name: f'{name.lower()}@buet.ac.bd'
        },
        {
            'name': 'KUET',
            'full_name': 'Khulna University of Engineering & Technology',
            'domain': 'kuet.ac.bd',
            'email_format': lambda name: f'{name.lower()}.1803045@kuet.ac.bd'  # রোল ভিত্তিক
        },
        {
            'name': 'DU',
            'full_name': 'Dhaka University',
            'domain': 'du.ac.bd',
            'email_format': lambda name: f'{name.lower()}.std@du.ac.bd'
        },
        {
            'name': 'KU',
            'full_name': 'Khulna University',
            'domain': 'ku.ac.bd',
            'email_format': lambda name: f'{name.lower()}.220101@ku.ac.bd'
        },
        {
            'name': 'DUET',
            'full_name': 'Dhaka University of Engineering & Technology',
            'domain': 'duet.ac.bd',
            'email_format': lambda name: f'{name.lower()}.cmt@duet.ac.bd'  # ডিপার্টমেন্ট ভিত্তিক
        },
        {
            'name': 'SUST',
            'full_name': 'Shahjalal University of Science and Technology',
            'domain': 'sust.edu',
            'email_format': lambda name: f'{name.lower()}.stud@sust.edu'
        },
        {
            'name': 'RU',
            'full_name': 'Rajshahi University',
            'domain': 'ru.ac.bd',
            'email_format': lambda name: f'{name.lower()}.1234@ru.ac.bd'
        },
        {
            'name': 'IUT',
            'full_name': 'Islamic University of Technology',
            'domain': 'iut-dhaka.edu',
            'email_format': lambda name: f'{name.lower()}@iut-dhaka.edu'
        },
        {
            'name': 'NSU',
            'full_name': 'North South University',
            'domain': 'nsu.edu',
            'email_format': lambda name: f'{name.lower()}.student@nsu.edu'
        },
        {
            'name': 'BRACU',
            'full_name': 'BRAC University',
            'domain': 'bracu.ac.bd',
            'email_format': lambda name: f'{name.lower()}.cse@bracu.ac.bd'
        },
    ]
    
    # আমেরিকার বিশ্ববিদ্যালয় ডেমো
    USA_UNIVERSITIES = [
        {
            'name': 'Harvard',
            'full_name': 'Harvard University',
            'domain': 'harvard.edu',
            'email_format': lambda name: f'{name.lower()}@harvard.edu'
        },
        {
            'name': 'Stanford',
            'full_name': 'Stanford University',
            'domain': 'stanford.edu',
            'email_format': lambda name: f'{name.lower()}.std@stanford.edu'
        },
        {
            'name': 'MIT',
            'full_name': 'Massachusetts Institute of Technology',
            'domain': 'mit.edu',
            'email_format': lambda name: f'{name.lower()}123@mit.edu'
        },
        {
            'name': 'Berkeley',
            'full_name': 'UC Berkeley',
            'domain': 'berkeley.edu',
            'email_format': lambda name: f'r.{name.lower()}@berkeley.edu'
        },
        {
            'name': 'Columbia',
            'full_name': 'Columbia University',
            'domain': 'columbia.edu',
            'email_format': lambda name: f'{name.lower()}.student@columbia.edu'
        },
        {
            'name': 'NYU',
            'full_name': 'New York University',
            'domain': 'nyu.edu',
            'email_format': lambda name: f'{name.lower()}_std@nyu.edu'
        },
        {
            'name': 'UCLA',
            'full_name': 'UCLA',
            'domain': 'ucla.edu',
            'email_format': lambda name: f'{name.lower()}@ucla.edu'
        },
        {
            'name': 'Yale',
            'full_name': 'Yale University',
            'domain': 'yale.edu',
            'email_format': lambda name: f'{name.lower()}.26@yale.edu'
        },
        {
            'name': 'Princeton',
            'full_name': 'Princeton University',
            'domain': 'princeton.edu',
            'email_format': lambda name: f'{name.lower()}.stud@princeton.edu'
        },
        {
            'name': 'Cornell',
            'full_name': 'Cornell University',
            'domain': 'cornell.edu',
            'email_format': lambda name: f'{name.lower()}@cornell.edu'
        },
    ]
    
    @staticmethod
    def generate_demo_emails() -> Dict[str, List[Dict]]:
        """Generate demo emails for testing"""
        demo_data = {
            'BD': [],
            'US': []
        }
        
        # বাংলাদেশের ডেমো ইমেইল
        for uni in AccountGenerator.BANGLADESH_UNIVERSITIES:
            email = uni['email_format']('rahim')
            demo_data['BD'].append({
                'email': email,
                'university': uni['name'],
                'university_full': uni['full_name'],
                'domain': uni['domain'],
                'country': 'Bangladesh 🇧🇩'
            })
        
        # আমেরিকার ডেমো ইমেইল
        for uni in AccountGenerator.USA_UNIVERSITIES:
            email = uni['email_format']('rahim')
            demo_data['US'].append({
                'email': email,
                'university': uni['name'],
                'university_full': uni['full_name'],
                'domain': uni['domain'],
                'country': 'USA 🇺🇸'
            })
        
        return demo_data
    
    @staticmethod
    def generate_password(length: int = 12) -> str:
        """Generate a random password"""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))
    
    @staticmethod
    def get_demo_data_table() -> str:
        """Get formatted demo data table"""
        demo_emails = AccountGenerator.generate_demo_emails()
        
        table = "\n📧 **DEMO STUDENT EMAILS** 📧\n\n"
        
        table += "🇧🇩 **BANGLADESH - ১০টি বিশ্ববিদ্যালয়**\n"
        table += "="*50 + "\n"
        for i, email_data in enumerate(demo_emails['BD'], 1):
            table += f"{i}. {email_data['email']}\n"
            table += f"   ({email_data['university_full']})\n\n"
        
        table += "\n🇺🇸 **USA - ১০টি বিশ্ববিদ্যালয়**\n"
        table += "="*50 + "\n"
        for i, email_data in enumerate(demo_emails['US'], 1):
            table += f"{i}. {email_data['email']}\n"
            table += f"   ({email_data['university_full']})\n\n"
        
        return table
