import json
from typing import List, Optional, Dict, Any, Union
from Metadata.geographicalExtent import GeographicalExtent
from Metadata.pointOfContact import PointOfContact

class Metadata:
    def __init__(self, geographical_extent: Optional[Union[List[float], GeographicalExtent]] = None, identifier: Optional[str] = None, point_of_contact: Optional[Dict[str, Any]] = None,
                 reference_date: Optional[str] = None, reference_system: Optional[str] = None, title: Optional[str] = None):
        """
        Initialize the Metadata object with the given parameters.

        :param geographical_extent: GeographicalExtent object or list of 6 floats or None.
        :param identifier: Identifier for the metadata.
        :param point_of_contact: Dictionary representing the point of contact or None.
        :param reference_date: Reference date for the metadata.
        :param reference_system: Reference system for the metadata.
        :param title: Title of the metadata.
        """
        self.geographical_extent = GeographicalExtent.to_geographical_extent(geographical_extent)
        self.identifier = identifier
        self.point_of_contact = self.to_point_of_contact(point_of_contact)
        self.reference_date = reference_date
        self.reference_system = reference_system
        self.title = title

    @staticmethod
    def to_point_of_contact(point_of_contact: Optional[Dict[str, Any]]) -> Optional[PointOfContact]:
        """
        Convert a dictionary to a PointOfContact object.

        :param point_of_contact: Dictionary representing the point of contact or None.
        :return: PointOfContact object or None.
        """
        if isinstance(point_of_contact, dict):
            contact_name = point_of_contact.get('contactName')
            email_address = point_of_contact.get('emailAddress')
            role = point_of_contact.get('role')
            website = point_of_contact.get('website')
            contact_type = point_of_contact.get('contactType')
            has_address = point_of_contact.get('address')
            phone = point_of_contact.get('phone')
            organization = point_of_contact.get('organization')
            return PointOfContact(contact_name, email_address, role, website, contact_type, has_address, phone, organization)
        elif point_of_contact is None:
            return None
        else:
            raise TypeError("Point of contact should be a dictionary or None")

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the Metadata object to a JSON-LD representation.

        :return: JSON-LD representation of the Metadata object.
        """
        geographical_extent_dict = json.loads(self.geographical_extent.to_json()) if self.geographical_extent else None
        point_of_contact_dict = json.loads(self.point_of_contact.to_json()) if self.point_of_contact else None
        data = {
            "@type": "cj:Metadata",
            "cj:hasGeographicalExtent": geographical_extent_dict,
            "cj:identifier": self.identifier,
            "cj:hasPointOfContact": point_of_contact_dict,
            "cj:referenceDate": self.reference_date,
            "cj:referenceSystem": self.reference_system,
            "cj:title": self.title
        }

        # Filter out None values
        filtered_data = {key: value for key, value in data.items() if value is not None}

        return filtered_data
