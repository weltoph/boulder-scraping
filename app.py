from quart import Quart, jsonify, request, abort
import datetime
import model


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

    # Filtering for dates in sql seems to be hard, so we do this in Python.
    datapoints = list(model.DataPoint.select())
    errorpoints = list(model.ErrorPoint.select())

    return jsonify({
        "beginning": beginning_date,
        "ending": end_date,
        "data": [
            {
                "date": dp.date.isoformat(),
                "place": str(dp.place),
                "boulder": int(dp.boulder) if dp.boulder is not None else None,
                "climbing": (int(dp.climbing)
                             if dp.climbing is not None
                             else None)}
            for dp in model.DataPoint.select()
            if beginning_date <= datetime.date(dp.date.year,
                                               dp.date.month,
                                               dp.date.day) <= end_date],
        "errors": [
            {
                "date": ep.date.isoformat(),
                "msg": str(ep.msg)}
            for ep in model.ErrorPoint.select()
            if beginning_date <= datetime.date(ep.date.year,
                                                ep.date.month,
                                                ep.date.day) <= end_date]
        })


if __name__ == "__main__":
    app.run()
