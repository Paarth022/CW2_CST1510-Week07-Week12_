class SecurityIncident:
    """Represents a cybersecurity incident in the platform."""
    
    def __init__(self, incident_id: int, incident_type: str, severity: str, 
                 status: str, description: str):
        self.__id = incident_id
        self.__incident_type = incident_type
        self.__severity = severity
        self.__status = status
        self.__description = description
    
    def get_id(self) -> int:
        """Get the incident ID."""
        return self.__id
    
    def get_incident_type(self) -> str:
        """Get the incident type."""
        return self.__incident_type
    
    def get_severity(self) -> str:
        """Get the severity level."""
        return self.__severity
    
    def get_status(self) -> str:
        """Get the current status."""
        return self.__status
    
    def get_description(self) -> str:
        """Get the incident description."""
        return self.__description
    
    def update_status(self, new_status: str) -> None:
        """Update the incident status."""
        self.__status = new_status
    
    def get_severity_level(self) -> int:
        """Return an integer severity level.
        
        Returns:
            int: 1=low, 2=medium, 3=high, 4=critical, 0=unknown
        """
        mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
        }
        return mapping.get(self.__severity.lower(), 0)
    
    def __str__(self) -> str:
        return (f"Incident {self.__id} [{self.__severity.upper()}] "
                f"{self.__incident_type} - Status: {self.__status}")