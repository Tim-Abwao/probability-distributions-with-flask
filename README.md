# Statistical Distributions with Flask

A simple app to learn basic facts about several popular and useful statistical distributions.

Powered by:

- [Flask][1] - web application interface
- [Pandas][2] - data manipulation
- [SciPy][3] - statistical distributions and functions
- [Seaborn][4] - plotting/visualisation

![screencast](stats_app/static/screen.gif)

A similar, interactive version of this app based on [Dash][5] is available [here][6].

## Getting Started

- Download the files, create a virtual environment, and activate it:

    ```bash
    git clone https://github.com/Tim-Abwao/statistical-distributions-flask.git
    cd statistical-distributions-flask
    python3 -m venv venv
    source venv/bin/activate
    ```

- Install the required packages:

    ```bash
    pip install -U pip
    pip install -r requirements.txt
    ```

- Start the [flask development server][7]:

    ```bash
    export FLASK_APP=stats_app
    export FLASK_ENV=development
    flask run
    ```

Afterwards, browse to <http://localhost:5000>. That's all, enjoy.

[1]: https://flask.palletsprojects.com/en/1.1.x/
[2]: https://pandas.pydata.org
[3]: https://www.scipy.org
[4]: https://seaborn.pydata.org
[5]: https://plotly.com/dash/
[6]: https://statistics-distributions.herokuapp.com
[7]: https://flask.palletsprojects.com/en/1.1.x/server/
