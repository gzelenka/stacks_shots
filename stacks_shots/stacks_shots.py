import cf_indexer

from flask import Flask, render_template, request, url_for

cf = cf_indexer.cf_indexer()
cf.populate_videos()

app = Flask(__name__)


def repop_vids():
    cf.populate_videos()


@app.route("/")
def list_games():
    return render_template("bouts.html", bouts=cf.videos)


@app.route("/player/<string:cont>/<string:name>/<string:size>")
def launch_player(cont, name, size):
    print "ROFL %s %s %s" % (cont, name, size)
    u = cf.get_url(cont, name, size)
    print "launching the player: %s" % u
    return render_template("player.htm", url=u, game=cont, jam=name, size=size)


@app.route("/game", methods=['GET'])
def list_jams():
    if request.method == "GET" and 'game' in request.args:
        return render_template("game.html", game=request.args.get('game'),
                               jams=cf.videos[request.args.get('game')])
    else:
        return render_template(url_for("list_games"))


if __name__ == "__main__":
    app.run(debug=True)
