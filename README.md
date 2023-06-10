# Getting Started with Application

This guide provides step-by-step instructions for setting up and running the application on your local machine.

## Prerequisites

Before starting, ensure that you have the following prerequisites installed:

- Python (version 3.7 or higher)
- Git

## Clone the Git Repository

1. Open your terminal or command prompt.
2. Change the current working directory to the location where you want to clone the repository.
3. Run the following command to clone the repository:


Replace `<repository_url>` with the actual URL of the Git repository.

## Create and Activate a Virtual Environment

1. Change the current working directory to the cloned repository:


Replace `<repository_directory>` with the actual directory name of the cloned repository.

2. Create a new virtual environment by running the following command:


3. Activate the virtual environment:

- For Windows:

  ```
  venv\Scripts\activate
  ```

- For macOS/Linux:

  ```
  source venv/bin/activate
  ```

## Install Requirements

1. Make sure your virtual environment is activated.

2. Install the required Python packages by running the following command:


This will install all the necessary dependencies for the application.

## Configure Environment Variables

1. Rename the `.env.example` file to `.env`.

2. Open the `.env` file and update the MongoDB connection URL and database name according to your setup.

## Start the Application

1. Make sure your virtual environment is activated.

2. Run the following command to start the application:


This will start the application server and enable auto-reloading for code changes.

3. Open a web browser and visit `http://localhost:8000` to access the application.

## Conclusion

You have successfully set up and started the application on your local machine. Now you can explore and use the features of the application.
