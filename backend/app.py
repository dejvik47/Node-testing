from flask import Flask
from modules.db_handler import commit_query, execute_query

app = Flask(__name__)

@app.route("/")
def index():
    test_data_q = "SELECT * FROM testing.maintenance_qr_eventlog ORDER BY id DESC"
    data = commit_query(test_data_q,"testing_db.conf") 
    return 


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)