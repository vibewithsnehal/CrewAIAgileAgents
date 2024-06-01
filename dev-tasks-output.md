```python
from flask import Flask, request, redirect, url_for, render_template, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# In-memory storage for user stories
user_stories = {}

@app.route('/')
def index():
    return render_template('index.html', user_stories=user_stories)

@app.route('/add', methods=['POST'])
def add_user_story():
    title = request.form['title']
    description = request.form['description']
    
    if title and description:
        story_id = len(user_stories) + 1
        user_stories[story_id] = {'title': title, 'description': description}
        flash('User story added successfully!')
    else:
        flash('Title and Description are required!')

    return redirect(url_for('index'))

@app.route('/edit/<int:story_id>', methods=['GET', 'POST'])
def edit_user_story(story_id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        if title and description:
            user_stories[story_id] = {'title': title, 'description': description}
            flash('User story updated successfully!')
            return redirect(url_for('index'))
        else:
            flash('Title and Description are required!')
    
    return render_template('edit.html', story_id=story_id, user_story=user_stories[story_id])

@app.route('/delete/<int:story_id>', methods=['POST'])
def delete_user_story(story_id):
    if story_id in user_stories:
        del user_stories[story_id]
        flash('User story deleted successfully!')
    else:
        flash('User story not found!')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
```

#### `templates/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Planning Poker App</title>
</head>
<body>
    <h1>Planning Poker App</h1>
    
    <form action="{{ url_for('add_user_story') }}" method="post">
        <h2>Add User Story</h2>
        <label for="title">Title:</label><br>
        <input type="text" id="title" name="title"><br><br>
        <label for="description">Description:</label><br>
        <textarea id="description" name="description"></textarea><br><br>
        <input type="submit" value="Add">
    </form>
    
    <h2>User Stories</h2>
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <ul>
                {% for message in messages %}
                    <li>{{ message }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}
    
    <ul>
        {% for story_id, story in user_stories.items() %}
            <li>
                <strong>{{ story.title }}</strong>: {{ story.description }}
                <a href="{{ url_for('edit_user_story', story_id=story_id) }}">Edit</a>
                <form action="{{ url_for('delete_user_story', story_id=story_id) }}" method="post" style="display:inline;">
                    <input type="submit" value="Delete">
                </form>
            </li>
        {% endfor %}
    </ul>
</body>
</html>
```

#### `templates/edit.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Edit User Story</title>
</head>
<body>
    <h1>Edit User Story</h1>
    
    <form action="{{ url_for('edit_user_story', story_id=story_id) }}" method="post">
        <label for="title">Title:</label><br>
        <input type="text" id="title" name="title" value="{{ user_story.title }}"><br><br>
        <label for="description">Description:</label><br>
        <textarea id="description" name="description">{{ user_story.description }}</textarea><br><br>
        <input type="submit" value="Update">
    </form>
    
    <a href="{{ url_for('index') }}">Back to User Stories</a>
</body>
</html>
```

#### `test_app.py`

```python
import unittest
from app import app, user_stories

class PlanningPokerAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_user_story(self):
        response = self.app.post('/add', data=dict(title='Test Story', description='This is a test story'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('Test Story', [story['title'] for story in user_stories.values()])

    def test_edit_user_story(self):
        self.app.post('/add', data=dict(title='Test Story', description='This is a test story'))
        story_id = next(iter(user_stories))
        response = self.app.post(f'/edit/{story_id}', data=dict(title='Updated Story', description='Updated description'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user_stories[story_id]['title'], 'Updated Story')

    def test_delete_user_story(self):
        self.app.post('/add', data=dict(title='Test Story', description='This is a test story'))
        story_id = next(iter(user_stories))
        response = self.app.post(f'/delete/{story_id}')
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(story_id, user_stories)

if __name__ == '__main__':
    unittest.main()
```

This is the complete content for implementing the "User Story Input" feature with unit tests and documentation.