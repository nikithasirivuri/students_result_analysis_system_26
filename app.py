
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# STUDENT RESULT ANALYSIS SYSTEM
# ==========================================

st.set_page_config(
    page_title="Student Result Analysis",
    page_icon="📊",
    layout="wide"
)

# Store student details during the session

if "students" not in st.session_state:
    st.session_state.students = []


# ==========================================
# GRADE CALCULATION
# ==========================================

def calculate_grade(percentage):

    if percentage >= 90:
        return "s"

    elif percentage >= 80:
        return "A"

    elif percentage >= 70:
        return "B"

    elif percentage >= 60:
        return "C"

    elif percentage >= 50:
        return "D"

    else:
        return "F"


# ==========================================
# RESULT CALCULATION
# ==========================================

def calculate_results(data):

    df = pd.DataFrame(data)

    df["Total"] = (
        df["Python"] +
        df["DBMS"] +
        df["Maths"]
    )

    df["Percentage"] = df["Total"] / 3

    df["Grade"] = df["Percentage"].apply(calculate_grade)

    df["Result"] = df.apply(
        lambda row: "Pass"
        if row["Python"] >= 35
        and row["DBMS"] >= 35
        and row["Maths"] >= 35
        else "Fail",
        axis=1
    )

    return df


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🎓 Student Analysis")

st.sidebar.write("Welcome to our project!")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Student Entry",
        "Student Records",
        "Result Analysis"
    ]
)

st.sidebar.markdown("---")

st.sidebar.write(
    "Students Entered:",
    len(st.session_state.students),
    "/ 10"
)

st.sidebar.progress(
    len(st.session_state.students) / 10
)


# ==========================================
# WEBSITE TITLE
# ==========================================

st.title("🎓 Student Result Analysis System")

st.write(
    "A Python-based application to analyse "
    "student academic performance."
)

st.markdown("---")


# ==========================================
# STUDENT ENTRY PAGE
# ==========================================

if page == "Student Entry":

    st.header("📝 Enter Student Details")

    st.write(
        "Enter the details of up to 10 students."
    )

    if len(st.session_state.students) < 10:

        with st.form("student_form"):

            roll_no = st.number_input(
                "Roll Number",
                min_value=1,
                step=1
            )

            name = st.text_input(
                "Student Name"
            )

            st.subheader("Enter Subject Marks")

            python = st.number_input(
                "Python",
                min_value=0,
                max_value=100,
                step=1
            )

            dbms = st.number_input(
                "DBMS",
                min_value=0,
                max_value=100,
                step=1
            )

            maths = st.number_input(
                "Mathematics",
                min_value=0,
                max_value=100,
                step=1
            )

            submit = st.form_submit_button(
                "Add Student"
            )

            if submit:

                if name.strip() == "":
                    st.error("Please enter student name.")

                elif any(
                    s["Roll No"] == roll_no
                    for s in st.session_state.students
                ):
                    st.error("Roll number already exists.")

                else:

                    student = {
                        "Roll No": int(roll_no),
                        "Name": name.strip(),
                        "Python": int(python),
                        "DBMS": int(dbms),
                        "Maths": int(maths)
                    }

                    st.session_state.students.append(
                        student
                    )

                    st.success(
                        "Student details added successfully!"
                    )

                    st.rerun()

    else:

        st.success("All 10 student records have been entered!")


    st.write(
        "Total Students Added:",
        len(st.session_state.students)
    )


# ==========================================
# CHECK DATA
# ==========================================

if len(st.session_state.students) > 0:

    df = calculate_results(
        st.session_state.students
    )

else:

    df = pd.DataFrame()


# ==========================================
# DASHBOARD PAGE
# ==========================================

if page == "Dashboard":

    st.header("📊 Dashboard")

    if len(df) > 0:

        total = len(df)

        passed = (df["Result"] == "Pass").sum()

        failed = (df["Result"] == "Fail").sum()

        average = df["Percentage"].mean()

        pass_percentage = (passed / total) * 100

        # Display summary cards

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Students", total)

        col2.metric("Passed", passed)

        col3.metric("Failed", failed)

        col4.metric(
            "Class Average",
            str(round(average, 2)) + "%"
        )

        st.markdown("---")

        st.subheader("Class Performance")

        st.write(
            "Pass Percentage:",
            round(pass_percentage, 2),
            "%"
        )

        # Subject-wise average

        subjects = ["Python", "DBMS", "Maths"]

        averages = [
            df["Python"].mean(),
            df["DBMS"].mean(),
            df["Maths"].mean()
        ]

        fig, ax = plt.subplots()

        ax.bar(subjects, averages)

        ax.set_title("Subject-wise Average Marks")

        ax.set_xlabel("Subjects")

        ax.set_ylabel("Average Marks")

        ax.set_ylim(0, 100)

        st.pyplot(fig)

        plt.close(fig)

        # Pass and fail chart

        st.subheader("Pass and Fail Analysis")

        fig, ax = plt.subplots()

        ax.pie(
            [passed, failed],
            labels=["Passed", "Failed"],
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title("Student Results")

        st.pyplot(fig)

        plt.close(fig)

    else:

        st.info(
            "No student records available. "
            "Go to Student Entry to add students."
        )


# ==========================================
# STUDENT RECORDS PAGE
# ==========================================

if page == "Student Records":

    st.header("📋 Student Records")

    if len(df) > 0:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Please enter student details first.")


# ==========================================
# RESULT ANALYSIS PAGE
# ==========================================

if page == "Result Analysis":

    st.header("📈 Result Analysis")

    if len(df) > 0:

        # Topper details

        topper = df.loc[
            df["Percentage"].idxmax()
        ]

        st.subheader("🏆 Class Topper")

        st.success(
            "Name: " + topper["Name"] +
            " | Percentage: " +
            str(round(topper["Percentage"], 2)) + "%"
        )

        # Subject analysis

        st.subheader("Subject-wise Average")

        subjects = ["Python", "DBMS", "Maths"]

        for subject in subjects:

            average = df[subject].mean()

            st.write(
                subject,
                ":",
                round(average, 2)
            )

        st.markdown("---")

        # Grade distribution

        st.subheader("Grade Analysis")

        grade_counts = df["Grade"].value_counts()

        st.dataframe(
            grade_counts.rename("Students"),
            use_container_width=True
        )

        st.markdown("---")

        # Student performance chart

        st.subheader("Student-wise Performance")

        top_students = df.sort_values(
            by="Percentage",
            ascending=False
        ).head(10)

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(
            top_students["Name"],
            top_students["Percentage"]
        )

        ax.set_title("Top 5 Student Performance")

        ax.set_xlabel("Student Name")

        ax.set_ylabel("Percentage")

        ax.set_ylim(0, 100)

        plt.xticks(rotation=45)

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)

        # Display failed students

        st.subheader("Students Who Failed")

        failed_students = df[
            df["Result"] == "Fail"
        ]

        if len(failed_students) > 0:

            st.dataframe(
                failed_students,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success("All students passed!")

    else:

        st.info(
            "Enter student details to view result analysis."
        )


# ==========================================
# DOWNLOAD RESULTS
# ==========================================

st.sidebar.markdown("---")

if len(df) > 0:

    csv = df.to_csv(index=False).encode("utf-8")

    st.sidebar.download_button(
        label="📥 Download Result CSV",
        data=csv,
        file_name="Student_Results.csv",
        mime="text/csv"
    )


# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "Student Result Analysis System | "
    "Developed using Python, Pandas, "
    "Matplotlib and Streamlit"
)
