# NewsMonitor

NewsMonitor is a Python project that fetches news from various sources and saves new articles to an Excel file. The script is designed to run every hour to keep the news articles up-to-date.

## Installation

This project requires Python 3.8 or higher. 

1. Clone the repository:
    ```
    git clone https://github.com/yourusername/NewsMonitor.git
    ```
2. Navigate to the project directory:
    ```
    cd NewsMonitor
    ```
3. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

## Usage

To run the project, navigate to the `src` directory and run `main.py`:

python main.py


## Scheduling the Script

To keep the news articles up-to-date, you should schedule the script to run every hour. Here's how you can do it:

### On Unix-based systems (like MacOS and Linux)

You can use `cron` to schedule the script. Open your crontab file with the command:

crontab -e


Then, add the following line to schedule the script to run every hour:

0 * * * * /usr/bin/python3 /path/to/your/script/main.py


Don't forget to replace `/path/to/your/script/main.py` with the actual path to your `main.py` file.

### On Windows

You can use Task Scheduler to schedule the script:

1. Open Task Scheduler.
2. Click on "Create Basic Task...".
3. Name the task and click "Next".
4. Choose "Daily" and click "Next".
5. Set the start time and select "Recur every: 1 hours", then click "Next".
6. Choose "Start a program" and click "Next".
7. Browse to your Python executable file (usually located in `C:\PythonXX\python.exe` where `XX` is the version) in the "Program/script" field.
8. In the "Add arguments" field, put the path to your `main.py` script.
9. Click "Next" and then "Finish".

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
