# Zendesk Automation Scripts

This repository contains Python scripts designed to automate and streamline tasks within Zendesk. These scripts utilize the Zendesk API to perform various operations, making it easier to manage tickets, users, and other administrative functions.

## Features

- **Ticket Management**: Automate tasks such as ticket updates, bulk deletions, or assigning tickets to agents.
- **User Management**: Handle user creation, updates, or bulk operations.
- **Data Export**: Extract Zendesk data for reporting or analysis.
- **Custom Automations**: Implement specific workflows tailored to your Zendesk instance.

## Prerequisites

Before using these scripts, make sure you have the following:

- **Python 3.8 or higher** installed on your machine.
- Access to your Zendesk API token and admin credentials.
- Required Python libraries (listed in `requirements.txt`).

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/zendesk-automation-scripts.git
   cd zendesk-automation-scripts
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your Zendesk credentials:
   ```env
   ZENDESK_SUBDOMAIN=your_subdomain
   ZENDESK_EMAIL=your_email@example.com
   ZENDESK_API_TOKEN=your_api_token
   ```

## Usage

Run any of the scripts in the repository by executing them from the command line. For example:
```bash
python bulk_delete_tickets.py
```

### Example Scripts

- **bulk_delete_tickets.py**: Deletes a batch of tickets based on certain criteria.
- **export_tickets.py**: Extracts ticket data into a CSV file.
- **update_ticket_status.py**: Updates ticket statuses in bulk.

## Configuration

Modify the `config.json` file (if included) to customize the scripts' behavior, such as setting filters for tickets or defining specific fields to update.

## Contributing

Feel free to fork this repository and submit pull requests for improvements or new features. Make sure to follow proper coding standards and document your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

These scripts were created with guidance from ChatGPT and adapted for specific Zendesk workflows. Special thanks to the Zendesk Developer documentation for detailed API references.

---

Happy automating! 🚀

