# Flask web app for exploring Statistical Distributions

A simple app to learn something about several popular and useful statistical distributions.

Powered by [Flask][1], [Pandas][2], [SciPy][3] and [Seaborn][4]. The application is live [here][5].

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

Then browse to <http://127.0.0.1:5000>. That's all, enjoy.

[1]: https://palletsprojects.com/p/flask/
[2]: https://pandas.pydata.org
[3]: https://www.scipy.org
[4]: https://seaborn.pydata.org
[5]: https://statistics-distributions.herokuapp.com
