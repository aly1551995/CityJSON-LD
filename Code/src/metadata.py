import json
from typing import Union, List
from geographicalExtent import GeographicalExtent
from pointOfContact import PointOfContact


class Metadata:

    def __init__(self, geographical_extent=None, identifier=None, point_of_contact=None,
                 reference_date=None, reference_system=None, title=None):
        self.geographical_extent = self.to_geographical_extent(
            geographical_extent)
        self.identifier = identifier
        self.point_of_contact = self.to_point_of_contact(point_of_contact)
        self.reference_date = reference_date
        self.reference_system = reference_system
        self.title = title

    def to_geographical_extent(self, geographical_extent):
        if isinstance(geographical_extent, list):
            if len(geographical_extent) == 6:
                min_x, min_y, min_z, max_x, max_y, max_z = geographical_extent
                return GeographicalExtent(min_x, min_y, min_z, max_x, max_y, max_z)
            else:
                print("Geographical Extent should be a list of 6 floats")
        elif not geographical_extent:
            return geographical_extent
        else:
            print("Geographical Extent should be either a GeographicalExtent object or a list of 6 floats or None")

    def to_point_of_contact(self, point_of_contact):
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
        elif not point_of_contact:
            return None
        else:
            print("Point of contact should be a dictionary or None")

    def to_json(self):
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
        filtered_data = {key: value for key,
                         value in data.items() if value is not None}
        return json.dumps(filtered_data, ensure_ascii=False)
