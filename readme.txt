Steps to run backend:
1. Make sure you are in the main folder, not in the backend folder
2. Install requirements (preferably in a virtual environment) using "python -m pip install -r requirements.txt"
3. Update config file in instance directory with path.
4. Run "flask --app Backend run --debug"
5. Navigate to 127.0.0.1:5000/ to run the app.
6. Registration page redirects to login, login redirects to home. Home shows all posts, has links to view each post, and has link to user profile and search bar. View post has edit and delete options, profile has options to CRUD education details.
