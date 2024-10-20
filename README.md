# Summarize Article

## Description
Summarize Article is a web application that allows users to input a URL of an article and receive a summarized version of the content. The application uses OpenAI's GPT model for summarization and falls back to the Sumy library for summarization in case of API rate limits or errors.

## Features
- Summarize articles from any URL.
- Uses OpenAI's GPT model for high-quality summarization.
- Falls back to Sumy library for summarization when OpenAI API is unavailable.
- Simple and intuitive web interface.

## Visuals
![Screenshot of the application](static/screenshot.png)

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Steps
1. Clone the repository:
    ```bash
    git clone https://git.savvycom.vn/minh.nguyen/summarize-article.git
    cd summarize-article
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the root directory of the project.
    - Add your OpenAI API key to the `.env` file:
        ```
        OPENAI_API_KEY=your_openai_api_key
        ```

5. Run the application:
    ```bash
    uvicorn main:app --reload
    ```

6. Open your browser and navigate to `http://localhost:8000` to use the application.

## Usage
1. Enter the URL of the article you want to summarize in the input field.
2. Click the "Summarize" button.
3. Wait for the summary to be generated and displayed on the screen.

## Support
If you encounter any issues or have questions, please open an issue on the GitLab repository or contact the project maintainer.

## Roadmap
- Add support for more languages.
- Improve the user interface.
- Add more summarization models.
- Implement user authentication and save summaries.

## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with clear messages.
4. Push your changes to your fork.
5. Create a pull request to the main repository.

## Authors and acknowledgment
- Leo - Project Maintainer

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Project status
The project is actively maintained. Contributions and feedback are welcome.