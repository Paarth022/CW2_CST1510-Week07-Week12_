class Dataset:
    """Represents a data science dataset in the platform."""
    
    def __init__(self, dataset_id: int, name: str, size_bytes: int, 
                 rows: int, source: str):
        self.__id = dataset_id
        self.__name = name
        self.__size_bytes = size_bytes
        self.__rows = rows
        self.__source = source
    
    def get_id(self) -> int:
        """Get the dataset ID."""
        return self.__id
    
    def get_name(self) -> str:
        """Get the dataset name."""
        return self.__name
    
    def get_size_bytes(self) -> int:
        """Get the dataset size in bytes."""
        return self.__size_bytes
    
    def get_rows(self) -> int:
        """Get the number of rows in dataset."""
        return self.__rows
    
    def get_source(self) -> str:
        """Get the data source."""
        return self.__source
    
    def calculate_size_mb(self) -> float:
        """Calculate the size in megabytes.
        
        Returns:
            float: Size in MB (2 decimal places)
        """
        return self.__size_bytes / (1024 * 1024)
    
    def calculate_size_gb(self) -> float:
        """Calculate the size in gigabytes.
        
        Returns:
            float: Size in GB (2 decimal places)
        """
        return self.__size_bytes / (1024 * 1024 * 1024)
    
    def __str__(self) -> str:
        size_mb = self.calculate_size_mb()
        return (f"Dataset {self.__id}: {self.__name} "
                f"({size_mb:.2f} MB, {self.__rows} rows, source: {self.__source})")