from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict



class Event(BaseModel):
    index: int = Field(
        description="The index of the event, starting from 0",
    )

    is_last: bool = Field(
        description="Indicates if this is the last event in the sequence"
    )

    description: str = Field(
        description="A concise description of the event, capturing its essence in one sentence",
        examples=[
            "A thief who stole a gem from a museum was caught after a rooftop chase with guards, and the gem was recovered.",
        ]
    )

    process_chain: List[str] = Field(
        description="A list of steps or actions that make up the event's process chain, which constitutes a complete causal chain.",
        examples=[
            [
                "A thief steals a gem from a museum, triggering the alarm. Guards notice and begin the chase.",
                "The thief rushes out the museum's back door and dashes through narrow alleys, with guards closely pursuing and calling for backup.",
                "The thief climbs a fire escape to the rooftops; the guards follow using low platforms on adjacent buildings.",
                "The thief leaps across a 1.5-meter gap between two buildings. The guards hesitate but take the risky jump, nearly losing their footing.",
                "The thief knocks over stacked wooden planks to create an obstacle. The guards dodge but lose speed.",
                "The thief attempts to slide down a rope to the opposite rooftop, but a guard lunges and grabs their ankle. Both tumble and grapple.",
                "Backup arrives, subduing the thief and recovering the gem.",
            ],
        ]
    )

    def __str__(self):
        s = f"<Event {self.index}>"
        s += f"\nDescription: {self.description}"
        s += f"\nProcess Chain:"
        for process in self.process_chain:
            s += f"\n- {process}"
        return s