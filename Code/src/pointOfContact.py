import json


class PointOfContact:

    def __init__(self, contact_name: str, email_address: str, role=None, website=None,
                 contact_type=None, address=None, phone=None, organization=None):
        self.contact_name = contact_name
        self.email_address = email_address
        self.role = role
        self.website = website
        self.contact_type = contact_type
        self.address = address
        self.phone = phone
        self.organization = organization

    def to_json(self):
        data = {
            "@type": "cj:PointOfContact",
            "cj:contactName": self.contact_name,
            "cj:emailAddress": self.email_address,
            "cj:role": self.role,
            "cj:website": self.website,
            "cj:contactType": self.contact_type,
            "cj:phone": self.phone,
            "cj:hasAddress": self.address,
            "cj:organization": self.organization,
        }
        # Filter out None values and use provided keys
        filtered_data = {key: value for key,
                         value in data.items() if value is not None}
        return json.dumps(filtered_data, ensure_ascii=False)
