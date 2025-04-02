![image](https://github.com/user-attachments/assets/86d12a39-bd56-4f05-bafc-501400845919)

Here’s a summary of the steps taken to build the Flask-based device monitoring and ping dashboard application:
1. Set up Flask App:
•	Created a Flask app instance using Flask(__name__).

3. Defined Devices to Monitor:
•	A dictionary called devices was created to store device names and their associated IP addresses.

5. Set Up SQLite Database:
•	A SQLite database (ping_data.db) was initialized with a table named devices to store ping results (device name, IP address, status, and timestamp).
•	The init_db() function checks if the devices table exists and creates it if necessary.

7. Ping Function:
•	Defined the ping_device() function to send a ping to each device's IP address using the os.system() command.
•	The function checks the platform (Windows or Linux/macOS) and uses the appropriate ping command (ping -n 1 for Windows, ping -c 1 for Linux/macOS).
•	Based on the ping response, the function determines if the device is "Online" or "Offline".
•	The result (along with a timestamp) is then stored in the SQLite database.

9. Fetch Ping History:
•	The get_ping_history() function retrieves the most recent ping results from the database, ordered by timestamp.

11. Flask Routes:
•	Dashboard Route (/): Displays a dashboard with the ping history pulled from the database and lists all the devices to monitor.
•	Ping Route (/ping): Triggers a ping to each device in the devices dictionary, returns their status (Online/Offline) as a JSON response.

13. Running the Flask App:
•	The app is run on host='0.0.0.0' and port 5000, making it accessible from the local network.

Key Components:
•	Flask: Used to create web routes and serve the dashboard.
•	SQLite: Used to store and retrieve ping data.
•	OS and Platform: Used to run system-specific ping commands.
•	Jinja Templates: Used to render HTML on the dashboard.
Result:
•	The app runs a Flask server, pings devices to check their status, stores the results in a database, and shows a dashboard with real-time device statuses and ping history.
Let me know if you'd like to dive deeper into any part of the project!
