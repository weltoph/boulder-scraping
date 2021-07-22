from quart import Quart, jsonify, request, abort
import datetime


app = Quart(__name__)


@app.route("/")
async def get_data():
    beginning = request.args.get("start", None)
    if beginning is None:
        abort(403, description="Missing start parameter.")
    try:
        parsed = datetime.datetime.strptime(beginning, "%Y-%m-%d")
        beginning_date = datetime.date(parsed.year, parsed.month, parsed.day)
    except ValueError:
        abort(403,
              description=("Could not parse start parameter. "
                           "Format: YYYY-MM-DD"))

    ending = request.args.get("end", None)
    if ending is None:
        end_date = datetime.date.today()
    else:
        try:
            parsed = datetime.datetime.strptime(ending, "%Y-%m-%d")
            end_date = datetime.date(parsed.year, parsed.month, parsed.day)
        except ValueError:
            abort(403,
                  description=("Could not parse end parameter. "
                               "Format: YYYY-MM-DD"))

    return jsonify({
        "beginning": beginning_date,
        "type_beginning": str(type(beginning_date)),
        "ending": end_date,
        "type_ending": str(type(end_date))})


if __name__ == "__main__":
    app.run()
