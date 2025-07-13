```python
class SprintAnalysis:
    def __init__(self, sprint_data):
        """
        Initialize with historical sprint data.
        :param sprint_data: List of dictionaries with keys 'sprint_number', 'completed_story_points'
        """
        self.sprint_data = sprint_data

    def calculate_velocity(self):
        """
        Calculate the average velocity from past sprints.
        :return: Average velocity as float
        """
        total_story_points = sum([sprint['completed_story_points'] for sprint in self.sprint_data])
        number_of_sprints = len(self.sprint_data)
        return total_story_points / number_of_sprints if number_of_sprints > 0 else 0

    def suggest_capacity(self, team_availability):
        """
        Suggest optimal team capacity for the next sprint based on historical velocity and team availability.
        :param team_availability: A float representing percentage of team availability (0 to 1)
        :return: Suggested capacity in story points
        """
        average_velocity = self.calculate_velocity()
        return average_velocity * team_availability

    def recommend_user_stories(self, backlog, team_capacity):
        """
        Recommend user stories for the next sprint based on priority and team capacity.
        :param backlog: List of dictionaries with keys 'story_id', 'priority', 'story_points'
        :param team_capacity: Capacity in story points
        :return: List of recommended story IDs
        """
        backlog.sort(key=lambda x: x['priority'], reverse=True)
        selected_stories = []
        current_capacity = 0

        for story in backlog:
            if current_capacity + story['story_points'] <= team_capacity:
                selected_stories.append(story['story_id'])
                current_capacity += story['story_points']

        return selected_stories


# Unit Tests
import unittest

class TestSprintAnalysis(unittest.TestCase):
    def setUp(self):
        self.sprint_data = [
            {'sprint_number': 1, 'completed_story_points': 20},
            {'sprint_number': 2, 'completed_story_points': 25},
            {'sprint_number': 3, 'completed_story_points': 30}
        ]
        self.analysis = SprintAnalysis(self.sprint_data)

    def test_calculate_velocity(self):
        self.assertEqual(self.analysis.calculate_velocity(), 25.0)

    def test_suggest_capacity(self):
        self.assertEqual(self.analysis.suggest_capacity(0.8), 20.0)

    def test_recommend_user_stories(self):
        backlog = [
            {'story_id': 1, 'priority': 3, 'story_points': 8},
            {'story_id': 2, 'priority': 5, 'story_points': 13},
            {'story_id': 3, 'priority': 1, 'story_points': 5}
        ]
        self.assertEqual(self.analysis.recommend_user_stories(backlog, 20), [2, 1])

if __name__ == '__main__':
    unittest.main()

```

### Documentation:

- **SprintAnalysis Class**: Analyzes historical sprint data to provide insights on team velocity and capacity.
  - **calculate_velocity()**: Calculates average sprint velocity.
  - **suggest_capacity(team_availability)**: Suggests optimal capacity based on historical velocity and team availability.
  - **recommend_user_stories(backlog, team_capacity)**: Recommends user stories for the next sprint based on priority and capacity.

- **Unit Tests**: Provided for each method to ensure accurate functionality.

This implementation meets the acceptance criteria by providing a summary of past sprint velocities, suggesting optimal team capacity, and recommending user stories for inclusion based on priority and team capacity.