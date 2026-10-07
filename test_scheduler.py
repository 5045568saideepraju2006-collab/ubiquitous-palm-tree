from scheduler import generate_timetable


classes = [
    {
        "id": "10A",
        "name": "Class 10-A"
    },
    {
        "id": "10B",
        "name": "Class 10-B"
    }
]


teachers = [
    {
        "id": "T1",
        "name": "Mr. Kumar"
    },
    {
        "id": "T2",
        "name": "Ms. Priya"
    },
    {
        "id": "T3",
        "name": "Mr. Arun"
    }
]


rooms = [
    {
        "id": "R1",
        "name": "Room 101"
    },
    {
        "id": "R2",
        "name": "Room 102"
    }
]


subjects = [
    {
        "id": "MATH",
        "name": "Mathematics",
        "class_id": "10A",
        "teacher_id": "T1",
        "room_id": "R1",
        "periods_per_week": 5
    },

    {
        "id": "PHYSICS",
        "name": "Physics",
        "class_id": "10A",
        "teacher_id": "T2",
        "room_id": "R2",
        "periods_per_week": 4
    },

    {
        "id": "ENGLISH",
        "name": "English",
        "class_id": "10A",
        "teacher_id": "T3",
        "room_id": "R1",
        "periods_per_week": 4
    },

    {
        "id": "MATH2",
        "name": "Mathematics",
        "class_id": "10B",
        "teacher_id": "T1",
        "room_id": "R1",
        "periods_per_week": 5
    },

    {
        "id": "PHYSICS2",
        "name": "Physics",
        "class_id": "10B",
        "teacher_id": "T2",
        "room_id": "R2",
        "periods_per_week": 4
    },

    {
        "id": "ENGLISH2",
        "name": "English",
        "class_id": "10B",
        "teacher_id": "T3",
        "room_id": "R1",
        "periods_per_week": 4
    }
]


result = generate_timetable(
    classes,
    subjects,
    teachers,
    rooms
)


print("\n================================")
print("CLASH-FREE TIMETABLE")
print("================================\n")


if result["success"]:

    for entry in result["timetable"]:

        print(
            f'{entry["day"]:10} '
            f'Period {entry["period"]} | '
            f'{entry["class_id"]:5} | '
            f'{entry["subject"]:15} | '
            f'{entry["teacher_id"]:3} | '
            f'{entry["room_id"]}'
        )

else:

    print(result["message"])