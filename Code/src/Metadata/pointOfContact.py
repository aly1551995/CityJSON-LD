import json
from typing import Optional

class PointOfContact:
    def __init__(self, contact_name: str, email_address: str, role: Optional[str] = None, website: Optional[str] = None,
                 contact_type: Optional[str] = None, address: Optional[str] = None, phone: Optional[str] = None, organization: Optional[str] = None):
        """
        Initialize the PointOfContact object with the given parameters.

        :param contact_name: Name of the contact person.
        :param email_address: Email address of the contact person.
        :param role: Role of the contact person, optional.
        :param website: Website of the contact person, optional.
        :param contact_type: Type of contact, optional.
        :param address: Address of the contact person, optional.
        :param phone: Phone number of the contact person, optional.
        :param organization: Organization of the contact person, optional.
        """
        self.contact_name = contact_name
        self.email_address = email_address
        self.role = role
        self.website = website
        self.contact_type = contact_type
        self.address = address
        self.phone = phone
        self.organization = organization

    def to_json(self) -> str:
        """
        Convert the PointOfContact object to a JSON-LD representation.

        :return: JSON-LD representation of the PointOfContact object.
        """
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
        # Filter out None values
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return json.dumps(filtered_data, ensure_ascii=False)
