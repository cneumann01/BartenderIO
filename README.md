# BartenderIO
BartenderIO is my first independent coding project, showcasing the culmination of my knowledge and skills at the halfway point of the Springboard coding bootcamp. Developed entirely without assistance from the school, the project solely features my own creativity and knowledge.

As a Flask/PostgreSQL driven web application, BartenderIO offers users a straightforward and user-friendly interface that interacts with the CocktailDB API. Users can freely explore an extensive library of drinks, create a personalized account to save their favorites, craft custom drink lists, and even discover inspiration with the random drink feature. Each drink features a beautiful photo sourced from the CocktailDB API, and is accompanied by easy-to-follow instructions and ingredient lists.

Both the web application and PostgreSQL database are currently hosted on Render.com using the free Student/Hobbyist plans. You can access the website here: [BartenderIO](https://bartenderio.onrender.com/). Please note that, due to the limitations of the free hosting plan, the initial site loading may take up to 90 seconds. This delay is beyond my control, but you can find more information about it here: [Render.com Documentation](https://render.com/docs/free).

Additionally, BartenderIO is available as a standalone Flask application. Please find the installation instructions below. Furthermore, a docker container is in development and will be released soon.


## Table of Contents
- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features
- Browse and search for drinks based on name, category, and alcoholic or non-alcoholic beverages.
- View detailed information about a specific drink, including its name, ingredients, and preparation instructions.
- Favorite drinks to keep track of your preferred beverages.
- Create custom collections of drinks and add your favorite drinks to them.
- Secure user authentication and password hashing.
- Share your collections with others and explore collections created by fellow users. (Coming soon)
- An easy to deploy docker container for local use cases. (Coming soon)


## Technologies
BartenderIO is built on the Flask web framework, utilizing several other technologies and libraries, including:
- Flask-Bcrypt: For password hashing and verification.
- Flask-SQLAlchemy: For interacting with the database and managing models.
- PostgreSQL: As the database management system to store user and drink data.
- JavaScript, HTML, and CSS: For the frontend design and interactivity.
- TheCocktailDB API: To fetch and display drink data.
- Render.com: For hosting of the Flask/PostgreSQL servers.

## Getting Started
To run BartenderIO locally on your machine, follow the installation and usage instructions below.

### Installation
1. Clone the repository from GitHub:
```
git clone https://github.com/yourusername/BartenderIO.git
```

2. Create a virtual environment and activate it (optional but recommended):
```
cd BartenderIO
python -m venv venv
source venv/bin/activate   # On Windows, use "venv\Scripts\activate"
```

3. Install the required dependencies:
```
pip install -r requirements.txt
```

4. Set up the PostgreSQL database and configure the environment variable for the database URL:
- Create a PostgreSQL database and note down the database URL, including username, password, host, and database name.
- Export the database URL as an environment variable:
```
export DATABASE_URL=postgresql:///your_database_name
```

### Usage
1. Run the application:
```
flask run
```

2. Visit `http://localhost:5000/` in your web browser to access the BartenderIO application.

## Contributing
Contributions to BartenderIO are welcome! If you find any bugs or have suggestions for improvements, feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch for your changes:
```
git checkout -b feature/your-feature-name
```
3. Make your changes and commit them with descriptive commit messages.
4. Push your branch to your forked repository.
5. Open a pull request on the main repository's `main` branch.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

