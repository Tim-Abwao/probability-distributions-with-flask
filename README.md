# Flask web app for exploring Statistical Distributions

A simple app to learn something about several popular and useful statistical distributions.

Powered by [Flask][1], [Pandas][2], [SciPy][3] and [Seaborn][4].

![screencast](static/screen.gif)

A similar, interactive version of this app based on [Dash][5] is live [here][6].

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

- There are various ways to run the application. A simple one is:

    ```bash
    python app.py
    ```

    But the [recommended][7] way to run it is:

    ```bash
    export FLASK_APP=app
    export FLASK_ENV=development
    flask run
    ```

Afterwards, browse to <http://localhost:5000>. That's all, enjoy.

[1]: https://palletsprojects.com/p/flask/
[2]: https://pandas.pydata.org
[3]: https://www.scipy.org
[4]: https://seaborn.pydata.org
[5]: https://plotly.com/dash/
[6]: https://statistics-distributions.herokuapp.com
[7]: https://flask.palletsprojects.com/en/master/server/#command-line
