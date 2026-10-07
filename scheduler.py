from ortools.sat.python import cp_model


DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]

PERIODS = [
    1,
    2,
    3,
    4,
    5,
    6
]


def generate_timetable(classes, subjects, teachers, rooms):
    """
    Generate a clash-free timetable.

    Each subject contains:
    - id
    - name
    - class_id
    - teacher_id
    - room_id
    - periods_per_week
    """

    model = cp_model.CpModel()

    # Total number of available time slots
    total_slots = len(DAYS) * len(PERIODS)

    lessons = []

    # ---------------------------------------------------------
    # CREATE LESSONS
    # ---------------------------------------------------------

    for subject in subjects:

        for lesson_number in range(subject["periods_per_week"]):

            lesson = {
                "id": f'{subject["id"]}_{lesson_number + 1}',
                "subject_id": subject["id"],
                "subject_name": subject["name"],
                "class_id": subject["class_id"],
                "teacher_id": subject["teacher_id"],
                "room_id": subject["room_id"]
            }

            lessons.append(lesson)

    # ---------------------------------------------------------
    # CREATE TIME VARIABLES
    # ---------------------------------------------------------

    lesson_slots = {}

    for lesson in lessons:

        lesson_slots[lesson["id"]] = model.new_int_var(
            0,
            total_slots - 1,
            f'slot_{lesson["id"]}'
        )

    # ---------------------------------------------------------
    # CLASS CLASH CONSTRAINT
    # ---------------------------------------------------------

    classes_lessons = {}

    for lesson in lessons:

        class_id = lesson["class_id"]

        if class_id not in classes_lessons:
            classes_lessons[class_id] = []

        classes_lessons[class_id].append(
            lesson_slots[lesson["id"]]
        )

    for class_id, slots in classes_lessons.items():

        model.add_all_different(slots)

    # ---------------------------------------------------------
    # TEACHER CLASH CONSTRAINT
    # ---------------------------------------------------------

    teacher_lessons = {}

    for lesson in lessons:

        teacher_id = lesson["teacher_id"]

        if teacher_id not in teacher_lessons:
            teacher_lessons[teacher_id] = []

        teacher_lessons[teacher_id].append(
            lesson_slots[lesson["id"]]
        )

    for teacher_id, slots in teacher_lessons.items():

        model.add_all_different(slots)

    # ---------------------------------------------------------
    # ROOM CLASH CONSTRAINT
    # ---------------------------------------------------------

    room_lessons = {}

    for lesson in lessons:

        room_id = lesson["room_id"]

        if room_id not in room_lessons:
            room_lessons[room_id] = []

        room_lessons[room_id].append(
            lesson_slots[lesson["id"]]
        )

    for room_id, slots in room_lessons.items():

        model.add_all_different(slots)

    # ---------------------------------------------------------
    # SOLVE
    # ---------------------------------------------------------

    solver = cp_model.CpSolver()

    solver.parameters.max_time_in_seconds = 10

    status = solver.solve(model)

    # ---------------------------------------------------------
    # CHECK RESULT
    # ---------------------------------------------------------

    if status not in (
        cp_model.OPTIMAL,
        cp_model.FEASIBLE
    ):

        return {
            "success": False,
            "message": "No clash-free timetable could be generated.",
            "timetable": []
        }

    # ---------------------------------------------------------
    # CONVERT SOLUTION
    # ---------------------------------------------------------

    timetable = []

    for lesson in lessons:

        slot = solver.value(
            lesson_slots[lesson["id"]]
        )

        day_index = slot // len(PERIODS)

        period_index = slot % len(PERIODS)

        timetable.append({
            "day": DAYS[day_index],
            "period": PERIODS[period_index],
            "class_id": lesson["class_id"],
            "subject_id": lesson["subject_id"],
            "subject": lesson["subject_name"],
            "teacher_id": lesson["teacher_id"],
            "room_id": lesson["room_id"]
        })

    # Sort timetable by day and period

    timetable.sort(
        key=lambda x: (
            DAYS.index(x["day"]),
            x["period"],
            x["class_id"]
        )
    )

    return {
        "success": True,
        "message": "Timetable generated successfully.",
        "timetable": timetable
    }