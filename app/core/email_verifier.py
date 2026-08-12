import re

# List of common disposable, temporary, or fake email domains
DISPOSABLE_DOMAINS = {
    "mailinator.com", "tempmail.com", "10minutemail.com", "trashmail.com",
    "dispostable.com", "guerrillamail.com", "fake.com", "test.com", "example.com",
    "yopmail.com", "sharklasers.com", "getairmail.com", "throwawaymail.com",
    "maildrop.cc", "temp-mail.org", "fakemail.net"
}

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

def validate_email_address(email: str) -> tuple[bool, str]:
    """
    Validates if an email address is properly formatted and from a real, non-disposable domain.
    Returns (is_valid, reason).
    """
    if not email or not isinstance(email, str):
        return False, "Email address is required."
        
    email_clean = email.strip().lower()
    
    if not EMAIL_REGEX.match(email_clean):
        return False, "Invalid email format. Please provide a valid email address (e.g., user@domain.com)."
        
    domain = email_clean.split("@")[-1]
    
    if domain in DISPOSABLE_DOMAINS:
        return False, f"The email domain '@{domain}' is a known temporary/disposable email service. Please use a real email address."
        
    tld = domain.split(".")[-1]
    if len(tld) < 2 or not tld.isalpha():
        return False, f"Invalid domain extension '.{tld}'. Please enter a valid email address."
        
    return True, "Valid real email address."
