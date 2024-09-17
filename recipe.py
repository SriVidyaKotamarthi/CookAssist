from dataclasses import dataclass
import decimal


@dataclass
class Recipe:
    short_name: str
    ingredients_list: list
    preparation_time: decimal
    preparation_time_unit: str
    cook_time: decimal
    cook_time_unit: str
    total_time: decimal
    calories: str
    cuisine: str
    course: str
    diet: list
    difficulty: str
    rating: decimal
    URL: str
    
    def __init__(self) -> None:
        self.short_name = None
        self.ingredients_list = None
        self.preparation_time = None
        self.preparation_time_unit = None
        self.cook_time = None
        self.cook_time_unit = None
        self.total_time = None
        self.calories = None
        self.cuisine = None
        self.course = None
        self.diet = None
        self.difficulty = None
        self.rating = None
        self.URL = None