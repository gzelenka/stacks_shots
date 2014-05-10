
import cf_indexer

from flask import Flask, render_template

cf = cf_indexer.cf_indexer()
cf.populate_videos()

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("player.htm")


@app.route("/video/<string:cont>/<string:name>/<string:size>")
def get_vid(cont, name, size):
    print "ROFL %s %s %s" % (cont, name, size)
    a = cf.get_file(cont, name, size)
    return "<Content-type: video/H264>\r\n" + a


if __name__ == "__main__":
    print cf.videos
    app.run(debug=True)
