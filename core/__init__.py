import ConfigParser, os
from flask import Flask
from flask.ext.mongoengine import MongoEngine

cfg = ConfigParser.SafeConfigParser()
cfg.read(os.getenv("WorkflowConfig","config/dampe.cfg"))

app = Flask(__name__)
app.config['MONGODB_DB']=cfg.get("database","name")
app.config['MONGODB_USERNAME']=cfg.get("database","user")
app.config['MONGODB_PASSWORD']=cfg.get("database","password")
app.config['MONGODB_HOST']=cfg.get("database","host")
app.config["SECRET_KEY"] = "KeepThisS3cr3t"
db = MongoEngine(app)


@app.route("/jobs")
def jobs(self):
    db.connect()
    res = []
    for job in models.Job.objects:
        res.append(job.jobInstance.to_dict())
    return json.dumps(res)

if __name__ == '__main__':
    app.run()
