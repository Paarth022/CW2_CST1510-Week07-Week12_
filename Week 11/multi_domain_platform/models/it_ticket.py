class ITTicket:
    """Represents an IT support ticket."""
    
    def __init__(self, ticket_id: int, title: str, priority: str, 
                 status: str, assigned_to: str = "Unassigned"):
        self.__id = ticket_id
        self.__title = title
        self.__priority = priority
        self.__status = status
        self.__assigned_to = assigned_to
    
    def get_id(self) -> int:
        """Get the ticket ID."""
        return self.__id
    
    def get_title(self) -> str:
        """Get the ticket title."""
        return self.__title
    
    def get_priority(self) -> str:
        """Get the priority level."""
        return self.__priority
    
    def get_status(self) -> str:
        """Get the current status."""
        return self.__status
    
    def get_assigned_to(self) -> str:
        """Get who the ticket is assigned to."""
        return self.__assigned_to
    
    def assign_to(self, staff: str) -> None:
        """Assign ticket to a staff member.
        
        Args:
            staff: Name or ID of the staff member
        """
        self.__assigned_to = staff
    
    def close_ticket(self) -> None:
        """Close/resolve the ticket."""
        self.__status = "Closed"
    
    def reopen_ticket(self) -> None:
        """Reopen a closed ticket."""
        if self.__status == "Closed":
            self.__status = "Open"
    
    def update_status(self, new_status: str) -> None:
        """Update the ticket status.
        
        Args:
            new_status: New status (e.g., 'Open', 'In Progress', 'Closed')
        """
        self.__status = new_status
    
    def __str__(self) -> str:
        return (f"Ticket {self.__id}: {self.__title} "
                f"[{self.__priority}] – {self.__status} "
                f"(assigned to: {self.__assigned_to})")