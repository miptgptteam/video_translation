from dataclasses import dataclass


@dataclass
class Segment:
    start: float  # seconds
    end: float    # seconds
    text: str

    @property
    def duration(self) -> float:
        return self.end - self.start
