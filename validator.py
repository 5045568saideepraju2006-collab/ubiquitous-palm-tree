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


def validate_input(classes, subjects, teachers, rooms):
    """
    Validate all timetable input before sending it
    to the scheduling engine.
    """

    errors = []

    # ---------------------------------------------------------
    # CHECK DUPLICATE IDS
    # ---------------------------------------------------------

    class_ids = [item["id"] for item in classes]
    teacher_ids = [item["id"] for item in teachers]
    room_ids = [item["id"] for item in rooms]
    subject_ids = [item["id"] for item in subjects]

    if len(class_ids) != len(set(class_ids)):
        errors.append("Duplicate class IDs found.")

    if len(teacher_ids) != len(set(teacher_ids)):
        errors.append("Duplicate teacher IDs found.")

    if len(room_ids) != len(set(room_ids)):
        errors.append("Duplicate room IDs found.")

    if len(subject_ids) != len(set(subject_ids)):
        errors.append("Duplicate subject IDs found.")

    # ---------------------------------------------------------
    # CHECK REFERENCES
    # ---------------------------------------------------------

    class_id_set = set(class_ids)
    teacher_id_set = set(teacher_ids)
    room_id_set = set(room_ids)

    for subject in subjects:

        subject_name = subject.get("name", "Unknown subject")

        if subject["class_id"] not in class_id_set:
            errors.append(
                f'{subject_name}: class "{subject["class_id"]}" does not exist.'
            )

        if subject["teacher_id"] not in teacher_id_set:
            errors.append(
                f'{subject_name}: teacher "{subject["teacher_id"]}" does not exist.'
            )

        if subject["room_id"] not in room_id_set:
            errors.append(
                f'{subject_name}: room "{subject["room_id"]}" does not exist.'
            )

    # ---------------------------------------------------------
    # CHECK PERIOD COUNTS
    # ---------------------------------------------------------

    total_slots = len(DAYS) * len(PERIODS)

    for subject in subjects:

        periods = subject.get("periods_per_week", 0)

        if periods <= 0:

            errors.append(
                f'{subject["name"]}: periods_per_week must be greater than 0.'
            )

        if periods > total_slots:

            errors.append(
                f'{subject["name"]}: requires {periods} periods, '
                f'but only {total_slots} weekly slots exist.'
            )

    # ---------------------------------------------------------
    # CHECK EMPTY DATA
    # ---------------------------------------------------------

    if len(classes) == 0:
        errors.append("At least one class is required.")

    if len(teachers) == 0:
        errors.append("At least one teacher is required.")

    if len(rooms) == 0:
        errors.append("At least one room is required.")

    if len(subjects) == 0:
        errors.append("At least one subject is required.")

    return errors


def validate_timetable(timetable):
    """
    Check the generated timetable for clashes.
    """

    errors = []

    class_slots = {}
    teacher_slots = {}
    room_slots = {}

    for entry in timetable:

        slot = (
            entry["day"],
            entry["period"]
        )

        class_id = entry["class_id"]
        teacher_id = entry["teacher_id"]
        room_id = entry["room_id"]

        # -----------------------------------------------------
        # CLASS CLASH
        # -----------------------------------------------------

        class_key = (
            class_id,
            slot
        )

        if class_key in class_slots:

            previous = class_slots[class_key]

            errors.append(
                f'CLASS CLASH: {class_id} has '
                f'"{previous["subject"]}" and '
                f'"{entry["subject"]}" at '
                f'{entry["day"]} Period {entry["period"]}.'
            )

        else:

            class_slots[class_key] = entry

        # -----------------------------------------------------
        # TEACHER CLASH
        # -----------------------------------------------------

        teacher_key = (
            teacher_id,
            slot
        )

        if teacher_key in teacher_slots:

            previous = teacher_slots[teacher_key]

            errors.append(
                f'TEACHER CLASH: {teacher_id} is teaching '
                f'"{previous["subject"]}" and '
                f'"{entry["subject"]}" at '
                f'{entry["day"]} Period {entry["period"]}.'
            )

        else:

            teacher_slots[teacher_key] = entry

        # -----------------------------------------------------
        # ROOM CLASH
        # -----------------------------------------------------

        room_key = (
            room_id,
            slot
        )

        if room_key in room_slots:

            previous = room_slots[room_key]

            errors.append(
                f'ROOM CLASH: {room_id} is being used by '
                f'{previous["class_id"]} and '
                f'{entry["class_id"]} at '
                f'{entry["day"]} Period {entry["period"]}.'
            )

        else:

            room_slots[room_key] = entry

    return errors