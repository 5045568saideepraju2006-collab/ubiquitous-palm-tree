import streamlit as st
import sys
import os

# Allow importing files from the backend folder
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from scheduler import generate_timetable
from validator import validate_input, validate_timetable


st.set_page_config(
    page_title="Clash-Free Timetable Generator",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Clash-Free Timetable Generator")
st.write("Generate a clash-free school timetable using OR-Tools.")


# -----------------------------
# Sample data
# -----------------------------

default_classes = [
    {"id": "10A", "name": "Class 10A"},
    {"id": "10B", "name": "Class 10B"},
]

default_teachers = [
    {"id": "T1", "name": "Teacher 1"},
    {"id": "T2", "name": "Teacher 2"},
    {"id": "T3", "name": "Teacher 3"},
]

default_rooms = [
    {"id": "R1", "name": "Room 1"},
    {"id": "R2", "name": "Room 2"},
]

default_subjects = [
    {
        "id": "MATH10A",
        "name": "Mathematics",
        "class_id": "10A",
        "teacher_id": "T1",
        "room_id": "R1",
        "periods_per_week": 5,
    },
    {
        "id": "ENG10A",
        "name": "English",
        "class_id": "10A",
        "teacher_id": "T2",
        "room_id": "R1",
        "periods_per_week": 5,
    },
    {
        "id": "SCI10A",
        "name": "Science",
        "class_id": "10A",
        "teacher_id": "T3",
        "room_id": "R2",
        "periods_per_week": 4,
    },
    {
        "id": "MATH10B",
        "name": "Mathematics",
        "class_id": "10B",
        "teacher_id": "T1",
        "room_id": "R2",
        "periods_per_week": 5,
    },
    {
        "id": "ENG10B",
        "name": "English",
        "class_id": "10B",
        "teacher_id": "T2",
        "room_id": "R2",
        "periods_per_week": 5,
    },
    {
        "id": "SCI10B",
        "name": "Science",
        "class_id": "10B",
        "teacher_id": "T3",
        "room_id": "R1",
        "periods_per_week": 4,
    },
]


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("Timetable Settings")

st.sidebar.info(
    "This version uses sample classes, teachers, rooms and subjects. "
    "You can modify the code later to accept custom data."
)


# -----------------------------
# Show input data
# -----------------------------

with st.expander("📋 View Input Data", expanded=False):

    st.subheader("Classes")
    st.dataframe(default_classes, use_container_width=True)

    st.subheader("Teachers")
    st.dataframe(default_teachers, use_container_width=True)

    st.subheader("Rooms")
    st.dataframe(default_rooms, use_container_width=True)

    st.subheader("Subjects")
    st.dataframe(default_subjects, use_container_width=True)


# -----------------------------
# Generate timetable
# -----------------------------

if st.button("🚀 Generate Timetable", type="primary"):

    with st.spinner("Generating clash-free timetable..."):

        # Validate input
        input_errors = validate_input(
            classes=default_classes,
            subjects=default_subjects,
            teachers=default_teachers,
            rooms=default_rooms,
        )

        if input_errors:

            st.error("❌ Invalid timetable data.")

            for error in input_errors:
                st.write(f"- {error}")

        else:

            # Generate timetable
            result = generate_timetable(
                classes=default_classes,
                subjects=default_subjects,
                teachers=default_teachers,
                rooms=default_rooms,
            )

            if not result["success"]:

                st.error(result["message"])

            else:

                timetable = result["timetable"]

                # Validate generated timetable
                timetable_errors = validate_timetable(timetable)

                if timetable_errors:

                    st.error("❌ Timetable contains clashes.")

                    for error in timetable_errors:
                        st.write(f"- {error}")

                else:

                    st.success(
                        "✅ Timetable generated and validated successfully!"
                    )

                    # Convert to display format
                    display_data = []

                    for item in timetable:
                        display_data.append(
                            {
                                "Day": item["day"],
                                "Period": item["period"],
                                "Class": item["class_id"],
                                "Subject": item["subject"],
                                "Teacher": item["teacher_id"],
                                "Room": item["room_id"],
                            }
                        )

                    st.subheader("📅 Generated Timetable")

                    st.dataframe(
                        display_data,
                        use_container_width=True,
                        hide_index=True,
                    )

                    # Download CSV
                    import pandas as pd

                    df = pd.DataFrame(display_data)

                    csv = df.to_csv(index=False)

                    st.download_button(
                        label="⬇️ Download Timetable CSV",
                        data=csv,
                        file_name="timetable.csv",
                        mime="text/csv",
                    )

                    st.success("🎉 No class, teacher, or room clashes found!")
