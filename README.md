# Real-time Chat Application with Django Channels

This project is a real-time chat application built using Django, Django Channels, and WebSocket. It allows users to send and receive messages instantly, supporting database storage and retrieval for persistent messaging.

---

## Features

- **Real-time Messaging**: Instantaneous delivery and receipt of messages.
- **Database Integration**: Persistent message storage in the database.
- **User Authentication**: Secure login and user-specific chat rooms.
- **Previous Messages Loading**: Retrieve chat history for context.
- **Scalable Architecture**: Supports WebSocket with Django Channels for asynchronous communication.

---

## Requirements

Before running the project, ensure you have the following installed:

- Python 3.8+
- Django 4.2+
- Django Channels 4.0+
- Redis (for production WebSocket handling)
- PostgreSQL (or your preferred database backend)

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/real-time-chat.git
   cd real-time-chat
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**:
   Update the `DATABASES` setting in `settings.py` with your database credentials.

5. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start Redis (for production)**:
   ```bash
   redis-server
   ```

7. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

---

## Usage

1. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:8000/`.

2. **User Authentication**:
   Register or log in to access the chat functionality.

3. **Start Chatting**:
   Select a user to start chatting in real-time.

---

## Project Structure

```
real-time-chat/
├── chat/                  # Chat application logic
│   ├── consumers.py       # WebSocket consumers for real-time messaging
│   ├── models.py          # Database models for messages
│   ├── routing.py         # WebSocket routing configuration
│   └── views.py           # Django views (if applicable)
├── templates/             # HTML templates for the frontend
├── static/                # Static files (CSS, JavaScript)
├── manage.py              # Django project management script
└── requirements.txt       # Python dependencies
```

---

## Key Files

- **`chat/consumers.py`**: Manages WebSocket connections and real-time message handling.
- **`chat/models.py`**: Defines the `Message` model for database storage.
- **`settings.py`**: Contains project settings, including database and channel layers.

---

## Troubleshooting

### Common Issues

1. **Messages Not Saving**:
   - Ensure the database is configured correctly and migrations are applied.
   - Check the `save_message` function for any exceptions or errors.

2. **WebSocket Not Connecting**:
   - Verify your channel layer configuration.
   - Use Redis for production and update the `CHANNEL_LAYERS` in `settings.py`.

3. **Debugging**:
   Enable debug-level logs in `settings.py`:
   ```python
   LOGGING = {
       'version': 1,
       'handlers': {
           'console': {
               'class': 'logging.StreamHandler',
           },
       },
       'loggers': {
           'django': {
               'level': 'DEBUG',
               'handlers': ['console'],
           },
       },
   }
   ```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch.
4. Create a pull request to the main repository.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

If you have any questions or issues, feel free to reach out:

- **Author**: [vinayvasantham](https://github.com/vinayvasantham)
- **Email**: vinayvasantham7@gmail.com
