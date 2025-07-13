# Synthetic Data Generator

This project provides a framework for generating synthetic data for various data models. The generated data can be used for testing, development, and other purposes where real data is not available or cannot be used.

## Features

- Generate synthetic data for multiple data models.
- Support for various data types including UUID, name, gender, email, phone, company, job title, date of birth, boolean, number, choice, credit card, text, and datetime.
- Save generated data to CSV files.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/synthetic-data-generator.git
    cd synthetic-data-generator
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Define your data models in the [complexDataModelLinking.py](http://_vscodecontentref_/0) file. Example:
    ```python
    data_models = {
      "data_models": {
        "personal_info_model": [
            {"name": "User ID", "type":"uuid"},
            {"name": "Name", "type": "name"},
            {"name": "Gender", "type": "gender"},
            {"name": "Email", "type": "email"},
            {"name": "Phone", "type": "phone"},
            {"name": "Company", "type": "company"},
            {"name": "Job Title", "type": "job"},
            {"name": "Date of Birth", "type": "date_of_birth"},
            {"name": "Is Active", "type": "boolean"},
            {"name": "Salary", "type": "number", "min": 30000, "max": 150000},
            {"name": "Country", "type": "choice", "choices": ["USA", "Canada", "Germany", "UK", "India"]},
            {"name": "Credit Card", "type": "credit_card"},
            {"name": "Notes", "type": "text"},
            {"name": "Join Date", "type": "datetime"}
        ]
      }
    }
    ```

2. Generate and save the synthetic data by running the [LinkingCustomDataModel.py](http://_vscodecontentref_/1) script:
    ```sh
    python LinkingCustomDataModel.py
    ```

3. The generated data will be saved as CSV files in the current directory.

## Example

To generate synthetic data for the example models provided in the [LinkingCustomDataModel.py](http://_vscodecontentref_/2) file, run:
```sh
python LinkingCustomDataModel.py