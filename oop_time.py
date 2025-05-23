from typing import Union, Tuple, overload
from functools import total_ordering
import math

@total_ordering
class Time:
    """A professional implementation of Time class with hour, minute, second precision.
    
    Features:
    - Type hints
    - Operator overloading (+, -, ==, <, etc.)
    - Immutability
    - Total ordering
    - String representation (__str__ and __repr__)
    - Input validation
    - Alternative constructors
    - Time arithmetic
    """
    
    __slots__ = ('_total_seconds',)  # Memory optimization
    
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        """Initialize Time with hours, minutes, seconds.
        
        Args:
            hours: Integer between 0-23
            minutes: Integer between 0-59
            seconds: Integer between 0-59
            
        Raises:
            ValueError: If any value is out of range
        """
        self._validate_range(hours, 0, 23, 'hours')
        self._validate_range(minutes, 0, 59, 'minutes')
        self._validate_range(seconds, 0, 59, 'seconds')
        self._total_seconds = hours * 3600 + minutes * 60 + seconds
    
    @staticmethod
    def _validate_range(value: int, min_val: int, max_val: int, name: str):
        """Validate if value is within range."""
        if not min_val <= value <= max_val:
            raise ValueError(f"{name} must be between {min_val}-{max_val}, got {value}")
    
    @property
    def hours(self) -> int:
        """Get hours component (0-23)."""
        return self._total_seconds // 3600
    
    @property
    def minutes(self) -> int:
        """Get minutes component (0-59)."""
        return (self._total_seconds % 3600) // 60
    
    @property
    def seconds(self) -> int:
        """Get seconds component (0-59)."""
        return self._total_seconds % 60
    
    @classmethod
    def from_seconds(cls, total_seconds: int) -> 'Time':
        """Create Time from total seconds.
        
        Args:
            total_seconds: Total seconds since midnight (0-86399)
            
        Returns:
            New Time instance
            
        Raises:
            ValueError: If total_seconds exceeds 24 hours
        """
        if not 0 <= total_seconds < 86400:
            raise ValueError("Total seconds must represent a valid 24-hour time (0-86399)")
        return cls(total_seconds // 3600, (total_seconds % 3600) // 60, total_seconds % 60)
    
    @classmethod
    def from_string(cls, time_str: str) -> 'Time':
        """Create Time from string (HH:MM:SS format).
        
        Args:
            time_str: String in HH:MM:SS format
            
        Returns:
            New Time instance
            
        Raises:
            ValueError: If format is invalid
        """
        try:
            hours, minutes, seconds = map(int, time_str.split(':'))
            return cls(hours, minutes, seconds)
        except (ValueError, AttributeError) as e:
            raise ValueError("Time string must be in HH:MM:SS format") from e
    
    def to_seconds(self) -> int:
        """Convert to total seconds since midnight."""
        return self._total_seconds
    
    def to_tuple(self) -> Tuple[int, int, int]:
        """Convert to (hours, minutes, seconds) tuple."""
        return (self.hours, self.minutes, self.seconds)
    
    def __add__(self, other: Union['Time', int]) -> 'Time':
        """Add two Time instances or seconds to Time.
        
        Args:
            other: Time instance or seconds to add
            
        Returns:
            New Time instance with added time
            
        Raises:
            TypeError: If other is not Time or int
            ValueError: If result exceeds 24 hours
        """
        if isinstance(other, Time):
            return self.from_seconds((self._total_seconds + other._total_seconds) % 86400)
        elif isinstance(other, int):
            return self.from_seconds((self._total_seconds + other) % 86400)
        else:
            raise TypeError(f"Unsupported operand type(s) for +: 'Time' and '{type(other).__name__}'")
    
    def __sub__(self, other: Union['Time', int]) -> 'Time':
        """Subtract two Time instances or seconds from Time.
        
        Args:
            other: Time instance or seconds to subtract
            
        Returns:
            New Time instance with subtracted time
            
        Raises:
            TypeError: If other is not Time or int
            ValueError: If result is negative
        """
        if isinstance(other, Time):
            return self.from_seconds((self._total_seconds - other._total_seconds) % 86400)
        elif isinstance(other, int):
            return self.from_seconds((self._total_seconds - other) % 86400)
        else:
            raise TypeError(f"Unsupported operand type(s) for -: 'Time' and '{type(other).__name__}'")
    
    def __eq__(self, other: object) -> bool:
        """Compare equality of two Time instances."""
        if not isinstance(other, Time):
            return NotImplemented
        return self._total_seconds == other._total_seconds
    
    def __lt__(self, other: 'Time') -> bool:
        """Compare if this Time is less than another."""
        if not isinstance(other, Time):
            return NotImplemented
        return self._total_seconds < other._total_seconds
    
    def __str__(self) -> str:
        """Return string representation (HH:MM:SS)."""
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"
    
    def __repr__(self) -> str:
        """Return official string representation."""
        return f"Time(hours={self.hours}, minutes={self.minutes}, seconds={self.seconds})"
    
    def __hash__(self) -> int:
        """Make Time hashable."""
        return hash(self._total_seconds)