from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    final_room = None
    decision_log = []

    if request.method == "POST":
        raw_rooms = request.form["rooms"]
        class_strength = int(request.form["strength"])
        need_projector = request.form.get("projector") == "yes"

        rooms = []

        # Format: R1,60,yes | R2,40,no
        for item in raw_rooms.split("|"):
            name, cap, proj = item.strip().split(",")
            rooms.append({
                "name": name.strip(),
                "capacity": int(cap),
                "projector": proj.strip().lower() == "yes"
            })

        decision_log.append(f"Class strength entered: {class_strength}")
        decision_log.append(f"Projector needed: {need_projector}")

        eligible = []

        for room in rooms:
            if room["capacity"] < class_strength:
                decision_log.append(
                    f"{room['name']} rejected (capacity too small)"
                )
                continue

            if need_projector and not room["projector"]:
                decision_log.append(
                    f"{room['name']} rejected (no projector)"
                )
                continue

            room["wastage"] = room["capacity"] - class_strength
            eligible.append(room)

            decision_log.append(
                f"{room['name']} accepted (unused seats: {room['wastage']})"
            )

        if eligible:
            eligible.sort(key=lambda x: x["wastage"])
            best = eligible[0]
            final_room = f"{best['name']} (Capacity {best['capacity']})"
            decision_log.append(
                f"Selected {best['name']} as it has minimum unused seats"
            )
        else:
            final_room = "No suitable room found"

    return render_template(
        "home.html",
        result=final_room,
        log=decision_log
    )

if __name__ == "__main__":
    app.run(debug=True)