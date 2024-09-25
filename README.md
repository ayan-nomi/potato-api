**System Overview and How to Use It**

**1. Clone the Repository**

To begin using the system, first clone the repository from GitHub onto your local machine:

    git clone https://github.com/your-username/potato-api.git #replace your-username with github username
    cd potato-api


**2. Install Docker**

You need to have Docker and Docker Compose installed on your system. 

- Install Docker: You can follow the official Docker installation instructions.

- Install Docker Compose: Install Docker Compose, which allows you to manage multi-container applications.


**3. Start the System**

To start the system, navigate to the project directory and run the following command:

    docker-compose up --build

This command will:

- **Build and run MongoDB:** MongoDB is the database where your data (in this case, Twitter-like data) will be stored.
- **Run the Flask API:** This is the web server that exposes the functionality to query the data. The Flask app interacts with MongoDB, processes requests, and sends responses.

**4. Data Insertion**

The system automatically reads data from a file (e.g., correct_twitter_201904.tsv) in the ```flask_app/data/``` folder and inserts it into MongoDB on startup. The data includes fields like tweet text, author_id, timestamp (ts1 and ts2), like_count, and more.

The ```data_sync.py``` script is responsible for reading the data using pandas, converting date fields to proper datetime format, and then inserting it into the MongoDB collection.

**5. API Query**

Once the system is running, you can query it using API requests.

Example Query Using curl:

    curl -X POST http://localhost:5000/query -H "Content-Type: application/json" -d '{"term": "music"}'
    
This will query the database for tweets containing the term "music" and return the following information:

- Total number of tweets containing the term.
- Number of unique users who posted tweets containing the term.
- The average number of likes for those tweets.
- The place IDs where the tweets originated.
- Times of day tweets were posted.
- The user who posted the most tweets containing the term.

This allows for flexible querying of tweet data based on terms, users, locations, or times.

**Design Choices and Justification**


**1. Containerization Using Docker**

**-** Docker ensures that the environment remains consistent regardless of the user's system (Windows, Mac, Linux). Users don't need to manually install MongoDB, Flask, or any other Python libraries – Docker handles everything.

**-** This approach simplifies onboarding. All users need to do is install Docker and run the provided docker-compose command. There's no need for manual setup or dependency resolution.

**2. Automated Data Insertion**

**-** The ```data_sync.py``` script automates the process of inserting data into MongoDB. When the system starts up, it reads the data file (TSV format), processes it (e.g., converts timestamps to datetime), and inserts it into the MongoDB database.

**-** This approach ensures that the system is ready to use as soon as it’s up and running. Users don’t have to worry about manually inserting data. It also ensures the data is consistently processed and transformed (e.g., datetime conversion) before being inserted.

**3. Data Querying via API**

**-** The system exposes a REST API that allows users to query data stored in MongoDB. This makes the system accessible not only via curl commands but also from external applications or front-end interfaces if needed.

**-** An API provides a flexible interface for querying data. It decouples the front-end from the back-end, allowing the back-end logic to be reused across different interfaces (e.g., command-line, web, or mobile).


**Conclusion**

With these steps, you can easily set up the system on your own computer. The use of Docker ensures consistency, Flask provides a lightweight but powerful API, and MongoDB offers a flexible and scalable database solution. The system is designed for ease of use and flexibility in querying, making it a robust solution for managing and analyzing Twitter-like datasets.
